#!/usr/bin/env python3
"""Overlay redacted copies of mount-set documentation that names an excluded study.

Used by run.sh when SSB_DATASET_EXCLUDE is set. Walks the dataset directories that WILL be
mounted, looks at documentation-type files (README, notes, codebooks, scripts; bounded size —
never the microdata itself), and for every file that names an excluded study writes a copy
with those lines replaced by a marker under <out-dir>/, printing one `src:dst:ro` line per
file for the launcher to add as a nested bind mount over the original. Nothing under
`data/` is modified.

    redact_mounts.py --exclude a,b,c --out <dir> <dataset-dir> [...] [--file data/README.md]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DOC_SUFFIXES = {".md", ".txt", ".html", ".htm", ".r", ".py", ".do", ".qmd", ".rmd", ".rtf", ".json",
                ".yaml", ".yml", ".toml", ".sh", ".ipynb", ".tex", ".bib", ".csv"}
MAX_BYTES = 2_000_000
ALIASES = {
    "goldwert2026": ["goldwert"], "orchinik2024": ["orchinik"], "kim2024": ["kim2024", "kim et al", "kim_et_al"],
    "dablander2025": ["dablander"], "altenmueller2024": ["altenmueller", "altenmüller", "altenmuller"],
    "kerwer2025": ["kerwer"], "beall2017": ["beall"],
    "bbprime2025": ["bbprime", "bb prime", "bb_prime", "bb-prime", "big-bang", "bigbang", "big bang"],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="*", type=Path)
    ap.add_argument("--file", action="append", type=Path, default=[])
    ap.add_argument("--exclude", required=True)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()
    names = [n.strip() for n in a.exclude.split(",") if n.strip()]
    pats = []
    for n in names:
        pats.append(re.escape(n))
        pats += [re.escape(x) for x in ALIASES.get(n, [])]
    rx = re.compile("|".join(pats), re.IGNORECASE)
    files = list(a.file)
    # Under downloads/ only documentation is eligible: a data or stimulus file that happens to
    # contain an alias (e.g. a common word inside a message text) must not be altered; it is
    # reported on stderr instead.
    doc_name = re.compile(r"readme|codebook|notes?|licen[cs]e|manifest|documentation|fetch|\.md$|\.txt$|\.html?$",
                          re.IGNORECASE)
    skipped = []
    for d in a.dirs:
        for p in d.rglob("*"):
            if not (p.is_file() and p.suffix.lower() in DOC_SUFFIXES and p.stat().st_size <= MAX_BYTES
                    and "__pycache__" not in p.parts):
                continue
            if "downloads" in p.parts and not doc_name.search(p.name):
                try:
                    if rx.search(p.read_text(errors="ignore")):
                        skipped.append(p)
                except OSError:
                    pass
                continue
            files.append(p)
    for p in skipped:
        print(f"# NOT overlaid (data file under downloads/ names an excluded study — inspect): {p}", file=sys.stderr)
    n_over = 0
    for p in files:
        try:
            text = p.read_text(errors="ignore")
        except OSError:
            continue
        if not rx.search(text):
            continue
        out_lines, n = [], 0
        for ln in text.split("\n"):
            if rx.search(ln):
                n += 1
                out_lines.append("[line redacted: names a held-out study]")
            else:
                out_lines.append(ln)
        dst = a.out / p.resolve().relative_to(Path.cwd().resolve()) if p.resolve().is_relative_to(Path.cwd().resolve()) \
            else a.out / p.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text("\n".join(out_lines))
        print(f"{p.resolve()}:{dst.resolve()}:{n}")
        n_over += 1
    print(f"# {len(files)} files inspected, {n_over} overlaid", file=sys.stderr)


if __name__ == "__main__":
    main()
