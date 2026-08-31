#!/usr/bin/env bash
# Launch a contained silicon-sample-submission idea session. Adapted from gssim_prime.
#
# The container is not a security boundary — Prime Agent runs model-written Python with the
# session user's permissions either way. It is EXPERIMENTAL CONTROL: self-improvement is the
# thing under study, so the state that improves has to be mounted, resettable and diffable.
# For this project it is also the BLINDING boundary: what an idea's session can see is
# exactly the mount set below, and no mount carries human outcome data of the target study.
#
# WHAT THE CONTAINER SEES, and nothing else:
#
#   <idea>/run/         -> /workspace/run        the harness surface (and the session's cwd):
#                                                 the frozen definitions, AGENTS.md, the
#                                                 skills it writes, its runs
#   data/               -> /workspace/datasets   read-only: the public training datasets
#                                                 (or exactly one of them, with SSB_DATASET)
#   silicon-sample-submission-template/
#                       -> /workspace/benchmark  read-only: the official submission template
#                                                 (survey instrument, codebook, validator)
#   utils/prime/gates/  -> /workspace/gates      read-only: operator-owned completion gates
#                                                 (transparent criteria, un-editable in-run)
#   pyproject.toml …    -> /workspace/           read-only, the uv project
#
# Not mounted: utils/ (this launcher, the Dockerfile), the idea's frozen.sha256 signature,
# .container-state/ (the OAuth token, every arm's harness state, all snapshots), the repo
# root, .git, BENCHMARK_NOTES.md, and every other idea.
#
#   idea        which idea's harness surface to mount (idea_01, idea_02, …).
#   arm         one experimental condition. Its Prime Agent state lives in
#               .container-state/arms/<idea>/<arm>/prime, mounted at ~/.prime/agent. A new
#               arm name starts with no harness state; reusing one carries it.
#   snapshots   harness state, AGENTS.md and skill hashes are copied out before and after
#               every run, so what the harness learned is a diff, not an anecdote.
#   frozen      <idea>/run/.prime/agent/APPEND_SYSTEM.md is checked against
#               <idea>/frozen.sha256 before the run starts and again after it ends. The
#               signature lives outside the mount set, so an in-container edit cannot
#               forge it.
#
# Usage:
#   SSB_IDEA=idea_01 SSB_ARM=fresh ./utils/prime/run.sh                  # interactive
#   SSB_IDEA=idea_01 SSB_ARM=fresh ./utils/prime/run.sh bash             # a shell
#   SSB_IDEA=idea_01 SSB_ARM=fresh ./utils/prime/run.sh \
#       --mode json --autonomous "$(cat idea_01/run/TASK_01.md)"             # headless
set -euo pipefail
cd "$(dirname "$0")/../.."
REPO_ROOT="$PWD"

IMAGE="${SSB_IMAGE:-ssb-prime:latest}"
IDEA="${SSB_IDEA:-}"
ARM="${SSB_ARM:-default}"
DATASET="${SSB_DATASET:-}"           # optional: restrict the mount to one dataset
# Further options (SSB_DATASET_EXCLUDE, SSB_RUN_DIR, SSB_PRIME_DIR, SSB_EXTRA_MOUNTS,
# SSB_LEDGER_PROMOTE) are read below, after <idea>/launch.env has supplied the idea's defaults.
STATE_DIR="${SSB_STATE:-$REPO_ROOT/.container-state}"
MODEL="${SSB_MODEL:-claude-opus-5}"
THINKING="${SSB_THINKING:-high}"     # off|minimal|low|medium|high|xhigh|max
TEMPLATE_DIR="$REPO_ROOT/silicon-sample-submission-template"

case "$ARM" in */*|..|.) echo "SSB_ARM must be a bare name" >&2; exit 1 ;; esac

# ------------------------------------------------------------------- idea (exactly one)
if [ -z "$IDEA" ]; then
    echo "SSB_IDEA is required: the container mounts exactly one idea's run/ directory." >&2
    echo "  SSB_IDEA=idea_01 $0 [args]" >&2
    echo "Available:" >&2
    for d in "$REPO_ROOT"/idea_*/; do [ -e "$d" ] && echo "  $(basename "$d")" >&2; done
    exit 1
