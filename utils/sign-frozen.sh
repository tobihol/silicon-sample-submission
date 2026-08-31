#!/usr/bin/env sh
# Re-sign an idea's frozen definitions. Operator-only: signing is the act that makes a
# change to the binding definitions official, and it is meant to be a deliberate,
# reviewable commit. The signature lives outside the container's mount set, so a run
# cannot forge it.
#
# Agent-agnostic: the frozen file is wherever the idea's runtime keeps its always-in-context
# instructions. Detected per runtime, or passed explicitly:
#
#   utils/sign-frozen.sh idea_01                      # auto-detect
#   utils/sign-frozen.sh idea_02 run/CLAUDE.md        # explicit, idea-relative
set -eu
cd "$(dirname "$0")/.."
IDEA="${1:?usage: sign-frozen.sh <idea> [frozen-file-relative-to-idea]}"
[ -d "$IDEA" ] || { echo "no such idea: $IDEA" >&2; exit 1; }

if [ "${2:-}" ]; then
    FROZEN="$IDEA/$2"
else
    # One candidate per known runtime: Prime Agent, Claude Code.
    FROZEN=""
    for f in "$IDEA/run/.prime/agent/APPEND_SYSTEM.md" "$IDEA/run/CLAUDE.md"; do
        [ -f "$f" ] && { FROZEN="$f"; break; }
    done
    [ -n "$FROZEN" ] || { echo "no frozen file found in $IDEA/run/ (looked for .prime/agent/APPEND_SYSTEM.md, CLAUDE.md); pass the path explicitly" >&2; exit 1; }
fi
[ -f "$FROZEN" ] || { echo "no such file: $FROZEN" >&2; exit 1; }

# Prime Agent: a SYSTEM.md beside APPEND_SYSTEM.md would REPLACE the base system prompt,
# making the signed append file meaningless. Refuse to bless that state.
if [ -e "$IDEA/run/.prime/agent/SYSTEM.md" ]; then
    echo "refusing to sign: $IDEA/run/.prime/agent/SYSTEM.md exists — it replaces the base" >&2
    echo "system prompt, so the signature over APPEND_SYSTEM.md would not cover what the" >&2
    echo "agent actually runs under. Remove it first." >&2
    exit 1
fi

if command -v sha256sum >/dev/null 2>&1
then sha256sum "$FROZEN" > "$IDEA/frozen.sha256"
else shasum -a 256 "$FROZEN" > "$IDEA/frozen.sha256"; fi
cat "$IDEA/frozen.sha256"
