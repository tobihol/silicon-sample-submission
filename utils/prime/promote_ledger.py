#!/usr/bin/env python3
"""Promote a session's local Prime Agent harness ledger to the arm's global ledger.

Why this exists (checked against prime-agent 0.7.2 source, 2026-08-25): Prime's auto-refine
and a plain `/refine` write LOCAL entries into `session-artifacts/<session-id>/harness/
harness_state.json`. The runtime merges that with the GLOBAL store `~/.prime/agent/harness/`
(= the arm directory) at session start, but nothing ever copies local entries upward. Our
launcher starts a fresh root session per run and quarantines old session-artifacts, so in
idea_01 every one of 5,974 refinement entries stayed local and none crossed a session. The
env var `RLM_HARNESS_STATE_DIR` only re-points the kernel-side `rlm.harness` local store; it
does not change where the TypeScript refiner writes. `/refine --global` does, but that leaves
persistence to the agent's discretion.

So the launcher promotes after every run: every local entry becomes a global entry (scope
rewritten; an id clash keeps the newer `updated_at`/higher version), local refinement records
are appended to the arm's `harness/refinements.jsonl` (the file `loadGlobalRefinementHistory`
reads) with `scope: global` and a `promoted_from` session id. Idempotent: promoted refinement
ids are skipped on a second pass.

    promote_ledger.py <prime-dir>            # promote every session-artifacts/*/harness/ found
    promote_ledger.py <prime-dir> --dry-run
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

KINDS = ("prompt", "memory", "skill", "subagent")


def load(p: Path) -> dict:
    if p.exists():
        d = json.loads(p.read_text())
        d.setdefault("schema", 1)
        d.setdefault("entries", {})
        for k in KINDS:
            d["entries"].setdefault(k, {})
        d.setdefault("refinements", [])
        return d
    return {"schema": 1, "entries": {k: {} for k in KINDS}, "refinements": []}


def newer(a: dict, b: dict) -> bool:
    """True if entry a should replace entry b."""
    va, vb = a.get("version", 0) or 0, b.get("version", 0) or 0
    if va != vb:
        return va > vb
    return str(a.get("updated_at", "")) >= str(b.get("updated_at", ""))


def promote(prime_dir: Path, dry: bool = False) -> dict:
    gdir = prime_dir / "harness"
    gstate_p = gdir / "harness_state.json"
    ghist_p = gdir / "refinements.jsonl"
    g = load(gstate_p)
    seen_ids = {r.get("id") for r in g["refinements"]}
    if ghist_p.exists():
        for line in ghist_p.read_text().splitlines():
            try:
                seen_ids.add(json.loads(line).get("id"))
            except Exception:  # noqa: BLE001
                pass
    stats = {"sessions": 0, "entries_added": 0, "entries_updated": 0, "refinements_added": 0}
    new_hist_lines = []
    for lp in sorted(prime_dir.glob("session-artifacts/*/harness/harness_state.json")):
        sid = lp.parent.parent.name
        loc = load(lp)
        stats["sessions"] += 1
        for k in KINDS:
            for eid, e in loc["entries"].get(k, {}).items():
                e = dict(e)
                e["scope"] = "global"
                e.setdefault("promoted_from", sid)
                cur = g["entries"][k].get(eid)
                if cur is None:
                    g["entries"][k][eid] = e
                    stats["entries_added"] += 1
                elif newer(e, cur):
                    g["entries"][k][eid] = e
                    stats["entries_updated"] += 1
        for r in loc.get("refinements", []):
            rid = r.get("id")
            if rid in seen_ids:
                continue
            r = dict(r)
            r["scope"] = "global"
            r["promoted_from"] = sid
            g["refinements"].append(r)
            new_hist_lines.append(json.dumps(r))
            seen_ids.add(rid)
            stats["refinements_added"] += 1
    if not dry and stats["sessions"]:
        gdir.mkdir(parents=True, exist_ok=True)
        tmp = gstate_p.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(g, indent=2) + "\n")
        os.replace(tmp, gstate_p)
        if new_hist_lines:
            with ghist_p.open("a") as f:
                f.write("\n".join(new_hist_lines) + "\n")
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prime_dir", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not a.prime_dir.is_dir():
        sys.exit(f"no such prime dir: {a.prime_dir}")
    print(json.dumps(promote(a.prime_dir, a.dry_run)))


if __name__ == "__main__":
    main()