fi
case "$IDEA" in */*|..|.) echo "SSB_IDEA must be a bare directory name" >&2; exit 1 ;; esac
[ -d "$REPO_ROOT/$IDEA/run" ] || { echo "no such idea surface: $IDEA/run" >&2; exit 1; }
RUN_DIR="$REPO_ROOT/$IDEA/run"
FROZEN="$RUN_DIR/.prime/agent/APPEND_SYSTEM.md"
SIGNATURE="$REPO_ROOT/$IDEA/frozen.sha256"

# ---------------------------------------------------- what this idea's container may see
# <idea>/launch.env declares the idea's mount defaults (held-out datasets to exclude, ledger
# promotion, …) as `VAR=${VAR:-default}` lines, so a caller's explicit setting still wins.
# An idea without the file (idea_01) runs exactly as before.
if [ -f "$REPO_ROOT/$IDEA/launch.env" ]; then
    set -a; . "$REPO_ROOT/$IDEA/launch.env"; set +a
    echo "note: defaults from $IDEA/launch.env" >&2
fi
DATASET_EXCLUDE="${SSB_DATASET_EXCLUDE:-}"   # comma list of data/<name> NOT to mount (held-out studies)
RUN_DIR_OVERRIDE="${SSB_RUN_DIR:-}"          # mount this directory as /workspace/run instead of <idea>/run (evaluation forks)
PRIME_DIR_OVERRIDE="${SSB_PRIME_DIR:-}"      # arm state directory (evaluation forks)
EXTRA_MOUNTS="${SSB_EXTRA_MOUNTS:-}"         # ';'-separated host:container[:ro] extra bind mounts
LEDGER_PROMOTE="${SSB_LEDGER_PROMOTE:-0}"    # 1: after the run, promote the session's local Prime ledger to the arm's global one
DATASET_REPLACE="${SSB_DATASET_REPLACE:-}"   # ';'-separated name=dir: mount <dir> at /workspace/datasets/<name> INSTEAD of
                                             # data/<name> (idea_04's arm-holdout masked copies; relative dirs are repo-relative)
# replacement_for <name> <default-dir>: the directory to mount for dataset <name>.
replacement_for() {
    local name="$1" dflt="$2" e n d
    if [ -n "$DATASET_REPLACE" ]; then
        IFS=';' read -r -a _REPL <<< "$DATASET_REPLACE"
        for e in "${_REPL[@]}"; do
            [ -n "$e" ] || continue
            n="${e%%=*}"; d="${e#*=}"
            if [ "$n" = "$name" ]; then
                case "$d" in /*) ;; *) d="$REPO_ROOT/$d" ;; esac
                [ -d "$d" ] || { echo "SSB_DATASET_REPLACE: no such directory for $name: $d" >&2; exit 1; }
                printf '%s' "$(cd "$d" && pwd -P)"; return
            fi
        done
    fi
    printf '%s' "$(cd "$dflt" && pwd -P)"
}
# dataset_rel <host-path>: the path relative to /workspace/datasets a mounted file lands at,
# for the original data/ tree and for replaced directories alike.
dataset_rel() {
    local src="$1" e n d
    if [ -n "$DATASET_REPLACE" ]; then
        IFS=';' read -r -a _REPL <<< "$DATASET_REPLACE"
        for e in "${_REPL[@]}"; do
            [ -n "$e" ] || continue
            n="${e%%=*}"; d="${e#*=}"
            case "$d" in /*) ;; *) d="$REPO_ROOT/$d" ;; esac
            d="$(cd "$d" 2>/dev/null && pwd -P)" || continue
            case "$src" in "$d"/*) printf '%s' "$n/${src#$d/}"; return ;; esac
        done
    fi
    printf '%s' "${src#$REPO_ROOT/data/}"
}
if [ -n "$RUN_DIR_OVERRIDE" ]; then
    RUN_DIR="$(cd "$RUN_DIR_OVERRIDE" 2>/dev/null && pwd -P)" || { echo "no such SSB_RUN_DIR: $RUN_DIR_OVERRIDE" >&2; exit 1; }
    FROZEN="$RUN_DIR/.prime/agent/APPEND_SYSTEM.md"
fi

# -------------------------------------------------------------- datasets (all, or one)
DATASET_MOUNTS=()
if [ -n "$DATASET" ]; then
    case "$DATASET" in */*|..|.) echo "SSB_DATASET must be a bare directory name" >&2; exit 1 ;; esac
    DATASET_DIR="$(cd "$REPO_ROOT/data/$DATASET" 2>/dev/null && pwd -P)" \
        || { echo "no such dataset: data/$DATASET" >&2; exit 1; }
    DATASET_MOUNTS+=(-v "$DATASET_DIR:/workspace/datasets/$DATASET:ro")
