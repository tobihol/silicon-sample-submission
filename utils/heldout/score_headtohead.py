#!/usr/bin/env python3
"""Score a head-to-head fork submission (any carved task) — sections 1-2 and 3 only.

    uv run --with scipy utils/heldout/score_headtohead.py --fork <fork>/run --task bokemper2022 --n 1

Writes idea_02/eval/h2h/<task>_score_<n>.json (task-level metrics only), never into the fork.
Reuses score_daemon's scoring functions (which resolve truth via data/<task>/carved/).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("sd", REPO / "utils/heldout/score_daemon.py")
sd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sd)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fork", type=Path, required=True)
    ap.add_argument("--task", required=True)
    ap.add_argument("--n", type=int, required=True)
    a = ap.parse_args()
    subs = sorted(a.fork.resolve().glob(f"runs/*/h2h/{a.task}/submission_*.csv"))
    subs = [s for s in subs if re.fullmatch(r"submission_\d+\.csv", s.name)]
    if not subs:
        sys.exit(f"no submission under {a.fork}/runs/*/h2h/{a.task}/")
    sub = subs[0]
    out_dir = REPO / "idea_02" / "eval" / "h2h"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{a.task}_score_{a.n}.json"
    if out_path.exists():
        sys.exit(f"{out_path} exists")
    result = {"fork": str(a.fork), "task": a.task,
              "submission": str(sub.relative_to(a.fork.resolve())),
              "sha256": hashlib.sha256(sub.read_bytes()).hexdigest(),
              "n_submissions_found": len(list(sub.parent.glob("submission_*"))),
              "scored_at": sd.now(),
              "section_naming": sd.SECTION_NAMING,
              "sections": {"1": sd.score_sections_1_2(a.task, sub)}}
    for mp in sorted(sub.parent.glob("submission_1_mod_*.csv")):
        mod = mp.stem.replace("submission_1_mod_", "")
        result["sections"][f"2_{mod}"] = sd.score_section_3(a.task, mp, mod)
    out_path.write_text(json.dumps(result, indent=1))
    sd.log({"event": "h2h_scored", "task": a.task, "n": a.n, "sha256": result["sha256"]})
    print(f"head-to-head #{a.n} ({a.task}) scored -> {out_path} (sealed)")


if __name__ == "__main__":
    main()
