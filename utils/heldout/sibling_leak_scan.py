#!/usr/bin/env python3
"""Audit: scan files for mentions of held-out study names (and their aliases).

Usage:
    python3 utils/heldout/sibling_leak_scan.py [--names a,b,c] [--quiet] PATH [PATH ...]

Paths may be files or directories (walked recursively; __pycache__, .git and
binary files skipped). Matching is case-insensitive substring on each line.
Prints, per file, the hit count and each matching line with its line number,
then a summary. Exit status 1 if any hit was found, 0 otherwise.

Stdlib only. The alias table below maps canonical study names to the strings
that count as a mention. Unknown names passed via --names are matched literally.
"""
import argparse
import os
import re
import sys

ALIASES = {
    "goldwert2026": ["goldwert2026", "goldwert"],  # NB: 'vlasceanu' is NOT an alias (vlasceanu2024 is a separate training study)
    "orchinik2024": ["orchinik2024", "orchinik"],
    "kim2024": ["kim2024", "kim et al", "kim_et_al"],
    "dablander2025": ["dablander2025", "dablander"],
    "altenmueller2024": ["altenmueller2024", "altenmueller", "altenmüller", "altenmuller"],
    "kerwer2025": ["kerwer2025", "kerwer"],
    "beall2017": ["beall2017", "beall"],
    "bbprime2025": ["bbprime2025", "bbprime", "bb prime", "bb_prime", "big-bang", "bigbang", "big bang"],
}

DEFAULT_NAMES = list(ALIASES)
SKIP_DIRS = {"__pycache__", ".git", ".venv", "node_modules"}
BINARY_EXT = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".pyc", ".zip", ".gz", ".parquet", ".xlsx", ".sav", ".dta", ".rds", ".rda"}


def build_pattern(names):
    terms = []
    for n in names:
        n = n.strip()
        if not n:
            continue
        terms.extend(ALIASES.get(n.lower(), [n]))
    terms = sorted(set(terms), key=len, reverse=True)
    return re.compile("|".join(re.escape(t) for t in terms), re.IGNORECASE)


def iter_files(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for f in sorted(files):
                if os.path.splitext(f)[1].lower() in BINARY_EXT:
                    continue
                yield os.path.join(root, f)


def scan_file(path, pat):
    hits = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for i, line in enumerate(fh, 1):
                if pat.search(line):
                    hits.append((i, line.rstrip("\n")))
    except (OSError, UnicodeDecodeError):
        return None
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--names", default=",".join(DEFAULT_NAMES), help="comma-separated study names (default: all held-out)")
    ap.add_argument("--quiet", action="store_true", help="only print per-file counts and summary")
    ap.add_argument("--maxlen", type=int, default=200, help="truncate printed lines to this many chars")
    ap.add_argument("paths", nargs="+")
    args = ap.parse_args(argv)

    pat = build_pattern(args.names.split(","))
    total_hits = 0
    files_with_hits = 0
    files_scanned = 0
    for path in iter_files(args.paths):
        hits = scan_file(path, pat)
        if hits is None:
            continue
        files_scanned += 1
        if not hits:
            continue
        files_with_hits += 1
        total_hits += len(hits)
        print(f"== {path}: {len(hits)} hit(s)")
        if not args.quiet:
            for ln, text in hits:
                text = text.strip()
                if len(text) > args.maxlen:
                    text = text[: args.maxlen] + "..."
                print(f"  {ln}: {text}")
    print(f"SUMMARY: {files_scanned} files scanned, {files_with_hits} files with hits, {total_hits} matching lines")
    return 1 if total_hits else 0


if __name__ == "__main__":
    sys.exit(main())