elif [ -n "$DATASET_EXCLUDE" ]; then
    # Held-out studies (idea_02 validation / internal test) must not be on disk inside the
    # container at all. Docker cannot mask a subdirectory of a bind mount, so mount every
    # other dataset directory individually, plus the index README.
    IFS=',' read -r -a EXCL <<< "$DATASET_EXCLUDE"
    for d in "$REPO_ROOT"/data/*/; do
        name="$(basename "$d")"
        skip=0
        for x in "${EXCL[@]}"; do [ "$name" = "$x" ] && skip=1; done
        [ "$skip" = 1 ] && continue
        src="$(replacement_for "$name" "$d")"
        DATASET_MOUNTS+=(-v "$src:/workspace/datasets/$name:ro")
        [ "$src" = "$(cd "$d" && pwd -P)" ] || echo "note: /workspace/datasets/$name is mounted from $src (replaced)" >&2
    done
    echo "note: datasets excluded from the mount: $DATASET_EXCLUDE" >&2
    # Documentation inside the mounted datasets (the data/ index, READMEs, codebooks, scripts)
    # that names an excluded study is overlaid with a redacted copy — nested bind mounts over
    # the read-only originals. The list of overlays is recorded with the run.
    REDACT_DIR="$STATE_DIR/mounts/$(date -u +%Y%m%dT%H%M%SZ)"
    mkdir -p "$REDACT_DIR"
    MOUNTED_DIRS=()
    for d in "$REPO_ROOT"/data/*/; do
        name="$(basename "$d")"; skip=0
        for x in "${EXCL[@]}"; do [ "$name" = "$x" ] && skip=1; done
        [ "$skip" = 1 ] || MOUNTED_DIRS+=("$(replacement_for "$name" "$d")")
    done
    while IFS= read -r line; do
        [ -n "$line" ] || continue
        src="${line%%:*}"; rest="${line#*:}"; dst="${rest%%:*}"
        rel="$(dataset_rel "$src")"
        DATASET_MOUNTS+=(-v "$dst:/workspace/datasets/$rel:ro")
    done < <(cd "$REPO_ROOT" && python3 utils/prime/redact_mounts.py --exclude "$DATASET_EXCLUDE" --out "$REDACT_DIR" \
                --file data/README.md "${MOUNTED_DIRS[@]}" 2>"$REDACT_DIR/summary.txt" | tee "$REDACT_DIR/overlays.txt")
    # the data/ index is mounted plain only when no redacted overlay replaced it
    if [ -f "$REPO_ROOT/data/README.md" ] && ! grep -q "^$REPO_ROOT/data/README.md:" "$REDACT_DIR/overlays.txt"; then
        DATASET_MOUNTS+=(-v "$REPO_ROOT/data/README.md:/workspace/datasets/README.md:ro")
    fi
    echo "note: $(wc -l < "$REDACT_DIR/overlays.txt" | tr -d ' ') redacted overlays ($(grep -c . "$REDACT_DIR/summary.txt") summary lines in $REDACT_DIR/summary.txt)" >&2
else
    DATASET_MOUNTS+=(-v "$REPO_ROOT/data:/workspace/datasets:ro")
    if [ -n "$DATASET_REPLACE" ]; then   # nested bind mounts over the originals (the mountpoints exist in data/)
        IFS=';' read -r -a _REPL <<< "$DATASET_REPLACE"
        for e in "${_REPL[@]}"; do
            [ -n "$e" ] || continue
            n="${e%%=*}"
            [ -d "$REPO_ROOT/data/$n" ] || { echo "SSB_DATASET_REPLACE: data/$n does not exist to be replaced" >&2; exit 1; }
            DATASET_MOUNTS+=(-v "$(replacement_for "$n" "$REPO_ROOT/data/$n"):/workspace/datasets/$n:ro")
            echo "note: /workspace/datasets/$n is mounted from a replacement directory" >&2
        done
    fi
