#!/usr/bin/env bash
# Session driver for the secondary-1 entry's harness (internal arm idea_01, published as
# llm-as-scientist-v1): preflight -> session. Written at deposit time for symmetry with
# llm-as-scientist-v2/run_session.sh; the campaign's own sessions were launched with the
# underlying ./utils/prime/run.sh directly.
#
#   ./llm-as-scientist-v1/run_session.sh login              first-time Prime Agent login
#   ./llm-as-scientist-v1/run_session.sh token              store a `claude setup-token`
#                                                           token for the in-container
#                                                           predictor calls (claude -p)
#   ./llm-as-scientist-v1/run_session.sh                    run a session on idea_01/run/TASK_01.md
#   ./llm-as-scientist-v1/run_session.sh <brief.md>         ...or any other brief
#
# From the start state in this repository, TASK_01 is the authoring session: the agent
# designs its own loop (AGENTS.md, tools). The finished pipeline this produced is in the
# entry deposit under run_record/pipeline/ (see its RUNBOOK.md to reproduce the entry itself).
set -euo pipefail
cd "$(dirname "$0")/.."

STATE=.container-state
EVAL=idea_01/eval
mkdir -p "$EVAL"

# ---------------------------------------------------------------- login subcommand
if [ "${1:-}" = login ]; then
    echo "Starting an interactive container on a throwaway arm. At the prompt type: /login"
    echo "and pick Claude Pro/Max. The browser will end on a FAILED localhost page — that is"
    echo "expected. Copy the full callback URL and run in ANOTHER terminal:"
    echo "  ./llm-as-scientist-v1/run_session.sh login-callback '<that url>'"
    SSB_IDEA=idea_01 SSB_ARM=login-tmp ./utils/prime/run.sh || true
    rm -rf "$STATE/arms/idea_01/login-tmp"
    if [ -s "$STATE/auth.json" ]; then echo "auth.json is set."
    else echo "auth.json still empty — /login did not complete."; exit 1; fi
    exit 0
fi

# ------------------------------------------- login-callback (in-container OAuth relay)
if [ "${1:-}" = login-callback ]; then
    URL="${2:-}"
    case "$URL" in http://localhost:*/callback\?*code=*) ;; *)
        echo "usage: $0 login-callback 'http://localhost:PORT/callback?code=...&state=...'" >&2
        exit 1 ;;
    esac
    CID=$(docker ps -q --filter ancestor=ssb-prime:latest | head -1)
    [ -n "$CID" ] || { echo "no running ssb-prime container — keep the login session open" >&2; exit 1; }
    docker exec "$CID" curl -fsS --max-time 10 "$URL" >/dev/null \
        && echo "callback delivered — the login session's TUI should now be logged in" \
        || { echo "callback failed — the code may have expired" >&2; exit 1; }
    exit 0
fi

# ---------------------------------------------------------------- token subcommand
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
    echo "wrote $STATE/container.env (predictor auth ready)"
}
if [ "${1:-}" = token ]; then
    if [ -n "${2:-}" ]; then store_token "$2"; exit 0; fi
    echo "Run 'claude setup-token' in another terminal, then paste the token (input hidden):"
    read -rs TOKEN; echo
    store_token "$TOKEN"
    exit 0
fi

TASK="${1:-idea_01/run/TASK_01.md}"
[ -f "$TASK" ] || { echo "no such task brief: $TASK" >&2; exit 1; }

# ---------------------------------------------------------------------- preflight
docker image inspect ssb-prime:latest >/dev/null 2>&1 \
    || { echo "image missing — run: docker build -t ssb-prime utils/prime/" >&2; exit 1; }
[ -s "$STATE/auth.json" ] \
    || { echo "Prime Agent is not logged in. Run: ./llm-as-scientist-v1/run_session.sh login" >&2; exit 1; }
[ -f "$STATE/container.env" ] \
    || echo "note: no $STATE/container.env — predictor calls ('claude -p') will be unauthenticated."
ls data/*/downloads >/dev/null 2>&1 \
    || echo "note: no data/*/downloads found — fetch training data first (data/README.md)."

# ------------------------------------------------------------------------ session
N=0; for f in "$EVAL"/*_exec.log; do [ -e "$f" ] && N=$((N + 1)); done; N=$((N + 1))
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)_s$N"
LOG="$EVAL/$(date -u +%Y%m%d)-s${N}_exec.log"
echo "session s$N: run id $RUN_ID, brief $TASK"
echo "  exec log: $LOG"

set +e
SSB_IDEA=idea_01 SSB_ARM=main SSB_RUN_ID="$RUN_ID" \
    ./utils/prime/run.sh --mode json --autonomous "$(cat "$TASK")" > "$LOG" 2>&1
SESSION_EXIT=$?
set -e
echo "session s$N finished (exit $SESSION_EXIT)"
echo "Done. Next: read idea_01/run/runs/ for the session's products;"
echo "ledger row: uv run utils/track_progress.py"
