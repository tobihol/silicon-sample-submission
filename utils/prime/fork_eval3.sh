#!/usr/bin/env bash
# Evaluation fork for idea_03's internal test — the branch that gets to see bbprime2025.
# Adapted from fork_eval.sh (idea_02) per idea_03/README.md § "The internal test":
# same fork discipline, two deliberate changes and one fix:
#   - IDEA=idea_03, scored by score_oracle3.py --itest (writes idea_03/eval/itest/ only)
#   - the fork copies ONLY the design-only brief/ directory. fork_eval.sh copied
#     "$ITEST_BRIEF/.." — the whole carved/ dir, which holds the SEALED truth.csv and
#     microdata.csv. Here the copy is brief-only and asserted after the fact.
#   - the mount exclude list is idea_03's ten datasets (launch.env), stated explicitly.
#
# The main arm never mounts the internal-test brief. This script copies the agent's ENTIRE
# mutable surface at this moment — arm state and run/ tree — into a fork, adds exactly one
# thing (the brief, under runs/<run-id>/itest/bbprime2025/brief/), launches ONE fresh root
# session with auto-refine off, scores it sealed, and archives the fork read-only. The main
# arm never sees the brief, the submission, or the score.
#
# Usage:
#   utils/prime/fork_eval3.sh <arm> <n>              # e.g. fork_eval3.sh main 1
#   SSB_FORK_DRY=1 utils/prime/fork_eval3.sh main 1  # copy + sanity checks, no session
set -euo pipefail
cd "$(dirname "$0")/../.."
REPO_ROOT="$PWD"
ARM="${1:?usage: fork_eval3.sh <arm> <n>}"
N="${2:?usage: fork_eval3.sh <arm> <n>}"
IDEA=idea_03
STATE_DIR="${SSB_STATE:-$REPO_ROOT/.container-state}"
SRC_PRIME="$STATE_DIR/arms/$IDEA/$ARM/prime"
SRC_RUN="$REPO_ROOT/$IDEA/run"
FORK_ROOT="$STATE_DIR/forks/$IDEA/$ARM-itest-$N"
ITEST_BRIEF="$REPO_ROOT/data/bbprime2025/carved/brief"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)_${IDEA}_${ARM}-itest-$N"

[ -d "$SRC_PRIME" ] || { echo "no arm state at $SRC_PRIME" >&2; exit 1; }
[ -d "$ITEST_BRIEF" ] || { echo "no internal-test brief at $ITEST_BRIEF" >&2; exit 1; }
[ -e "$FORK_ROOT" ] && { echo "fork $FORK_ROOT exists — one fork per n; pick the next number" >&2; exit 1; }
[ -e "$REPO_ROOT/$IDEA/eval/itest/score_$N.json" ] && { echo "$IDEA/eval/itest/score_$N.json exists" >&2; exit 1; }
if docker ps -q --filter ancestor=ssb-prime:latest | grep -q .; then
    if [ "${SSB_FORK_DRY:-0}" = 1 ]; then
        echo "warning: an ssb-prime container is running — dry-run copy will be mid-session state" >&2
    else
        echo "refusing to fork: an ssb-prime container is running — fork between sessions, not mid-session" >&2
        exit 1
    fi
fi

# The main tree must not already know the internal test (names gate; the value-echo audit
# runs post-session on the whole tree and transcripts).
if python3 "$REPO_ROOT/utils/heldout/sibling_leak_scan.py" --quiet --names bbprime2025 "$SRC_RUN" >/dev/null 2>&1; then :; else
    echo "refusing to fork: the main run tree already names bbprime2025" >&2
    python3 "$REPO_ROOT/utils/heldout/sibling_leak_scan.py" --names bbprime2025 "$SRC_RUN" >&2 || true
    exit 1
fi

mkdir -p "$FORK_ROOT"
echo "copying arm state -> $FORK_ROOT/prime" >&2
rsync -a --exclude 'session-leases' --exclude 'daemon-workers' --exclude 'logs' --exclude '_archive-*' \
    "$SRC_PRIME/" "$FORK_ROOT/prime/"
echo "copying run tree -> $FORK_ROOT/run" >&2
rsync -a --exclude '__pycache__' --exclude '.venv' "$SRC_RUN/" "$FORK_ROOT/run/"