fi
EXTRA_MOUNT_ARGS=()
if [ -n "$EXTRA_MOUNTS" ]; then
    IFS=';' read -r -a EM <<< "$EXTRA_MOUNTS"
    for m in "${EM[@]}"; do [ -n "$m" ] && EXTRA_MOUNT_ARGS+=(-v "$m"); done
fi

# ------------------------------------------------------------------- the frozen check
hash_of() { { sha256sum "$1" 2>/dev/null || shasum -a 256 "$1" 2>/dev/null; } | awk '{print $1}'; }
[ -f "$SIGNATURE" ] || { echo "missing $SIGNATURE — the definitions are unsigned; run utils/sign-frozen.sh $IDEA" >&2; exit 1; }
SIGNED="$(awk '{print $1}' "$SIGNATURE")"
FROZEN_BEFORE="$(hash_of "$FROZEN")"
if [ "$FROZEN_BEFORE" != "$SIGNED" ]; then
    echo "$IDEA/run/.prime/agent/APPEND_SYSTEM.md does not match its signature." >&2
    echo "It carries the binding definitions — the criteria a run works under — so a run starting" >&2
    echo "from an unsigned version measures nothing. Either revert it:" >&2
    echo "    git checkout -- $IDEA/run/.prime/agent/APPEND_SYSTEM.md" >&2
    echo "or, if the change is yours and intended, sign it: utils/sign-frozen.sh $IDEA" >&2
    exit 1
fi

# ------------------------------------------------------------------------------ the arm
PRIME_DIR="${PRIME_DIR_OVERRIDE:-$STATE_DIR/arms/$IDEA/$ARM/prime}"   # -> ~/.prime/agent  (harness state, sessions, auth)
AUTH_FILE="$STATE_DIR/auth.json"               # shared across arms: a reset must not log you out
mkdir -p "$PRIME_DIR"
[ -f "$AUTH_FILE" ] || { : > "$AUTH_FILE"; chmod 600 "$AUTH_FILE"; }
# Nested bind mounts need their mountpoint to exist inside the outer mount first.
[ -f "$PRIME_DIR/auth.json" ] || : > "$PRIME_DIR/auth.json"

# A SYSTEM.md in either prompt directory REPLACES the base system prompt entirely
# (docs/usage.md, 0.7.2) — a session could rewrite its ground rules without touching the
# signed APPEND_SYSTEM.md. Their absence is part of the frozen contract, checked before
# and after the run; an APPEND_SYSTEM.md in the arm state would append unsigned text too.
UNSIGNED_PROMPT_FILES=("$RUN_DIR/.prime/agent/SYSTEM.md"
                       "$PRIME_DIR/SYSTEM.md" "$PRIME_DIR/APPEND_SYSTEM.md")
for f in "${UNSIGNED_PROMPT_FILES[@]}"; do
    if [ -e "$f" ]; then
        echo "refusing to run: $f exists — it would inject an unsigned system prompt" >&2
        echo "around the frozen definitions. Remove it (or sign what you actually mean)." >&2
        exit 1
    fi
done

# Residual daemon/session state from a previous container wedges the new container's
# daemon BEFORE the agent loop starts, so the autonomous timeout never arms (four idle
# hangs on 2026-08-19/20; leases/workers cleanup alone did NOT fix it — only a full
# archive of per-session state did, twice). Our runs are one-shot: nothing in these
# dirs is ever legitimately carried across launches. Durable knowledge lives in the
# run/ mount (AGENTS.md, skills) and survives; archived transcripts stay readable
# (utils/track_progress.py globs the archives).
ARCHIVE="$PRIME_DIR/_archive-$(date -u +%Y%m%dT%H%M%SZ)"
for stale in session-leases daemon-workers sessions session-artifacts logs; do
    if [ -d "$PRIME_DIR/$stale" ] && [ -n "$(ls -A "$PRIME_DIR/$stale" 2>/dev/null)" ]; then
        mkdir -p "$ARCHIVE" && mv "$PRIME_DIR/$stale" "$ARCHIVE/$stale" && mkdir -p "$PRIME_DIR/$stale"
        echo "note: archived $stale -> $ARCHIVE" >&2
    fi
