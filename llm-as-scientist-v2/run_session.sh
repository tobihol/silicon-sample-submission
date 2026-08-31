#!/usr/bin/env bash
# One-command session driver for the primary entry's campaign (internal arm idea_03,
# published as llm-as-scientist-v2): preflight -> oracle -> session -> post-run audits.
#
#   ./llm-as-scientist-v2/run_session.sh login              first-time Prime Agent login (throwaway arm; the
#                                      token lands in .container-state/auth.json, shared)
#   ./llm-as-scientist-v2/run_session.sh token              store a `claude setup-token` token for the
#                                      in-container simulator (claude -p) — one-time
#   ./llm-as-scientist-v2/run_session.sh                    run a session on idea_03/run/TASK_01.md
#   ./llm-as-scientist-v2/run_session.sh <brief.md>         ...or any other brief
#
# What it does NOT automate, on purpose: the LOSO promotion gate, itest forks, and the
# progress ledger — those are deliberate operator moves.
set -euo pipefail
cd "$(dirname "$0")/.."

STATE=.container-state
EVAL=idea_03/eval
mkdir -p "$EVAL"

# ---------------------------------------------------------------- login subcommand
if [ "${1:-}" = login ]; then
    echo "Starting an interactive container on a throwaway arm. At the prompt type: /login"
    echo "and pick Claude Pro/Max. The browser will end on a FAILED localhost page — that is"
    echo "expected (the callback port lives inside the container). To finish the login:"
    echo "  copy the full URL from the failed browser tab (http://localhost:PORT/callback?...)"
    echo "  and in ANOTHER terminal run:  ./llm-as-scientist-v2/run_session.sh login-callback '<that url>'"
    echo "Exit the session when the TUI confirms login — the token is shared across arms."
    SSB_IDEA=idea_03 SSB_ARM=login-tmp ./utils/prime/run.sh || true
    rm -rf "$STATE/arms/idea_03/login-tmp"
    if [ -s "$STATE/auth.json" ]; then echo "auth.json is set. You can now: ./llm-as-scientist-v2/run_session.sh"
    else echo "auth.json still empty — /login did not complete."; exit 1; fi
    exit 0
fi

# ------------------------------------------- login-callback (in-container OAuth relay)
if [ "${1:-}" = login-callback ]; then
    URL="${2:-}"
    case "$URL" in http://localhost:*/callback\?*code=*) ;; *)
        echo "usage: $0 login-callback 'http://localhost:PORT/callback?code=...&state=...'" >&2
        echo "(paste the full URL from the browser tab that said 'refused to connect')" >&2
        exit 1 ;;
    esac
    CID=$(docker ps -q --filter ancestor=ssb-prime:latest | head -1)
    [ -n "$CID" ] || { echo "no running ssb-prime container — keep the login session open" >&2; exit 1; }
    if docker exec "$CID" curl -fsS --max-time 10 "$URL" >/dev/null; then
        echo "callback delivered — check the login session's TUI, it should now be logged in"
    else
        echo "callback failed — the code may have expired (restart /login and redo the flow)" >&2
        exit 1
    fi
    exit 0
fi

# ---------------------------------------------------------------- token subcommand
# Accepts:  ./llm-as-scientist-v2/run_session.sh token            (prompts, input hidden — preferred)
#           ./llm-as-scientist-v2/run_session.sh token sk-ant-...  or  ./llm-as-scientist-v2/run_session.sh sk-ant-...
store_token() {
    case "$1" in
        *[\'\"[:space:]]*) echo "token contains quotes/whitespace — paste the bare token only" >&2; exit 1 ;;
        sk-ant-*) ;;
        "") echo "empty input" >&2; exit 1 ;;
        *) echo "that does not look like a Claude token (expected sk-ant-...)" >&2; exit 1 ;;
    esac
    mkdir -p "$STATE"
    printf 'CLAUDE_CODE_OAUTH_TOKEN=%s\n' "$1" > "$STATE/container.env"
    chmod 600 "$STATE/container.env"
    echo "wrote $STATE/container.env (simulator auth ready)"
}
if [ "${1:-}" = token ]; then
    if [ -n "${2:-}" ]; then store_token "$2"; exit 0; fi
    echo "Run 'claude setup-token' in another terminal, complete the browser flow,"
    echo "then paste the token here (input hidden):"
    read -rs TOKEN; echo
    store_token "$TOKEN"
    exit 0
