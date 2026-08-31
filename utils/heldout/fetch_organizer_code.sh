#!/usr/bin/env bash
# Fetch the organizers' scoring code, pinned to the commit verified in
# docs/organizer-code-comparison-2026-08-27.md, into idea_03's run tree so the agent can
# read exactly how it will be scored. NOT committed to this repo (the organizer repo
# declares no license) — gitignored, re-fetched by anyone via this script.
set -euo pipefail
cd "$(dirname "$0")/../.."

PIN=b25667b297c036e86c80a51a9594b10cd41644ac
BASE="https://raw.githubusercontent.com/janpfander/llm_predictions_megastudy/$PIN"
DEST="${ORGANIZER_CODE_DEST:-idea_03/run/inputs/organizer_code}"   # idea_04 passes its own
mkdir -p "$DEST"

curl -fsSL "$BASE/R/functions/statistics.R"          -o "$DEST/statistics.R"
curl -fsSL "$BASE/preregistration_benchmark.qmd"     -o "$DEST/preregistration_benchmark.qmd"
printf 'commit=%s\nfetched_at=%s\nsource=janpfander/llm_predictions_megastudy\nlicense=none declared - do not redistribute; fetch via this script\n' \
    "$PIN" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$DEST/PIN.txt"

cat > "$DEST/README.md" <<'EOF'
# Organizer scoring code (read-only reference)

`statistics.R` + `preregistration_benchmark.qmd` are the benchmark's actual scoring
pipeline, pinned to the commit named in PIN.txt. This is how every submission — yours
included — will be scored: sections, metrics (r within outcomes, r_adj, directional
half-credit for predicted zeros, calibration), floors, the Human-2 replication row,
cluster bootstrap. Read it before predicting anything.

Provenance and the line-by-line comparison against this repo's frozen Python metrics:
docs/organizer-code-comparison-2026-08-27.md (identical math on all decision metrics).
EOF
echo "fetched organizer code @ $PIN -> $DEST"