# The brief, and ONLY the brief.
mkdir -p "$FORK_ROOT/run/runs/$RUN_ID/itest/bbprime2025"
cp -R "$ITEST_BRIEF" "$FORK_ROOT/run/runs/$RUN_ID/itest/bbprime2025/brief"
# Hard assertions: nothing sealed entered the fork, and the brief is design-only files.
for bad in truth.csv microdata.csv manifest.json adapter_scoring.json attrition_bounds.csv halves; do
    if [ -e "$FORK_ROOT/run/runs/$RUN_ID/itest/bbprime2025/$bad" ] \
       || [ -e "$FORK_ROOT/run/runs/$RUN_ID/itest/bbprime2025/brief/$bad" ]; then
        echo "FATAL: sealed artefact '$bad' entered the fork — aborting and removing it" >&2
        rm -rf "$FORK_ROOT"; exit 1
    fi
done
find "$FORK_ROOT/run/runs/$RUN_ID/itest" -type f | sed "s|$FORK_ROOT/run/||" > "$FORK_ROOT/ITEST_FILES.txt"
grep -qv -E '/(task\.json|template(_mod_[a-z_]+)?\.csv)$' "$FORK_ROOT/ITEST_FILES.txt" && {
    echo "FATAL: unexpected file in the itest brief (see $FORK_ROOT/ITEST_FILES.txt) — aborting" >&2
    cat "$FORK_ROOT/ITEST_FILES.txt" >&2; rm -rf "$FORK_ROOT"; exit 1; }

# auto-refine off in the fork: the fork measures the method, it does not improve it
python3 - "$FORK_ROOT/prime/settings.json" <<'PY'
import json, sys, pathlib
p = pathlib.Path(sys.argv[1]); d = json.loads(p.read_text()) if p.exists() else {}
d.setdefault("autoRefine", {})["enabled"] = False
p.write_text(json.dumps(d, indent=2) + "\n")
PY
cat > "$FORK_ROOT/FORK.json" <<EOF
{"idea": "$IDEA", "arm": "$ARM", "n": $N, "run_id": "$RUN_ID", "forked_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
 "source_prime": "$SRC_PRIME", "source_run": "$SRC_RUN",
 "git_commit": "$(git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || echo unknown)",
 "run_tree_sha256": "$(cd "$SRC_RUN" && find . -type f -not -path '*/__pycache__/*' -not -path './runs/*' | sort | xargs shasum -a 256 | shasum -a 256 | cut -d' ' -f1)"}
EOF
echo "fork ready: $FORK_ROOT (run id $RUN_ID)" >&2

TASK="$(cat <<EOF
# Internal test — one session, one submission

This is an evaluation fork of your arm. Everything you have built is here unchanged. One
task has been added: \`runs/$RUN_ID/itest/bbprime2025/brief/\` (a design-only brief, exactly
like a validation brief). Predict it **exactly as you would predict the target study**: the
standing method your DESIGN.md prescribes, no shortcuts, no extra care. Write
\`runs/$RUN_ID/itest/bbprime2025/submission_1.csv\` (plus the \`_mod_<m>\` companions if your
target procedure produces them). One submission, ever; you will not see a score. Do not
refine the harness in this session. Then write REPORT.md into \`runs/$RUN_ID/itest/\`: what
procedure ran, cost, and anything that differed from the target procedure.
EOF
)"

if [ "${SSB_FORK_DRY:-0}" = 1 ]; then echo "dry run: not launching" >&2; exit 0; fi

SSB_IDEA=$IDEA SSB_ARM="$ARM-itest-$N" SSB_RUN_ID="$RUN_ID" \
SSB_RUN_DIR="$FORK_ROOT/run" SSB_PRIME_DIR="$FORK_ROOT/prime" SSB_AUTOREFINE=off SSB_LEDGER_PROMOTE=0 \
SSB_DATASET_EXCLUDE="${SSB_DATASET_EXCLUDE:-goldwert2026,bbprime2025,orchinik2024,kim2024,dablander2025,altenmueller2024,kerwer2025,beall2017,bokemper2022,hewitt2026}" \
    "$REPO_ROOT/utils/prime/run.sh" --mode json --autonomous "$TASK" || echo "fork session exited non-zero" >&2

echo "scoring (sealed) …" >&2
uv run --project "$REPO_ROOT" --with scipy python "$REPO_ROOT/utils/heldout/score_oracle3.py" --itest "$FORK_ROOT/run" --n "$N"
echo "leak audit of the fork's transcripts against every sealed task …" >&2
uv run --project "$REPO_ROOT" --with scipy python "$REPO_ROOT/utils/heldout/leak_audit_run.py" --prime "$FORK_ROOT/prime" --run "$FORK_ROOT/run" --exclude bbprime2025 || true
chmod -R a-w "$FORK_ROOT"
echo "fork archived read-only at $FORK_ROOT; score sealed at $IDEA/eval/itest/score_$N.json" >&2
echo "now audit the MAIN tree: python3 utils/heldout/sibling_leak_scan.py --names bbprime2025,hewitt2026 $SRC_RUN" >&2