done

# Auto-refine is ON by upstream default (since 0.2.8) and self-improvement is the thing
# under study here, so the refinement regime must be pinned per arm, not inherited.
# SSB_AUTOREFINE=on|off (default on). Written only when the arm has no settings.json yet;
# an existing file is arm state and is left alone (and snapshotted below).
if [ ! -f "$PRIME_DIR/settings.json" ]; then
    case "${SSB_AUTOREFINE:-on}" in
        on)  printf '{\n  "autoRefine": { "enabled": true }\n}\n'  > "$PRIME_DIR/settings.json" ;;
        off) printf '{\n  "autoRefine": { "enabled": false }\n}\n' > "$PRIME_DIR/settings.json" ;;
        *) echo "SSB_AUTOREFINE must be on or off" >&2; exit 1 ;;
    esac
fi

# ------------------------------------------------------------ simulator auth (Claude CLI)
ENV_FILE="${SSB_ENV:-$STATE_DIR/container.env}"
ENV_ARGS=()
if [ -f "$ENV_FILE" ]; then
    if grep -Eq '^CLAUDE_CODE_OAUTH_TOKEN=["'"'"']|^CLAUDE_CODE_OAUTH_TOKEN=.*[[:space:]]$' "$ENV_FILE"; then
        echo "CLAUDE_CODE_OAUTH_TOKEN in $ENV_FILE is quoted or has trailing whitespace —" >&2
        echo "docker --env-file passes that verbatim and the token becomes invalid; write it bare" >&2
        exit 1
    fi
    ENV_ARGS=(--env-file "$ENV_FILE")
else
    echo "note: no $ENV_FILE — simulator calls via 'claude -p' will not be authenticated." >&2
fi
# ANTHROPIC_API_KEY is never forwarded: an ambient key silently bills the metered API.

# ------------------------------------------------------------------------- run identity
RUN_ID="${SSB_RUN_ID:-$(date -u +%Y%m%dT%H%M%SZ)_${IDEA}_${ARM}}"
SNAP_DIR="$STATE_DIR/snapshots/$RUN_ID"
mkdir -p "$SNAP_DIR"

# Snapshots are best-effort throughout: a snapshot must never abort a run.
snapshot() {  # $1 = before|after
    local tag="$1" f sid
    [ -d "$PRIME_DIR/harness" ] && cp -R "$PRIME_DIR/harness" "$SNAP_DIR/harness_global.$tag" 2>/dev/null || true
    if [ -d "$PRIME_DIR/session-artifacts" ]; then
        while IFS= read -r f; do
            [ -n "$f" ] || continue
            sid="$(basename "$(dirname "$(dirname "$f")")")"
            cp "$f" "$SNAP_DIR/harness_state.$sid.$tag.json" 2>/dev/null || true
        done < <(find "$PRIME_DIR/session-artifacts" -name harness_state.json 2>/dev/null || true)
    fi
    cp "$RUN_DIR/AGENTS.md" "$SNAP_DIR/AGENTS.$tag.md" 2>/dev/null || true
    cp "$PRIME_DIR/settings.json" "$SNAP_DIR/settings.$tag.json" 2>/dev/null || true
    cp "$PRIME_DIR/telemetry.json" "$SNAP_DIR/telemetry.$tag.json" 2>/dev/null || true
    if [ -d "$RUN_DIR/.prime/agent/skills" ]; then
        (cd "$RUN_DIR" && find .prime/agent/skills -type f 2>/dev/null | sort | tr '\n' '\0' \
            | xargs -0 shasum -a 256 2>/dev/null) > "$SNAP_DIR/skills.$tag.sha256" 2>/dev/null || true
    else
        : > "$SNAP_DIR/skills.$tag.sha256"
    fi
}
if [ "${SSB_DRY_RUN:-0}" = 1 ]; then
    echo "SSB_DRY_RUN=1: checks passed; not launching. Dataset mount set:" >&2
    i=0; for a in "${DATASET_MOUNTS[@]}"; do [ "$a" = -v ] || echo "  $a" >&2; done
    for a in ${EXTRA_MOUNT_ARGS[@]+"${EXTRA_MOUNT_ARGS[@]}"}; do [ "$a" = -v ] || echo "  $a (extra)" >&2; done
    exit 0