fi
case "${1:-}" in sk-ant-*)   # a bare token as the first argument: store it, don't run
    store_token "$1"
    echo "note: the token was passed on the command line, so it is in your shell history —"
    echo "      consider clearing that entry (zsh: run 'fc -l -1' to see it, edit ~/.zsh_history)."
    exit 0 ;;
esac

TASK="${1:-idea_03/run/TASK_01.md}"
[ -f "$TASK" ] || { echo "no such task brief: $TASK" >&2; exit 1; }

# ---------------------------------------------------------------------- preflight
docker image inspect ssb-prime:latest >/dev/null 2>&1 \
    || { echo "image missing — run: docker build -t ssb-prime utils/prime/" >&2; exit 1; }
[ -s "$STATE/auth.json" ] \
    || { echo "Prime Agent is not logged in. Run: ./llm-as-scientist-v2/run_session.sh login" >&2; exit 1; }
if [ ! -f "$STATE/container.env" ]; then
    echo "note: no $STATE/container.env — simulator calls ('claude -p') will be unauthenticated."
    echo "      (fine for TASK_01; to enable: ./llm-as-scientist-v2/run_session.sh token)"
fi
for f in idea_03/run/inputs/val/kim2024/brief/task.json idea_03/run/inputs/organizer_code/statistics.R \
         data/kim2024/carved/halves/index.json; do
    [ -f "$f" ] || { echo "setup incomplete ($f missing) — run: bash utils/heldout/setup_idea03.sh" >&2; exit 1; }
done

# ------------------------------------------------------------------------- oracle
if pgrep -f "score_oracle3.py idea_03/run" >/dev/null 2>&1; then
    echo "oracle: already running"
else
    nohup uv run --with scipy utils/heldout/score_oracle3.py idea_03/run \
        >> "$EVAL/oracle.log" 2>&1 &
    ORACLE_PID=$!
    sleep 3
    kill -0 "$ORACLE_PID" 2>/dev/null \
        || { echo "oracle died on start — see $EVAL/oracle.log" >&2; exit 1; }
    echo "oracle: started (pid $ORACLE_PID, log $EVAL/oracle.log)"
fi

# ------------------------------------------------------------------------ session
N=0; for f in "$EVAL"/*_exec.log; do [ -e "$f" ] && N=$((N + 1)); done; N=$((N + 1))
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)_s$N"
LOG="$EVAL/$(date -u +%Y%m%d)-s${N}_exec.log"
echo "session s$N: run id $RUN_ID, brief $TASK"
echo "  exec log: $LOG   (budgets: idea_03/launch.env — 24 continuations / 800 turns / 24M tok / 6h)"

# health watcher (utils/README.md: >=1 turn_start within 5 min, else stop+quarantine+relaunch)
( sleep 300
  if [ -f "$LOG" ] && ! grep -q turn_start "$LOG"; then
      echo "*** HEALTH CHECK FAILED: no turn_start in $LOG after 5 min." >&2
      echo "*** Likely a wedged daemon: docker stop the container, then relaunch" >&2
      echo "*** (run.sh auto-quarantines stale session state on the next start)." >&2
  fi ) &
WATCHER=$!

set +e
SSB_IDEA=idea_03 SSB_ARM=main SSB_RUN_ID="$RUN_ID" \
    ./utils/prime/run.sh --mode json --autonomous "$(cat "$TASK")" > "$LOG" 2>&1
SESSION_EXIT=$?
set -e
kill "$WATCHER" 2>/dev/null || true
echo "session s$N finished (exit $SESSION_EXIT)"

# ----------------------------------------------------- post-run audits (non-negotiable)
echo "== leak audit (value echo vs every carved truth)"
uv run --with scipy utils/heldout/leak_audit_run.py \
    --prime "$STATE/arms/idea_03/main/prime" --run idea_03/run
echo "== sibling leak scan (itest/diet study names)"
python3 utils/heldout/sibling_leak_scan.py --names bbprime2025,hewitt2026 idea_03/run
echo
echo "Done. Next: read idea_03/run/runs/$RUN_ID/REPORT.md and OPEN.md;"
echo "ledger row: uv run utils/track_progress.py"
echo "Do NOT read idea_03/eval/full/ or eval/itest/ mid-campaign."
