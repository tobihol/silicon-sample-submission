#!/usr/bin/env python3
"""One row per idea_02 iteration: validation aggregate, internal-test score, rlm/refine usage.

Reads what each iteration leaves on disk and appends a line to idea_02/eval/campaign.csv:

  iter, run_id, val_r_within_mean, val_dir_mean, val_rmse_mean, n_val_tasks,
  itest_r, itest_r_within, itest_dir, itest_rmse, itest_beta,
  rlm_children, refinements_total, ledger_entries, notes

- validation aggregate: mean of the BEST submission per task from runs/<run-id>/val/*/score_*.json
- internal test: idea_02/eval/itest/score_<iter>.json (bbprime, if the fork for this iter ran)
- rlm_children: distinct rlm child ids in the session exec log (idea_02/eval/<run-id>_exec.log)
- refinements_total / ledger_entries: from the promoted arm ledger

    uv run --with scipy utils/heldout/track_campaign.py <iter> <run-id> [--note "..."]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import statistics as st
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EVAL = REPO / "idea_02" / "eval"
RUNS = REPO / "idea_02" / "run" / "runs"
LEDGER = REPO / ".container-state" / "arms" / "idea_02" / "main" / "prime" / "harness"
OUT = EVAL / "campaign.csv"
COLS = ["iter", "run_id", "val_r_within_mean", "val_dir_mean", "val_rmse_mean", "n_val_tasks",
        "itest_r", "itest_r_within", "itest_dir", "itest_rmse", "itest_beta",
        "rlm_children", "refinements_total", "ledger_entries", "note"]


def best_val(run_id: str):
    """Mean over tasks of each task's best submission (max r_within, tie-break min rmse)."""
    rows = []
    for task_dir in sorted((RUNS / run_id / "val").glob("*")) if (RUNS / run_id / "val").is_dir() else []:
        best = None
        for sp in task_dir.glob("score_*.json"):
            s = json.loads(sp.read_text())["sections"].get("1_2", {})
            rw = s.get("pearson_r_within_outcomes")
            if rw is None:
                continue
            key = (rw, -(s.get("rmse_pp") or 0))
            if best is None or key > best[0]:
                best = (key, s)
        if best:
            rows.append(best[1])
    if not rows:
        return {}
    return {"val_r_within_mean": round(st.mean(r["pearson_r_within_outcomes"] for r in rows), 4),
            "val_dir_mean": round(st.mean(r["directional_agreement"] for r in rows), 4),
            "val_rmse_mean": round(st.mean(r["rmse_pp"] for r in rows), 4),
            "n_val_tasks": len(rows)}


def itest(iter_n: int):
    p = EVAL / "itest" / f"score_{iter_n}.json"
    if not p.exists():
        return {}
    secs = json.loads(p.read_text())["sections"]
    s = secs.get("1") or secs.get("1_2") or {}  # official key since 2026-08-26; legacy fallback
    return {"itest_r": s.get("pearson_r"), "itest_r_within": s.get("pearson_r_within_outcomes"),
            "itest_dir": s.get("directional_agreement"), "itest_rmse": s.get("rmse_pp"),
            "itest_beta": s.get("cal_beta")}


def usage(run_id: str):
    out = {}
    log = EVAL / f"{run_id}_exec.log"
    if log.exists():
        txt = log.read_text(errors="ignore")
        out["rlm_children"] = len(set(re.findall(r'"child":\{"id":"([^"]+)"', txt)))
    hs = LEDGER / "harness_state.json"
    if hs.exists():
        d = json.loads(hs.read_text())
        out["refinements_total"] = len(d.get("refinements", []))
        out["ledger_entries"] = sum(len(v) for v in d.get("entries", {}).values())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("iter", type=int)
    ap.add_argument("run_id")
    ap.add_argument("--note", default="")
    a = ap.parse_args()
    row = {"iter": a.iter, "run_id": a.run_id, "note": a.note,
           **best_val(a.run_id), **itest(a.iter), **usage(a.run_id)}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    new = not OUT.exists()
    with OUT.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        if new:
            w.writeheader()
        w.writerow({c: row.get(c, "") for c in COLS})
    print(json.dumps(row, indent=1))


if __name__ == "__main__":
    main()