fi
snapshot before

cat > "$SNAP_DIR/run.json" <<EOF
{
  "run_id": "$RUN_ID",
  "idea": "$IDEA",
  "arm": "$ARM",
  "dataset": "${DATASET:-all}",
  "dataset_exclude": "$DATASET_EXCLUDE",
  "dataset_replace": "$DATASET_REPLACE",
  "run_dir": "$RUN_DIR",
  "prime_dir": "$PRIME_DIR",
  "ledger_promote": "$LEDGER_PROMOTE",
  "model": "$MODEL",
  "thinking": "$THINKING",
  "autorefine": "${SSB_AUTOREFINE:-on}",
  "gate": "${SSB_GATE:-default}",
  "goal": $(printf '%s' "${SSB_GOAL:-}" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))'),
  "started_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "image": "$IMAGE",
  "git_commit": "$(git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || echo unknown)",
  "git_dirty": $(test -n "$(git -C "$REPO_ROOT" status --porcelain 2>/dev/null)" && echo true || echo false),
  "frozen_sha256_before": "$FROZEN_BEFORE"
}
EOF

# ------------------------------------------------------------------------------- launch
# The node base image's entrypoint prepends `node` to any argument starting with '-', so
# bare flags would be eaten before prime-agent ever sees them. Name the program explicitly
# when the caller passes flags (or nothing); an explicit command like `bash` passes through.
CMD_ARGS=("$@")
if [ $# -eq 0 ] || [ "${1#-}" != "$1" ]; then
    # Pin model and reasoning level. Prime Agent's model default tracks its own release
    # (thinking documents a default of xhigh as of 0.7.2), so an unpinned run is not
    # reproducible. An explicit flag from the caller wins.
    PINS=()
    case " $* " in *" --model "*) ;; *) PINS+=(--model "$MODEL") ;; esac
    case " $* " in *" --thinking "*) ;; *) PINS+=(--thinking "$THINKING") ;; esac
    # --autonomous inherits silent defaults sized for coding tasks (3 continuations,
    # 12 turns, 80k tokens, 30 min — the 30 min cut a 31-min authoring session's exit
    # short). Pin idea-session budgets; any explicit --autonomous-* from the caller wins.
    if [[ " $* " == *" --autonomous "* ]]; then
        case " $* " in *" --autonomous-max-continuations "*) ;; *) PINS+=(--autonomous-max-continuations "${SSB_AUTONOMOUS_MAX_CONTINUATIONS:-10}") ;; esac
        case " $* " in *" --autonomous-max-turns "*) ;; *) PINS+=(--autonomous-max-turns "${SSB_AUTONOMOUS_MAX_TURNS:-300}") ;; esac
        # The token count is input + output + cacheWrite (cacheRead is free); with a
        # growing context, cacheWrite dominates at ~10x output, so size accordingly.
        case " $* " in *" --autonomous-max-tokens "*) ;; *) PINS+=(--autonomous-max-tokens "${SSB_AUTONOMOUS_MAX_TOKENS:-8000000}") ;; esac
        case " $* " in *" --autonomous-timeout-ms "*) ;; *) PINS+=(--autonomous-timeout-ms "${SSB_AUTONOMOUS_TIMEOUT_MS:-10800000}") ;; esac
        # Completion gate (ARC-3-style): the session may not finish until the gate
        # passes; failed-gate output is fed back for another attempt. Operator-owned,
        # mounted read-only. SSB_GATE=off disables; any other value replaces the command.
        if [ "${SSB_GATE:-default}" != off ]; then
            case " $* " in *" --autonomous-gate "*) ;; *)
                GATE_CMD="${SSB_GATE:-default}"
                [ "$GATE_CMD" = default ] && GATE_CMD="uv run --project /workspace python /workspace/gates/session_gate.py"
                PINS+=(--autonomous-gate "$GATE_CMD") ;;
            esac
        fi
    fi
    # Optional persistent goal (re-prompted until the agent calls goal.complete()).
    if [ -n "${SSB_GOAL:-}" ]; then
        PINS+=(--goal "$SSB_GOAL")
        [ -n "${SSB_GOAL_TOKENS:-}" ] && PINS+=(--goal-token-budget "$SSB_GOAL_TOKENS")
    fi
    CMD_ARGS=(prime-agent ${PINS[@]+"${PINS[@]}"} "$@")
