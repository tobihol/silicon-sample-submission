#!/usr/bin/env python3
"""Carve fresh-draw respondent-half truths for idea_03's validation tasks (host side).

idea_03's scoring oracle (`score_oracle3.py`) never scores against the full-sample truth:
every scored submission is evaluated against a *different* random half of the study's
respondents, so there is no fixed noise draw for the agent to hill-climb. This script
produces those halves, next to the existing full carve (which `carve_val.py` must have
written first):

    data/<task>/carved/halves/truth_h<seed>.csv    ATE cells from one random respondent-half
    data/<task>/carved/halves/index.json           seeds, sha256, per-half reliability

Halves are drawn respondent-level with numpy's default_rng(seed), seed in 0..N_HALVES-1,
within-arm balance left to chance (a half of n/2 keeps SEs interpretable; the oracle
reports r_adj, which corrects for exactly this noise). Reuses idea_01's adapters and
`ssb.task` unchanged, with carve_val.py's host path remap.

    uv run --with pyreadstat --with scipy utils/heldout/carve_halves.py            # all 7
    uv run --with pyreadstat --with scipy utils/heldout/carve_halves.py kim2024    # one
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
IDEA01_RUN = REPO / "idea_01" / "run"
SSB_SRC = IDEA01_RUN / ".prime" / "agent" / "skills" / "ssb" / "src"
DATA = REPO / "data"

VALIDATION = ["goldwert2026", "orchinik2024", "kim2024", "dablander2025",
              "altenmueller2024", "kerwer2025", "beall2017"]
N_HALVES = 16

os.environ.setdefault("SSB_BENCHMARK", str(REPO / "silicon-sample-submission-template"))
os.environ.setdefault("SSB_RUNROOT", str(IDEA01_RUN))
os.environ.setdefault("SSB_DATASETS", str(REPO / "data"))
sys.path.insert(0, str(SSB_SRC))
from ssb import task as T  # noqa: E402

PATHMAP = [("/workspace/datasets", str(REPO / "data")), ("/workspace/run", str(IDEA01_RUN))]


def host(p: str) -> str:
    for a, b in PATHMAP:
        if p.startswith(a):
            return b + p[len(a):]
    return p


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def carve_halves(name: str) -> dict:
    ad = T.load_adapter(name)
    ad["file"] = host(ad["file"])
    if "message_texts_file" in ad:
        ad["message_texts_file"] = host(ad["message_texts_file"])
    df = T.load_dataset(ad).reset_index(drop=True)

    sealed = DATA / name / "carved"
    if not (sealed / "truth.csv").exists():
        raise SystemExit(f"{name}: no full carve at {sealed} — run utils/heldout/carve_val.py first")
    out = sealed / "halves"
    out.mkdir(exist_ok=True)

    index = {"task": name, "n_rows_full": int(len(df)), "n_halves": N_HALVES, "halves": {}}
    for seed in range(N_HALVES):
        rng = np.random.default_rng(20260827 + seed)
        idx = rng.permutation(len(df))[: len(df) // 2]
        half = df.iloc[np.sort(idx)].reset_index(drop=True)
        t = T.true_ates(half, ad).dropna(subset=["ate"])
        p = out / f"truth_h{seed}.csv"
        t.to_csv(p, index=False)
        var = float(np.var(t.ate, ddof=1)) if len(t) > 2 else float("nan")
        ms = float(np.mean(np.square(t.se.to_numpy(float)))) if len(t) else float("nan")
        rel = 1.0 - ms / var if var and np.isfinite(var) and var > 0 else float("nan")
        index["halves"][str(seed)] = {"file": p.name, "sha256": sha(p), "n_cells": int(len(t)),
                                      "reliability": None if not np.isfinite(rel) else round(rel, 4)}
    (out / "index.json").write_text(json.dumps(index, indent=1))
    rels = [h["reliability"] for h in index["halves"].values() if h["reliability"] is not None]
    print(f"  {name:18s} {N_HALVES} halves, cells/half≈{index['halves']['0']['n_cells']}, "
          f"half-reliability median={np.median(rels):.3f}" if rels else f"  {name}: reliability n/a")
    return index


def main(argv):
    want = set(argv) or set(VALIDATION)
    for n in VALIDATION:
        if n in want:
            carve_halves(n)


if __name__ == "__main__":
    main(sys.argv[1:])
