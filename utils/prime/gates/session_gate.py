#!/usr/bin/env python3
"""Operator-owned completion gate for autonomous idea sessions (ARC-3-style).

Mounted read-only at /workspace/gates/ — the agent can read the criteria (they are
meant to be transparent, like a benchmark verifier) but cannot edit them. Runs via
Prime Agent's `--autonomous-gate`: the session is not allowed to finish until this
exits 0; on failure the (bounded) output below is fed back to the agent for another
attempt.

Checks are integrity checks, not quality judgments — whether a session *improved*
anything is judged by the operator from the scoreboard and snapshots afterwards.
Stdlib only; must stay fast (< a few seconds).
"""
import csv
import os
import sys
import hashlib
from pathlib import Path

RUN = Path("/workspace/run") if Path("/workspace/run").is_dir() else Path.cwd()
failures = []


def fail(msg: str) -> None:
    failures.append(msg)


# 1. Frozen definitions unchanged mid-session (signed hash passed in by the launcher;
#    the launcher also re-checks after the container exits, but catching it here lets
#    the session revert instead of invalidating itself).
signed = os.environ.get("SSB_FROZEN_SHA256", "")
frozen = RUN / ".prime/agent/APPEND_SYSTEM.md"
if signed:
    if not frozen.is_file():
        fail(f"frozen definitions missing: {frozen}")
    else:
        h = hashlib.sha256(frozen.read_bytes()).hexdigest()
        if h != signed:
            fail(
                "APPEND_SYSTEM.md no longer matches its signature — the session edited "
                "its own binding definitions. Revert it (git is not available in here: "
                "restore the original content) before the session can finish."
            )

# 2. No unsigned system-prompt files (SYSTEM.md would REPLACE the base prompt).
for p in [RUN / ".prime/agent/SYSTEM.md"]:
    if p.exists():
        fail(f"{p} exists — it would inject an unsigned system prompt. Remove it.")

# 3. Scoreboard integrity (only if a scoreboard exists — authoring sessions may not
#    have one yet).
sb = RUN / "runs/scoreboard.csv"
if sb.is_file():
    try:
        rows = list(csv.DictReader(sb.open()))
    except Exception as e:  # noqa: BLE001
        rows = []
        fail(f"runs/scoreboard.csv does not parse: {e}")
    if rows:
        required = {"run_id", "stage", "stub", "task_id", "leak_verdict"}
        missing = required - set(rows[0].keys())
        if missing:
            fail(f"scoreboard missing required columns: {sorted(missing)}")
        else:
            for i, r in enumerate(rows, start=2):
                if r["stub"] not in ("True", "False"):
                    fail(f"scoreboard line {i}: stub must be True/False, got {r['stub']!r}")
                    break
            # TARGET rows are exempt: no sealed truth exists for the target, so their
            # leak audit is structurally n/a (the blinding there is enforced upstream).
            bad = [
                r for r in rows
                if r["stub"] == "False" and r["task_id"] != "TARGET"
                and r["leak_verdict"] != "CLEAN"
            ]
            if bad:
                fail(
                    f"{len(bad)} non-stub scoreboard row(s) without a CLEAN leak verdict "
                    f"(first: run_id={bad[0]['run_id']}, task={bad[0]['task_id']}, "
                    f"verdict={bad[0]['leak_verdict']!r}). Un-audited scores may not stand."
                )

# 4. Close-out contract: REPORT.md must exist and have been written during THIS
#    session (mtime vs. the session start epoch passed in by the launcher).
report = RUN / "REPORT.md"
start = os.environ.get("SSB_SESSION_START")
if not report.is_file() or report.stat().st_size == 0:
    fail("REPORT.md missing or empty — every session ends with an operator-readable report.")
elif start and report.stat().st_mtime < float(start):
    fail(
        "REPORT.md was not updated during this session. Write the close-out report "
        "(what was tried, what the scoreboard says, what the operator should judge) "
        "before finishing."
    )

if failures:
    print("SESSION GATE: FAIL")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
print("SESSION GATE: PASS")