fi

RUN_MODE_ARGS=(--rm -it)
if [ "${SSB_DETACH:-0}" != 0 ]; then RUN_MODE_ARGS=(-d)
elif ! { [ -t 0 ] && [ -t 1 ]; }; then RUN_MODE_ARGS=(--rm -i); fi

set +e
docker run "${RUN_MODE_ARGS[@]}" --init \
    ${ENV_ARGS[@]+"${ENV_ARGS[@]}"} \
    -e "SSB_RUN_ID=$RUN_ID" \
    -e "SSB_IDEA=$IDEA" \
    -e "SSB_ARM=$ARM" \
    -e "SSB_DATASET=${DATASET:-all}" \
    -e "SSB_SESSION_START=$(date +%s)" \
    -e "SSB_FROZEN_SHA256=$SIGNED" \
    -v "$REPO_ROOT/utils/prime/gates:/workspace/gates:ro" \
    -v "$RUN_DIR:/workspace/run" \
    "${DATASET_MOUNTS[@]}" \
    ${EXTRA_MOUNT_ARGS[@]+"${EXTRA_MOUNT_ARGS[@]}"} \
    -v "$TEMPLATE_DIR:/workspace/benchmark:ro" \
    -v "$REPO_ROOT/pyproject.toml:/workspace/pyproject.toml:ro" \
    -v "$REPO_ROOT/uv.lock:/workspace/uv.lock:ro" \
    -v "$REPO_ROOT/.python-version:/workspace/.python-version:ro" \
    -v "$PRIME_DIR:/home/agent/.prime/agent" \
    -v "$AUTH_FILE:/home/agent/.prime/agent/auth.json" \
    -w /workspace/run \
    "$IMAGE" "${CMD_ARGS[@]}"
STATUS=$?
set -e

# ------------------------------------------------------------------------------ verdict
[ "${SSB_DETACH:-0}" != 0 ] && exit $STATUS

# Prime's auto-refine writes LOCAL ledger entries (session-artifacts/<id>/harness/), which a
# fresh session never sees; the arm-level GLOBAL ledger (~/.prime/agent/harness/) is what the
# next session merges in. Promote before the after-snapshot so the diff shows what persisted.
if [ "$LEDGER_PROMOTE" = 1 ]; then
    python3 "$REPO_ROOT/utils/prime/promote_ledger.py" "$PRIME_DIR" >&2 || echo "warning: ledger promotion failed" >&2
fi

snapshot after
FROZEN_AFTER="$(hash_of "$FROZEN")"
python3 - "$SNAP_DIR/run.json" "$FROZEN_AFTER" "$STATUS" <<'PY'
import json, sys, datetime
path, after, status = sys.argv[1], sys.argv[2], int(sys.argv[3])
d = json.load(open(path))
d["ended_at"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
d["exit_status"] = status
d["frozen_sha256_after"] = after
d["frozen_intact"] = (after == d["frozen_sha256_before"])
json.dump(d, open(path, "w"), indent=2)
PY

if [ "$FROZEN_BEFORE" != "$FROZEN_AFTER" ]; then
    echo >&2
    echo "*** THE FROZEN DEFINITIONS CHANGED DURING THIS RUN ***" >&2
    echo "    $IDEA/run/.prime/agent/APPEND_SYSTEM.md carries the binding definitions. A run" >&2
    echo "    that edits its own criteria has invalidated its own result. Inspect:" >&2
    echo "    git diff -- $FROZEN" >&2
    echo >&2
fi
for f in "${UNSIGNED_PROMPT_FILES[@]}"; do
    if [ -e "$f" ]; then
        echo >&2
        echo "*** AN UNSIGNED PROMPT FILE APPEARED DURING THIS RUN: $f ***" >&2
        echo "    SYSTEM.md replaces the base system prompt; an arm-state APPEND_SYSTEM.md" >&2
        echo "    appends unsigned text. The run wrote around its frozen definitions —" >&2
        echo "    inspect it, then remove it before the next run." >&2
        echo >&2
    fi
done
echo "run $RUN_ID -> $SNAP_DIR (exit $STATUS)" >&2
exit $STATUS
