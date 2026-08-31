#!/usr/bin/env python3
"""idea_03's mechanical promotion gate — operator-run, leave-one-study-out.

The agent proposes a technique by producing a CANDIDATE set of validation predictions; the
environment decides whether it generalizes. This script compares candidate vs baseline on
the FULL carved truths (which neither run ever saw scored), leave-one-study-out over the
promotion tasks, and writes back only a verdict + failure category — never per-study
scores. That is the whole design: nothing here needs to be (or should be) explained to the
agent beyond "the gate promotes what transfers".

    uv run --with scipy utils/heldout/loso_gate.py \
        --tree idea_03/run --candidate <run-id> --baseline <run-id> [--k 1] [--tag <name>]

Reads   <tree>/runs/<run-id>/val/<task>/submission_<k>.csv   for both run ids
Writes  <tree>/runs/<candidate>/gate_<tag>.json              agent-visible: verdict + category
        idea_03/eval/gate/<candidate>__<tag>.json            operator-only: full per-task detail

Verdict = PROMOTED iff (a) every leave-one-out fold's mean Δ(r_within) > 0 and (b) the
worst single-task Δ(r_within) > -NOISE. Δ is candidate minus baseline on identical cells.
Failure category names the outcome family of the worst task, not the task.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
EVAL = REPO / "idea_03" / "eval"
DATA = REPO / "data"

import os  # noqa: E402
SSB_SRC = REPO / "idea_01" / "run" / ".prime" / "agent" / "skills" / "ssb" / "src"
os.environ.setdefault("SSB_BENCHMARK", str(REPO / "silicon-sample-submission-template"))
os.environ.setdefault("SSB_RUNROOT", str(REPO / "idea_01" / "run"))
sys.path.insert(0, str(SSB_SRC))
from ssb import score as S  # noqa: E402

PROMOTION_TASKS = ["goldwert2026", "kim2024", "dablander2025", "altenmueller2024", "beall2017"]
NOISE = 0.10  # a single-task Δ(r_within) below -0.10 is "hurts one study beyond noise"

FAMILY = {"goldwert2026": "donation/behavioral outcomes",
          "kim2024": "trust-in-scientists (Likert)",
          "dablander2025": "trust-in-scientists (vignette nulls)",
          "altenmueller2024": "trust-in-scientists (METI)",
          "beall2017": "scientist credibility (framings)"}


def r_within(task: str, sub: Path) -> float | None:
    truth = pd.read_csv(DATA / task / "carved" / "truth.csv")
    pred = pd.read_csv(sub)
    if not {"condition", "outcome", "ate"} <= set(pred.columns):
        return None
    pred = pred[["condition", "outcome", "ate"]].rename(columns={"ate": "pred"})
    d = truth.merge(pred, on=["condition", "outcome"], how="left").rename(columns={"ate": "human"})
    d["pred"] = pd.to_numeric(d.pred, errors="coerce").fillna(0.0)
    v = S.pearson_r_within_outcomes(d)
    return None if not np.isfinite(v) else float(v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", type=Path, default=REPO / "idea_03" / "run")
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--k", type=int, default=1, help="which submission_<k> to compare (default 1)")
    ap.add_argument("--tag", default="verdict", help="name for this gate decision")
    a = ap.parse_args()

    deltas, detail, missing = {}, {}, []
    for task in PROMOTION_TASKS:
        cs = a.tree / "runs" / a.candidate / "val" / task / f"submission_{a.k}.csv"
        bs = a.tree / "runs" / a.baseline / "val" / task / f"submission_{a.k}.csv"
        if not cs.exists() or not bs.exists():
            missing.append(task)
            continue
        rc, rb = r_within(task, cs), r_within(task, bs)
        if rc is None or rb is None:
            missing.append(task)
            continue
        deltas[task] = rc - rb
        detail[task] = {"candidate_r_within": rc, "baseline_r_within": rb, "delta": rc - rb}
    if len(deltas) < 3:
        sys.exit(f"gate needs >= 3 promotion tasks on both sides; have {len(deltas)} (missing: {missing})")

    tasks = list(deltas)
    folds = {t: float(np.mean([deltas[u] for u in tasks if u != t])) for t in tasks}
    worst_task = min(deltas, key=deltas.get)
    promoted = all(v > 0 for v in folds.values()) and deltas[worst_task] > -NOISE
    category = None if promoted else FAMILY.get(worst_task, "unknown family")

    agent_visible = {"tag": a.tag, "candidate": a.candidate, "baseline": a.baseline,
                     "verdict": "PROMOTED" if promoted else "REJECTED",
                     "failure_category": category,
                     "decided_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    out_agent = a.tree / "runs" / a.candidate / f"gate_{a.tag}.json"
    out_agent.write_text(json.dumps(agent_visible, indent=1))

    gd = EVAL / "gate"
    gd.mkdir(parents=True, exist_ok=True)
    (gd / f"{a.candidate}__{a.tag}.json").write_text(json.dumps(
        {**agent_visible, "detail": detail, "loso_fold_means": folds,
         "worst_task": worst_task, "noise_threshold": NOISE, "missing_tasks": missing}, indent=1))
    print(f"{agent_visible['verdict']}"
          + (f" (failure category: {category})" if category else "")
          + f" -> {out_agent}  [operator detail: idea_03/eval/gate/]")


if __name__ == "__main__":
    main()
