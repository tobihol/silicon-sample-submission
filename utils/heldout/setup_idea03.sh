#!/usr/bin/env bash
# One-shot idea_03 setup: assembles everything the launcher and oracle need that is not in
# git (carves, halves, briefs, idea01_lib, organizer code) and verifies the frozen
# signature. Idempotent — safe to re-run. See idea_03/README.md for the full runbook.
set -euo pipefail
cd "$(dirname "$0")/../.."

echo "== 1/6 full carves (data/<task>/carved/) =="
need_carve=0
for t in goldwert2026 orchinik2024 kim2024 dablander2025 altenmueller2024 kerwer2025 beall2017 bbprime2025; do
    [ -f "data/$t/carved/truth.csv" ] || { echo "  missing: data/$t/carved/truth.csv"; need_carve=1; }
done
if [ "$need_carve" = 1 ]; then
    echo "  -> carving (needs fetched raw data; see data/<task>/README.md + fetch.sh)"
    uv run --with pyreadstat --with scipy utils/heldout/carve_val.py
fi

echo "== 2/6 fresh-draw halves (data/<task>/carved/halves/) =="
uv run --with pyreadstat --with scipy utils/heldout/carve_halves.py

echo "== 3/6 validation briefs -> idea_03/run/inputs/val/ =="
mkdir -p idea_03/run/inputs/val
for t in goldwert2026 orchinik2024 kim2024 dablander2025 altenmueller2024 kerwer2025 beall2017; do
    src="idea_02/run/inputs/val/$t"
    [ -d "$src" ] || { echo "  missing brief $src — carve_val.py writes it"; exit 1; }
    rm -rf "idea_03/run/inputs/val/$t"
    cp -R "$src" "idea_03/run/inputs/val/$t"
done
echo "  7 briefs copied (identical to idea_02's — same tasks, same formats)"
# idea_02's briefs state its budget ("at most 5 submissions"); idea_03's frozen budget is 2
# and the oracle enforces 2 (session-1 OPEN.md A2). Correct the copies, not the originals.
for t in goldwert2026 orchinik2024 kim2024 dablander2025 altenmueller2024 kerwer2025 beall2017; do
    python3 - "idea_03/run/inputs/val/$t/brief/task.json" <<'PY'
import json, sys
p = sys.argv[1]
d = json.load(open(p))
def fix(o):
    if isinstance(o, dict): return {k: fix(v) for k, v in o.items()}
    if isinstance(o, list): return [fix(v) for v in o]
    if isinstance(o, str): return o.replace(
        "At most 5 submissions per task per session.",
        "At most 2 scored submissions per task per run id (the scorer refuses further calls).")
    return o
json.dump(fix(d), open(p, "w"), indent=1, ensure_ascii=False)
PY
done
echo "  brief budget text corrected to the idea_03 cap (2 per run id)"

echo "== 4/6 idea01_lib (redacted idea_01 code + notes) =="
if [ ! -d idea_02/run/inputs/idea01_lib ]; then
    echo "  -> building (scanner-verified redaction)"
    uv run --with scipy utils/heldout/build_idea01_lib.py
fi
rm -rf idea_03/run/inputs/idea01_lib
cp -R idea_02/run/inputs/idea01_lib idea_03/run/inputs/idea01_lib

echo "== 5/6 organizer scoring code (pinned) =="
bash utils/heldout/fetch_organizer_code.sh

echo "== 6/6 frozen signature =="
if command -v sha256sum >/dev/null 2>&1; then H=$(sha256sum idea_03/run/.prime/agent/APPEND_SYSTEM.md | awk '{print $1}')
else H=$(shasum -a 256 idea_03/run/.prime/agent/APPEND_SYSTEM.md | awk '{print $1}'); fi
SIGNED=$(awk '{print $1}' idea_03/frozen.sha256 2>/dev/null || echo MISSING)
if [ "$H" != "$SIGNED" ]; then
    echo "  FROZEN MISMATCH: idea_03/frozen.sha256 does not sign the current APPEND_SYSTEM.md."
    echo "  If the change is intended and reviewed: utils/sign-frozen.sh idea_03"
    exit 1
fi
echo "  signature ok"

echo
echo "idea_03 is set up. Next (see idea_03/README.md):"
echo "  terminal 1:  uv run --with scipy utils/heldout/score_oracle3.py idea_03/run"
echo "  terminal 2:  SSB_IDEA=idea_03 SSB_ARM=main SSB_RUN_ID=<id> \\"
echo "               ./utils/prime/run.sh --mode json --autonomous \"\$(cat idea_03/run/TASK_01.md)\""
