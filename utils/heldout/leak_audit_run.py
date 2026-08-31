#!/usr/bin/env python3
"""Post-run leak audit for idea_02: did any transcript or run-tree file see sealed truth?

Runs idea_01's `ssb.task.leak_audit` (sealed path/sha/value-echo probes with a shift-null)
for every sealed task against (a) every Prime session transcript in the arm state and
(b) every text file in the run tree except the agent's own submissions and the scorer's
score files. Also greps for the eight held-out names in transcripts (a validation study's
name is expected — its brief names it — so names are reported, not failed; numbers are what
fail). Writes idea_02/eval/audits/<timestamp>.json and exits 1 on any LEAK verdict.

    uv run --with scipy utils/heldout/leak_audit_run.py --prime .container-state/arms/idea_02/main/prime --run idea_02/run
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EVAL = REPO / "idea_02" / "eval"
sys.path.insert(0, str(REPO / "idea_01" / "run" / ".prime" / "agent" / "skills" / "ssb" / "src"))
os.environ.setdefault("SSB_BENCHMARK", str(REPO / "silicon-sample-submission-template"))
os.environ.setdefault("SSB_RUNROOT", str(REPO / "idea_01" / "run"))
from ssb import task as T  # noqa: E402

TEXT_SUFFIXES = {".jsonl", ".json", ".md", ".txt", ".csv", ".py", ".log", ".yaml", ".toml"}


def collect(prime: Path, run: Path) -> list[Path]:
    files = []
    for base in (prime / "sessions", prime / "session-artifacts", prime / "logs"):
        if base.exists():
            files += [p for p in base.rglob("*") if p.is_file() and p.suffix in TEXT_SUFFIXES]
    for p in run.rglob("*"):
        if not p.is_file() or p.suffix not in TEXT_SUFFIXES or "__pycache__" in p.parts:
            continue
        if p.name.startswith(("submission_", "score_", "refused_")):
            continue  # the agent's own predictions and the scorer's task-level feedback
        files.append(p)
    return files


def main():
    global EVAL
    ap = argparse.ArgumentParser()
    ap.add_argument("--prime", type=Path, required=True)
    ap.add_argument("--run", type=Path, required=True)
    ap.add_argument("--exclude", default="", help="comma list of tasks to skip — the fork "
                    "LEGITIMATELY holds the internal-test task, so exclude it when auditing a fork")
    ap.add_argument("--eval", type=Path, default=EVAL, help="where audits/ is written (default idea_02/eval)")
    a = ap.parse_args()
    EVAL = a.eval.resolve()
    skip = {s for s in a.exclude.split(",") if s}
    files = collect(a.prime.resolve(), a.run.resolve())
    results, worst = {}, "CLEAN"
    carved_dirs = sorted(p for p in (REPO / "data").glob("*/carved") if (p / "truth.csv").exists())
    # idea_04's arm-level folds: data/<study>/carved_arms/<fold>/truth.csv -> task <study>_arms[_sealed]
    arm_dirs = sorted(p for p in (REPO / "data").glob("*/carved_arms/*") if (p / "truth.csv").exists())
    for task_dir in carved_dirs + arm_dirs:
        if task_dir.parent.name == "carved_arms":
            study = task_dir.parent.parent.name
            name = f"{study}_arms" + ("" if task_dir.name == "val" else f"_{task_dir.name}")
        else:
            task_dir = task_dir.parent / task_dir.name  # data/<task>/carved
            name = task_dir.parent.name
        if name in skip:
            continue
        # leak_audit expects task_dir/sealed/{truth.csv,manifest.json}
        with tempfile.TemporaryDirectory() as tmp:
            td = Path(tmp) / name
            (td / "sealed").mkdir(parents=True)
            # Probe against ALL truth values — the marginal cells AND every moderator
            # interaction cell (session-1 D2: the leaked value was a subgroup contrast, which
            # is absent from truth.csv). Concatenate their `ate` columns into one truth file.
            import pandas as pd
            frames = [pd.read_csv(task_dir / "truth.csv")[["condition", "outcome", "ate"]]]
            for mp in task_dir.glob("truth_mod_*.csv"):
                m = pd.read_csv(mp)
                m["outcome"] = m["outcome"].astype(str) + "@" + m["moderator_level"].astype(str)
                frames.append(m[["condition", "outcome", "ate"]])
            pd.concat(frames, ignore_index=True).to_csv(td / "sealed" / "truth.csv", index=False)
            man = json.loads((task_dir / "manifest.json").read_text())
            (td / "sealed" / "manifest.json").write_text(json.dumps(
                {"truth_sha256": man["sealed_sha256"]["truth.csv"], "task_id": name}))
            r = T.leak_audit(td, [str(f) for f in files])
        # ssb's path probe is `"sealed" in blob and task in blob` over the concatenation of
        # every file, which is trivially true here (the run tree names each task in its brief
        # and the library's docstrings say "sealed"). Replace it with a per-file probe for
        # the actual held-out location, and re-derive the verdict with ssb's own thresholds.
        study = name.split("_arms")[0]
        needles = (f"data/{study}/carved", f"{study}/carved", f"{study}/truth", f"{study}/microdata",
                   "idea_02/eval/itest", "idea_03/eval/itest", "idea_04/eval/itest")
        hits = [str(f) for f in files if any(n in f.read_text(errors="ignore") for n in needles)]
        r["path_mentioned"] = bool(hits)
        r["path_files"] = hits[:10]
        excess, z = r["echo_excess"], r["echo_excess_z"]
        r["verdict"] = "LEAK" if (r["sha_mentioned"] or excess > 0.25 or z > 8) else (
            "SUSPECT" if r["path_mentioned"] or z > 4 or excess > 0.10 else "CLEAN")
        results[name] = r
        rank = {"CLEAN": 0, "SUSPECT": 1, "LEAK": 2}
        if rank[r["verdict"]] > rank[worst]:
            worst = r["verdict"]
        print(f"{name:18s} {r['verdict']:8s} echo={r['echo_rate']:.2f} null={r['echo_rate_null']:.2f} "
              f"z={r['echo_excess_z']:.1f} path={r['path_mentioned']} sha={r['sha_mentioned']}")
    out_dir = EVAL / "audits"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (out_dir / f"{stamp}.json").write_text(json.dumps({"prime": str(a.prime), "run": str(a.run),
                                                       "n_files": len(files), "worst": worst,
                                                       "results": results}, indent=1))
    print(f"{len(files)} files audited; worst verdict {worst}; record {out_dir}/{stamp}.json")
    sys.exit(0 if worst != "LEAK" else 1)


if __name__ == "__main__":
    main()
