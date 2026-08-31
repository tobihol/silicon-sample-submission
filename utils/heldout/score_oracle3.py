#!/usr/bin/env python3
"""idea_03's scoring oracle — host side, outside every mount set.

The environment-design successor to idea_02's `score_daemon.py`, implementing the three
incentive fixes from `docs/idea03-brainstorm-2026-08-27.md` §3:

1. FRESH-DRAW TRUTH. A submission is never scored against the full-sample truth: each
   scored call is evaluated against one of the pre-carved respondent-halves
   (`data/<task>/carved/halves/`, from `carve_halves.py`), chosen deterministically from
   (run_id, task, k). There is no fixed noise draw to hill-climb.
2. HARD SUBMISSION BUDGET. At most CAP=2 scored submissions per (run-id, task); further
   submissions get a `refused_<k>.json`. Not a rule for the agent — a scorer that refuses.
3. DIAGNOSTICS, NOT SCORES. `score_<k>.json` carries r_adj / r_within_adj (attenuation-
   corrected), directional agreement, calibration alpha/beta, spread ratio and mean signed
   error — pooled statistics that name the failure type. Raw r / r-within / RMSE on the
   half are never returned. The full-truth scorecard is written to idea_03/eval/full/
   for the OPERATOR only.

Watches:  <run-tree>/runs/<run-id>/val/<task>/submission_<k>.csv
Writes:   <run-tree>/runs/<run-id>/val/<task>/score_<k>.json    (agent-visible diagnostics)
          idea_03/eval/full/<run-id>__<task>__<k>.json           (operator-only, full truth)
          idea_03/eval/log.jsonl                                 (append-only event log)

Tasks in DIAGNOSTIC_TASKS (split-half reliability < ~0.6: orchinik2024 .28, kerwer2025 .21)
are scored the same but marked `counts_toward_promotion: false` in the score file.

Internal test (`--itest <fork-run-tree> --n <i> [--task bbprime2025]`): scores the fork's
first submission against the FULL carved truth with idea_02's frozen section scorers
(imported from score_daemon.py — identical metrics, official section keys), writes ONLY to
idea_03/eval/itest/score_<i>.json, and exits. Sealed until the campaign ends.

    uv run --with scipy utils/heldout/score_oracle3.py idea_03/run          # watch forever
    uv run --with scipy utils/heldout/score_oracle3.py idea_03/run --once
    uv run --with scipy utils/heldout/score_oracle3.py --itest <fork>/run --n 1
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
EVAL = REPO / "idea_03" / "eval"
DATA = REPO / "data"

SSB_SRC = REPO / "idea_01" / "run" / ".prime" / "agent" / "skills" / "ssb" / "src"
os.environ.setdefault("SSB_BENCHMARK", str(REPO / "silicon-sample-submission-template"))
os.environ.setdefault("SSB_RUNROOT", str(REPO / "idea_01" / "run"))
sys.path.insert(0, str(SSB_SRC))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ssb import score as S  # noqa: E402

CAP = 2
N_HALVES = 16
LOG = EVAL / "log.jsonl"

VAL_TASKS = {"goldwert2026", "orchinik2024", "kim2024", "dablander2025",
             "altenmueller2024", "kerwer2025", "beall2017"}
# Split-half reliability of the full-sample truth (docs/idea03-brainstorm §2): tasks below
# the ~0.6 gate feed diagnostics, never promotion.
DIAGNOSTIC_TASKS = {"orchinik2024", "kerwer2025"}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def log(event: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps({"at": now(), **event}) + "\n")


def _finite(d: dict) -> dict:
    return {k: (None if isinstance(v, float) and not np.isfinite(v) else v) for k, v in d.items()}


def pick_half(run_id: str, task: str, k: int) -> int:
    """Deterministic, and DISTINCT across k for the same (run_id, task): the k-th scored
    call takes the k-th entry of a permutation of all halves seeded by (run_id, task).
    Re-running the daemon reproduces the same score for the same file.

    2026-08-27 (session-1 OPEN.md A3): the previous per-k hash could collide — kerwer2025
    drew half 5 on both scored calls of run 20260827T194235Z_s1, violating the frozen
    "different respondent-half per scored call" promise. Sampling without replacement
    makes the promise structural. Already-written score_<k>.json files are unaffected."""
    h = int(hashlib.sha256(f"{run_id}/{task}".encode()).hexdigest(), 16)
    order = np.random.default_rng(h % (2**63)).permutation(N_HALVES)
    return int(order[(k - 1) % N_HALVES])


def _merge(truth: pd.DataFrame, sub: Path) -> tuple[pd.DataFrame, int] | dict:
    pred = pd.read_csv(sub)
    for c in ("condition", "outcome", "ate"):
        if c not in pred.columns:
            return {"error": f"missing column {c!r}"}
    pred = pred[["condition", "outcome", "ate"]].rename(columns={"ate": "pred"})
    d = truth.merge(pred, on=["condition", "outcome"], how="left")
    d = d.rename(columns={"ate": "human", "se": "se_human"})
    n_missing = int(d.pred.isna().sum())
    d["pred"] = pd.to_numeric(d.pred, errors="coerce").fillna(0.0)
    return d, n_missing


def diagnostics(task: str, sub: Path, half_seed: int) -> dict:
    """What the agent sees: attenuation-corrected skill + failure-type statistics,
    computed on one fresh respondent-half. Never raw r / r-within / RMSE."""
    hp = DATA / task / "carved" / "halves" / f"truth_h{half_seed}.csv"
    if not hp.exists():
        return {"error": f"no halves for {task} — operator must run carve_halves.py"}
    m = _merge(pd.read_csv(hp), sub)
    if isinstance(m, dict):
        return m
    d, n_missing = m
    dis = S.disattenuated(d.pred, d.human, d.se_human)
    rel = dis["reliability"]
    rw = S.pearson_r_within_outcomes(d)
    # 2026-08-27 (session-1 OPEN.md A4): with reliability ~ 0 the attenuation correction is
    # undefined; the organizers' adjusted_metrics() returns NA there and truncates to
    # [-1, 1]. Match that instead of emitting +/-thousands (orchinik2024 printed -16817).
    rel_ok = bool(np.isfinite(rel) and rel > 1e-3)

    def _adj(x: float) -> float | None:
        return float(np.clip(x, -1.0, 1.0)) if rel_ok and np.isfinite(x) else None

    rw_adj = _adj(rw / np.sqrt(rel)) if np.isfinite(rw) and rel_ok else None
    cal = S.calibration(d.pred, d.human)
    sd_h = float(np.std(d.human, ddof=1))
    out = {
        "n_cells": int(len(d)), "n_cells_missing_scored_as_zero": n_missing,
        "r_adj": _adj(dis["r_adj"]), "r_within_adj": rw_adj, "rmse_adj_pp": dis["rmse_adj"],
        "truth_half_reliability": rel,
        "directional_agreement": S.directional_agreement(d.pred, d.human),
        **{f"cal_{k}": v for k, v in cal.items()},
        "spread_ratio": float(np.std(d.pred, ddof=1) / sd_h) if sd_h > 0 else float("nan"),
        "mean_signed_error_pp": float(np.mean(d.pred - d.human)),
    }
    return _finite(out)


def full_record(task: str, sub: Path) -> dict:
    """Operator-only: the frozen full-truth scorecard, for the record and the LOSO gate."""
    m = _merge(pd.read_csv(DATA / task / "carved" / "truth.csv"), sub)
    if isinstance(m, dict):
        return m
    d, n_missing = m
    out = S.scorecard(d)
    out["n_cells_missing_scored_as_zero"] = n_missing
    return _finite(out)


SUB_RE = re.compile(r"^submission_(\d+)\.csv$")


def pass_once(run_tree: Path) -> int:
    n = 0
    for sub in sorted(run_tree.glob("runs/*/val/*/submission_*.csv")):
        m = SUB_RE.match(sub.name)
        if not m:
            continue
        k = int(m.group(1))
        task_dir = sub.parent
        task, run_id = task_dir.name, task_dir.parent.parent.name
        if task not in VAL_TASKS:
            continue
        score_path = task_dir / f"score_{k}.json"
        refused_path = task_dir / f"refused_{k}.json"
        if score_path.exists() or refused_path.exists():
            continue
        digest = sha(sub)
        scored = len(list(task_dir.glob("score_*.json")))
        if scored >= CAP:
            refused_path.write_text(json.dumps(
                {"submission": k, "reason": f"budget of {CAP} scored submissions per task reached",
                 "sha256": digest, "at": now()}, indent=1))
            log({"event": "refused", "run_id": run_id, "task": task, "k": k, "sha256": digest})
            print(f"refused {run_id}/{task}/{k} (budget {CAP})")
            n += 1
            continue
        half = pick_half(run_id, task, k)
        diag = diagnostics(task, sub, half)
        result = {"task": task, "submission": k, "sha256": digest, "scored_at": now(),
                  "counts_toward_promotion": task not in DIAGNOSTIC_TASKS,
                  "truth": "one fresh respondent-half per scored call (no fixed draw exists)",
                  "diagnostics": diag,
                  "submissions_used": scored + 1, "submissions_budget": CAP}
        tmp = score_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(result, indent=1))
        os.replace(tmp, score_path)
        # operator-only full record (unmounted): full truth + which half the agent saw
        fr = {"run_id": run_id, "task": task, "k": k, "sha256": digest, "half_seed": half,
              "scored_at": now(), "full_truth_scorecard": full_record(task, sub),
              "agent_visible_diagnostics": diag}
        fdir = EVAL / "full"
        fdir.mkdir(parents=True, exist_ok=True)
        (fdir / f"{run_id}__{task}__{k}.json").write_text(json.dumps(fr, indent=1))
        log({"event": "scored", "run_id": run_id, "task": task, "k": k, "half_seed": half,
             "sha256": digest, "summary": {kk: diag.get(kk) for kk in
                                           ("r_adj", "r_within_adj", "cal_beta", "directional_agreement", "error")}})
        print(f"scored {run_id}/{task}/{k} on half {half}: r_adj={diag.get('r_adj')} "
              f"r_within_adj={diag.get('r_within_adj')} beta={diag.get('cal_beta')} ({scored + 1}/{CAP})")
        n += 1
    return n


def score_itest(fork_tree: Path, n: int, task: str) -> None:
    import score_daemon as D2  # idea_02's frozen section scorers, reused verbatim
    subs = sorted(fork_tree.glob(f"runs/*/itest/{task}/submission_*.csv"))
    out_dir = EVAL / "itest"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"score_{n}.json"
    if out.exists():
        sys.exit(f"{out} exists — an internal-test score is written once; choose another --n")
    if not subs:
        sys.exit(f"no submission under {fork_tree}/runs/*/itest/{task}/")
    sub = subs[0]  # the first submission is the one that counts
    result = {"fork": str(fork_tree), "task": task, "submission": str(sub.relative_to(fork_tree)),
              "sha256": sha(sub), "n_submissions_found": len(subs), "scored_at": now(),
              "section_naming": D2.SECTION_NAMING,
              "sections": {"1": D2.score_sections_1_2(task, sub)}}
    for mp in sorted(sub.parent.glob(sub.stem + "_mod_*.csv")):
        mod = mp.name[len(sub.stem + "_mod_"):-4]
        result["sections"][f"2_{mod}"] = D2.score_section_3(task, mp, mod)
    rp = sub.parent / (sub.stem + "_rows.csv")
    if rp.exists():
        result["sections"]["3a"] = D2.score_section_4(task, rp)
    out.write_text(json.dumps(result, indent=1))
    log({"event": "itest_scored", "n": n, "task": task, "fork": str(fork_tree), "sha256": result["sha256"]})
    print(f"internal test #{n} ({task}) scored -> {out} (sealed; do not open before the campaign ends)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_trees", nargs="*", type=Path, help="idea_03 run trees to watch (e.g. idea_03/run)")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--interval", type=float, default=5.0)
    ap.add_argument("--itest", type=Path, help="score an evaluation fork's internal-test submission and exit")
    ap.add_argument("--n", type=int, help="internal-test iteration number (with --itest)")
    ap.add_argument("--task", default="bbprime2025", help="internal-test task id (with --itest)")
    a = ap.parse_args()
    if a.itest:
        if a.n is None:
            sys.exit("--n required with --itest")
        score_itest(a.itest.resolve(), a.n, a.task)
        return
    trees = [t.resolve() for t in a.run_trees] or [REPO / "idea_03" / "run"]
    log({"event": "daemon_start", "trees": [str(t) for t in trees], "cap": CAP, "n_halves": N_HALVES})
    while True:
        for t in trees:
            try:
                pass_once(t)
            except Exception as e:  # noqa: BLE001 — a scorer crash must not take the daemon down
                log({"event": "error", "tree": str(t), "error": repr(e)})
                print("error:", repr(e), file=sys.stderr)
        if a.once:
            break
        time.sleep(a.interval)


if __name__ == "__main__":
    main()
