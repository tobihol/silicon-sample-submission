#!/usr/bin/env python3
"""Build idea_02's read-only library from idea_01 — redacted so no held-out study leaks.

The 2026-08-25 sibling-leak scan found idea_01's AGENTS.md, OPEN.md, baselines, format
params and several tools carrying effect sizes, control-arm levels, practice scores and
calibration slopes of the eight studies idea_02 holds out. Mounting idea_01's run tree, or
any of those files as they are, would hand the idea_02 agent validation/internal-test truth.

This script writes `idea_02/run/inputs/idea01_lib/` deterministically:

    ssb/                 the ssb skill source, with the two known held-out constants neutralised
    SKILL.md
    DESIGN.md            paragraphs mentioning a held-out study removed
    AGENTS.md            numbered findings / paragraphs mentioning a held-out study removed
    RUNBOOK.md           as-is (commands and token tables)
    notes/               only the notes that never name a held-out study, block-redacted
    inputs/              outcome_families.json, prompt_budget.json, stimuli.json,
                         format_params.json minus the donation/newsletter blocks (goldwert-fitted),
                         measured/ minus goldwert2026_format.json,
                         baselines/ minus every row/entry sourced from a held-out study
    README.md            what was removed and why, with counts

then runs utils/heldout/sibling_leak_scan.py over the result and FAILS if any hit remains.
idea_01's own files are never modified. Re-run after any idea_01 change you want to carry over.
"""
from __future__ import annotations

import csv
import io
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "idea_01" / "run"
DST = REPO / "idea_02" / "run" / "inputs" / "idea01_lib"
SCAN = REPO / "utils" / "heldout" / "sibling_leak_scan.py"

HELD_OUT = ["goldwert2026", "orchinik2024", "kim2024", "dablander2025", "altenmueller2024",
            "kerwer2025", "beall2017", "bbprime2025"]
ALIASES = [r"goldwert", r"orchinik", r"kim2024", r"kim et al", r"dablander", r"altenm(?:ue|u|ü)ller",
           r"kerwer", r"beall", r"bb[\s_]?prime", r"big[\s-]?bang"]
# Held-out studies are sometimes described by data file, variable, or design WITHOUT the name
# (session-1 D2: finding 81's "sociologists vs economists" = altenmueller2024; DATA_experiments.md
# section 2's advocacy_data.csv/condName = goldwert2026). Redact those signatures too.
SIGNATURES = [
    r"advocacy_data", r"Advocacy_Cleaning", r"\bcondName\b",          # goldwert2026
    r"sociologist", r"economist", r"study4b",                          # altenmueller2024
    r"\bbovitz\b",                                                     # orchinik2024
    r"\babehsn\b", r"causal evidence", r"consensus messaging",        # kim2024
    r"scientist[- ]protest",                                           # dablander2025
    r"News Comments", r"BB[- ]PRIME",                                  # bbprime2025
    r"PsychArchives", r"\b14209\b", r"plain[- ]language summar",      # kerwer2025
    r"controvers[a-z]* (?:solution|matters)",                          # beall2017
]
NAME_RE = re.compile("|".join(ALIASES + SIGNATURES), re.IGNORECASE)

removed: dict[str, int] = {}


def note(path: str, n: int) -> None:
    removed[path] = removed.get(path, 0) + n


def redact_blocks(text: str) -> tuple[str, int]:
    """Drop every block that names a held-out study. A block is a blank-line-separated
    paragraph, except inside numbered/bulleted lists where each item (with its indented
    continuation lines) is a block; a heading whose section is emptied is kept."""
    lines = text.split("\n")
    blocks, cur = [], []
    def flush():
        if cur:
            blocks.append("\n".join(cur))
            cur.clear()
    for ln in lines:
        starts_item = bool(re.match(r"^\s*(\d+[.)]|[-*+]|\|)\s", ln)) and not ln.startswith("    ")
        if ln.strip() == "":
            flush(); blocks.append("")
        elif starts_item and cur and not cur[-1].strip() == "":
            flush(); cur.append(ln)
        elif ln.startswith("#"):
            flush(); cur.append(ln); flush()
        else:
            cur.append(ln)
    flush()
    kept, n = [], 0
    for b in blocks:
        if b and NAME_RE.search(b) and not b.lstrip().startswith("#"):
            n += 1
            kept.append("[…redacted: names a held-out study…]" if not b.lstrip().startswith("|") else "")
        else:
            kept.append(b)
    # line-level fallback: whatever the block splitter left (headings, code fences, table
    # rows inside a kept block) is dropped line by line so the scanner returns zero hits.
    out = []
    for ln in "\n".join(kept).split("\n"):
        if NAME_RE.search(ln):
            n += 1
            out.append("[…redacted line…]")
        else:
            out.append(ln)
    return "\n".join(out), n


def scrub_json(o):
    """Drop every key or string value that names a held-out study, recursively."""
    if isinstance(o, dict):
        return {k: scrub_json(v) for k, v in o.items()
                if not NAME_RE.search(k) and not (isinstance(v, str) and NAME_RE.search(v))}
    if isinstance(o, list):
        return [scrub_json(v) for v in o if not (isinstance(v, str) and NAME_RE.search(v))]
    return o


def copy_redacted_md(rel: str, dst_rel: str | None = None) -> None:
    text = (SRC / rel).read_text()
    out, n = redact_blocks(text)
    p = DST / (dst_rel or rel)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(out)
    note(rel, n)


