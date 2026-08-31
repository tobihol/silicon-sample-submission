#!/usr/bin/env python3
"""Carve idea_02's validation and internal-test tasks (host side, never mounted).

For each held-out study this writes, next to the raw data it came from (disk-only, gitignored
like downloads/, and absent from idea_02's mount because the whole dataset directory is
excluded there — see idea_02/launch.env):

    data/<task>/carved/truth.csv                 marginal ATE cells (condition, outcome, ate, se, n)
    data/<task>/carved/truth_mod_<m>.csv         one per moderator the adapter maps (Section 3)
    data/<task>/carved/attrition_bounds.csv      where the adapter declares Lee bounds
    data/<task>/carved/microdata.csv             loaded analysis rows: _arm, moderators, outcomes (Section 4)
    data/<task>/carved/manifest.json             sha256 of every carved file, adapter provenance
    <brief-root>/<task>/brief/task.json          DESIGN ONLY: sample, arms + verbatim texts, outcomes,
                                                 n per arm, moderators + levels, sections scoreable
    <brief-root>/<task>/brief/template.csv       condition, outcome, ate (blank)
    <brief-root>/<task>/brief/template_mod_<m>.csv  condition, moderator_level, outcome, ate (blank)

Validation briefs go to idea_02/run/inputs/val/ (mounted with the run tree). The internal-test
brief goes to data/bbprime2025/carved/brief/ and is copied ONLY into evaluation forks by
utils/prime/fork_eval.sh — the main branch never sees it. An index of what was carved is
written to idea_02/eval/carved_index.json.

The brief is checked before it is written: none of the sealed truth values (2 dp) may appear
in it, and no key outside the design whitelist is allowed. Reuses idea_01's adapters and
`ssb.task` unchanged; container paths are remapped to host paths.

    uv run --with pyreadstat --with scipy utils/heldout/carve_val.py            # all eight
    uv run --with pyreadstat --with scipy utils/heldout/carve_val.py kim2024    # one
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
IDEA01_RUN = REPO / "idea_01" / "run"
SSB_SRC = IDEA01_RUN / ".prime" / "agent" / "skills" / "ssb" / "src"
DATA = REPO / "data"
VAL_BRIEFS = REPO / "idea_02" / "run" / "inputs" / "val"
EVAL = REPO / "idea_02" / "eval"

VALIDATION = ["goldwert2026", "orchinik2024", "kim2024", "dablander2025",
              "altenmueller2024", "kerwer2025", "beall2017"]
INTERNAL_TEST = ["bbprime2025"]

# Only these keys may appear in a brief. Everything else in an adapter (caveats that quote
# effect sizes, calibration families, harness notes) stays on the host.
BRIEF_KEYS = {"task_id", "study", "split", "sample", "n_total", "n_by_arm", "control_arms",
              "arms", "control_texts", "outcomes", "moderators", "sections", "instruction",
              "submission_files"}

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


def carve_one(name: str, split: str) -> dict:
    ad = T.load_adapter(name)
    ad["file"] = host(ad["file"])
    if "message_texts_file" in ad:
        ad["message_texts_file"] = host(ad["message_texts_file"])
    df = T.load_dataset(ad)

    sealed = DATA / name / "carved"
    if sealed.exists():
        shutil.rmtree(sealed)
    sealed.mkdir(parents=True)
    if split == "validation":
        if (VAL_BRIEFS / name).exists():
            shutil.rmtree(VAL_BRIEFS / name)
        brief_dir = VAL_BRIEFS / name / "brief"
    else:
        brief_dir = sealed / "brief"     # internal test: stays beside the truth, forks copy it
    brief_dir.mkdir(parents=True)

    # --- sealed: marginal truth via ssb.task.carve (into a temp dir), then moderators
    with tempfile.TemporaryDirectory() as tmp:
        # carve() reads the adapter by name again; hand it the host-remapped copy instead.
        orig = T.load_adapter
        T.load_adapter = lambda n, _ad=ad: _ad  # noqa: E731
        try:
            man = T.carve(name, Path(tmp) / name)
        finally:
            T.load_adapter = orig
        for f in ("truth.csv", "attrition_bounds.csv"):
            src = Path(tmp) / name / "sealed" / f
            if src.exists():
                shutil.copy(src, sealed / f)
        base_brief = json.loads((Path(tmp) / name / "brief" / "task.json").read_text())
        shutil.copy(Path(tmp) / name / "brief" / "template.csv", brief_dir / "template.csv")

    moderators = {}
    for m in ad.get("moderators", {}):
        try:
            tm = T.true_ates(df, ad, moderator=m)
        except Exception as e:  # noqa: BLE001  (goldwert education: thin cells -> NaN cast)
            print(f"  [{name}] moderator {m}: not carved ({e.__class__.__name__}: {e})")
            continue
        tm = tm.dropna(subset=["ate"])
        if tm.empty:
            continue
        tm.to_csv(sealed / f"truth_mod_{m}.csv", index=False)
        levels = sorted(str(x) for x in tm.moderator_level.unique())
        moderators[m] = levels
        tmpl = tm[["condition", "moderator_level", "outcome"]].drop_duplicates().assign(ate="")
        tmpl.to_csv(brief_dir / f"template_mod_{m}.csv", index=False)

    # microdata for Section 4 (native units; only what the scorer needs)
    cols = ["_arm"] + list(ad.get("moderators", {}).keys()) + [o["col"] for o in ad["outcomes"].values()]
    cols = [c for c in dict.fromkeys(cols) if c in df.columns]
    df[cols].to_csv(sealed / "microdata.csv", index=False)
    json.dump({"outcomes": {k: {"col": v["col"], "lo": v["lo"], "hi": v["hi"],
                                "reverse": bool(v.get("reverse", False))} for k, v in ad["outcomes"].items()},
               "control_arms": ad["control_arms"], "weight_col": ad.get("weight_col")},
              open(sealed / "adapter_scoring.json", "w"), indent=1)

    # --- brief: design only
    sections = ["1", "2"] + (["3"] if moderators else []) + ["4"]
    brief = {k: v for k, v in base_brief.items() if k in BRIEF_KEYS}
    brief.update({
        "split": split,
        "moderators": moderators,
        "sections": sections,
        "submission_files": {
            "submission_<k>.csv": "required - template.csv filled (Sections 1-2)",
            **{f"submission_<k>_mod_{m}.csv": f"optional - template_mod_{m}.csv filled (Section 3)" for m in moderators},
            "submission_<k>_rows.csv": "optional - synthetic rows: condition, <outcome columns in native units>"
                                        ", <moderator columns> (Section 4: variance ratio, OVL, KS, W1 per cell)",
        },
        "instruction": (base_brief["instruction"] + " Optional files score the other sections; "
                        "the scorer returns task-level metrics only. At most 5 submissions per task per session."),
    })
    brief.pop("moderator", None)
    assert set(brief) <= BRIEF_KEYS, set(brief) - BRIEF_KEYS

    # leak check: no sealed truth value (2 dp) may appear in the brief text
    import pandas as pd
    truth = pd.read_csv(sealed / "truth.csv")
    vals = {f"{v:.2f}" for v in truth.ate.dropna() if abs(v) > 0.05}
    text = json.dumps(brief, ensure_ascii=False)
    nums = {f"{float(x):.2f}" for x in re.findall(r"-?\d+\.\d+", text)}
    echoed = nums & vals
    # a handful of chance collisions with scale bounds is possible; anything more is a leak
    assert len(echoed) <= 2, f"{name}: brief echoes {len(echoed)} truth values: {sorted(echoed)[:5]}"
    bad = re.search(r"\bATEs?\b|\beffect sizes?\b|\bLee bounds?\b|\bcalibrat|\bpp\b|\bslope\b",
                    brief["sample"], flags=re.IGNORECASE)
    assert not bad, f"{name}: sample_description mentions {bad.group(0)!r}"
    (brief_dir / "task.json").write_text(json.dumps(brief, indent=1, ensure_ascii=False))

    files = {p.name: sha(p) for p in sorted(sealed.iterdir()) if p.is_file()}
    manifest = {"task_id": name, "split": split, "adapter": name, "n_cells": man["n_cells"],
                "n_rows": int(len(df)), "moderators": list(moderators),
                "attrition": man.get("attrition"), "provenance": ad.get("provenance", {}),
                "sealed_sha256": files, "brief_sha256": {p.name: sha(p) for p in sorted(brief_dir.iterdir())}}
    (sealed / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"  {name:18s} {split:13s} cells={man['n_cells']:4d} rows={len(df):6d} "
          f"moderators={list(moderators)} brief={brief_dir.relative_to(REPO)}")
    return manifest


def main(argv):
    want = set(argv) or set(VALIDATION + INTERNAL_TEST)
    EVAL.mkdir(parents=True, exist_ok=True)
    out = {}
    for n in VALIDATION:
        if n in want:
            out[n] = carve_one(n, "validation")
    for n in INTERNAL_TEST:
        if n in want:
            out[n] = carve_one(n, "internal_test")
    idx = EVAL / "carved_index.json"
    prev = json.loads(idx.read_text()) if idx.exists() else {}
    prev.update({k: {"split": v["split"], "n_cells": v["n_cells"], "truth_sha256": v["sealed_sha256"]["truth.csv"]}
                 for k, v in out.items()})
    idx.write_text(json.dumps(prev, indent=1))


if __name__ == "__main__":
    main(sys.argv[1:])
