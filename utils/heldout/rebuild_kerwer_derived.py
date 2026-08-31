#!/usr/bin/env python3
"""Rebuild idea_01/run/inputs/derived/kerwer2025.csv from data/kerwer2025/carved/microdata.csv.

The original derived file was disk-only (license scrub 2026-08-24: CC-BY-SA source) and never
committed. The carved microdata IS the loaded analysis frame (`_arm`, moderators, outcome
columns, in load order), so the derived file the adapter reads can be reconstructed by
inverting the adapter's loading transforms, all of which are invertible for this study:

  - arms mapping is the identity        -> arm_title = _arm
  - gender comes from quota_assignment  -> emit a representative code (Male->1, Female->2)
  - filters dispcode in (31,32), dropout == False -> constant passing values
  - no weight_col, outcomes read as-is  -> copy columns through

`ssb.task.load_dataset` on the result reproduces the microdata frame row-for-row (same
order), which is all `carve_halves.py` and the oracle need. Verified by the check below.

Run: uv run utils/heldout/rebuild_kerwer_derived.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
MICRO = REPO / "data" / "kerwer2025" / "carved" / "microdata.csv"
ADAPTER = REPO / "idea_01" / "run" / "inputs" / "adapters" / "kerwer2025.json"
OUT = REPO / "idea_01" / "run" / "inputs" / "derived" / "kerwer2025.csv"


def main() -> int:
    ad = json.loads(ADAPTER.read_text())
    assert ad.get("weight_col") is None
    assert all(k == v for k, v in ad["arms"].items()), "arms mapping not identity"
    micro = pd.read_csv(MICRO)

    df = micro.rename(columns={"_arm": ad["condition_col"]}).copy()
    gender_map = ad["moderators"]["gender"]["map"]          # code -> label
    label_to_code = {}
    for code, label in gender_map.items():                  # first code per label wins
        label_to_code.setdefault(label, code)
    df[ad["moderators"]["gender"]["col"]] = df.pop("gender").map(label_to_code)
    for f in ad["filters"]:
        df[f["col"]] = f["eq"] if "eq" in f else f["isin"][0]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)

    # round-trip check: load_dataset(adapter) must reproduce the microdata frame
    sys.path.insert(0, str(REPO / "idea_01/run/.prime/agent/skills/ssb/src"))
    from ssb import task as T  # noqa: E402
    ad2 = dict(ad, file=str(OUT))
    got = T.load_dataset(ad2).reset_index(drop=True)
    want = micro.reset_index(drop=True)
    if len(got) != len(want):
        sys.exit(f"round-trip row count {len(got)} != {len(want)}")
    for col in want.columns:
        a, b = got[col], want[col]
        if b.dtype.kind == "f":
            ok = ((a.isna() & b.isna()) | (a - b).abs().lt(1e-9)).all()
        else:
            ok = a.astype(str).where(a.notna()).equals(b.astype(str).where(b.notna()))
        if not ok:
            sys.exit(f"round-trip mismatch in column {col!r}")
    print(f"wrote {OUT.relative_to(REPO)} ({len(df)} rows); round-trip check ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