def build():
    if DST.exists():
        shutil.rmtree(DST)
    DST.mkdir(parents=True)

    # --- ssb skill source: two known held-out constants
    skill = SRC / ".prime" / "agent" / "skills" / "ssb"
    shutil.copytree(skill / "src" / "ssb", DST / "ssb", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy(skill / "SKILL.md", DST / "SKILL.md")
    shutil.copy(skill / "pyproject.toml", DST / "ssb_pyproject.toml")
    synth = (DST / "ssb" / "synth.py").read_text()
    synth, n1 = re.subn(r'"donation_atoms":\s*\[\[[^\]]*\],\s*\[[^\]]*\],\s*\[[^\]]*\]\]',
                        '"donation_atoms": [[0.0, 2.5, 0.5], [5.0, 2.5, 0.5], [10.0, 2.5, 0.5]]  '
                        '# PLACEHOLDER (idea_02): idea_01 fitted this on a held-out study; refit on train', synth)
    synth, n2 = redact_blocks(synth)
    (DST / "ssb" / "synth.py").write_text(synth)
    note("ssb/synth.py", n1 + n2)
    pred = (DST / "ssb" / "predict.py").read_text()
    pred, n3 = redact_blocks(pred)
    (DST / "ssb" / "predict.py").write_text(pred)
    note("ssb/predict.py", n3)
    for f in ("task.py",):
        t = (DST / "ssb" / f).read_text()
        t, n = redact_blocks(t)
        (DST / "ssb" / f).write_text(t)
        note(f"ssb/{f}", n)

    # --- prose
    copy_redacted_md("DESIGN.md")
    copy_redacted_md("AGENTS.md")
    copy_redacted_md("RUNBOOK.md")
    for nm in ("DATA_experiments.md", "DATA_format.md", "DATA_baselines.md", "DATA_QSF_TEXTS.md",
               "DATA_VOELKEL2026_FORMAT.md", "DATA_KOETKE.md", "DATA_PEW.md"):
        if (SRC / "notes" / nm).exists():
            copy_redacted_md(f"notes/{nm}")

    # --- inputs
    (DST / "inputs").mkdir()
    for nm in ("outcome_families.json", "prompt_budget.json", "stimuli.json"):
        if (SRC / "inputs" / nm).exists():
            d = json.loads((SRC / "inputs" / nm).read_text())
            s = scrub_json(d)
            (DST / "inputs" / nm).write_text(json.dumps(s, indent=1, ensure_ascii=False))
            note(f"inputs/{nm}", len(json.dumps(d)) - len(json.dumps(s)) and 1)
    fp = json.loads((SRC / "inputs" / "format_params.json").read_text())
    dropped = [k for k in list(fp) if NAME_RE.search(json.dumps(fp[k]))]
    for k in dropped:
        fp[k] = {"REDACTED": "fitted on a held-out study in idea_01; refit on train"}
    (DST / "inputs" / "format_params.json").write_text(json.dumps(fp, indent=1))
    note("inputs/format_params.json", len(dropped))
    (DST / "inputs" / "measured").mkdir()
    for p in sorted((SRC / "inputs" / "measured").glob("*")):
        if p.is_file() and not NAME_RE.search(p.name) and not NAME_RE.search(p.read_text(errors="ignore")):
            shutil.copy(p, DST / "inputs" / "measured" / p.name)
        else:
            note(f"inputs/measured/{p.name}", 1)
    (DST / "inputs" / "baselines").mkdir()
    for p in sorted((SRC / "inputs" / "baselines").glob("*.csv")):
        rows = list(csv.reader(p.open()))
        keep = [rows[0]] + [r for r in rows[1:] if not NAME_RE.search(",".join(r))]
        buf = io.StringIO(); csv.writer(buf).writerows(keep)
        (DST / "inputs" / "baselines" / p.name).write_text(buf.getvalue())
        note(f"inputs/baselines/{p.name}", len(rows) - len(keep))
    prov = SRC / "inputs" / "baselines" / "provenance.json"
    if prov.exists():
        (DST / "inputs" / "baselines" / "provenance.json").write_text(
            json.dumps(scrub_json(json.loads(prov.read_text())), indent=1))

    # --- README
    lines = ["# idea01_lib — idea_01's library, redacted for idea_02 (built by utils/heldout/build_idea01_lib.py)", "",
             "Read-only reference. `ssb/` is importable (`sys.path.insert(0, 'inputs/idea01_lib')`). Everything that",
             "named or quantified a held-out study (validation / internal test) was removed at block level; the marker",
             "`[…redacted…]` shows where. Not copied at all: idea_01's OPEN.md, tools/, runs/, cards, inputs/derived,",
             "inputs/texts, inputs/adapters, and the notes files about held-out studies. Removed counts:", ""]
    lines += [f"- `{NAME_RE.sub('<held-out>', k)}`: {v} block(s)/row(s)/line(s)" for k, v in sorted(removed.items()) if v]
    (DST / "README.md").write_text("\n".join(lines) + "\n")

    # --- verify: zero hits or fail
    r = subprocess.run([sys.executable, str(SCAN), "--quiet", str(DST)], capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr)
    if r.returncode != 0:
        print(r.stdout)
        sys.exit("idea01_lib still names a held-out study — fix the redaction before mounting")
    print("idea01_lib built:", DST.relative_to(REPO))


if __name__ == "__main__":
    build()
