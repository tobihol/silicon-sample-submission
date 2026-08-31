#!/bin/sh
# Fetch the Kerwer, Jonas, Stoll, Benz & Chasiotis (2025) plain-language-summary
# RCT deposit (PsychArchives, doi:10.23668/psycharchives.14209) into
# data/kerwer2025/downloads/.
#
# The raw files are NOT committed (data/*/downloads/ is gitignored). They are
# licensed CC-BY-SA 4.0 (share-alike): keep them as separately licensed
# material and never merge them into a permissively licensed bundle. Run this
# script to reproduce the downloads/ folder; every file is verified against a
# pinned sha256 computed at first download (2026-08-24).
#
# PsychArchives serves bitstreams from two hosts with identical bitstream ids:
# pada.psycharchives.org (linked from the record page) and www.psycharchives.org.
# On 2026-08-24 both returned 500/502/504 intermittently, never at the same
# time, so each file is tried on both hosts with retries; a run that prints a
# few "HTTP error ... retrying" lines and then "ok (verified)" is normal.
#
# Usage: sh data/kerwer2025/fetch.sh

set -eu

cd "$(dirname "$0")"
mkdir -p downloads

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

sha256() {
    if command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "$1" | awk '{print $1}'
    else
        sha256sum "$1" | awk '{print $1}'
    fi
}

fail=0

fetch() {
    # fetch <bitstream-id> <dest> <sha256>
    id=$1; dest=$2; want=$3
    if [ -f "$dest" ] && [ "$(sha256 "$dest")" = "$want" ]; then
        echo "ok (cached)   $dest"
        return 0
    fi
    echo "downloading   $dest"
    got=""
    for host in www.psycharchives.org pada.psycharchives.org; do
        for attempt in 1 2 3; do
            if curl -fsSL -A "$UA" -o "$dest" "https://$host/bitstream/$id"; then
                got=$(sha256 "$dest")
                [ "$got" = "$want" ] && break 2
                echo "  sha256 mismatch from $host (attempt $attempt), retrying" >&2
            else
                echo "  HTTP error from $host (attempt $attempt), retrying" >&2
            fi
            sleep 3
        done
    done
    if [ "$got" = "$want" ]; then
        echo "ok (verified) $dest"
    else
        echo "SHA256 MISMATCH for $dest" >&2
        echo "  expected: $want" >&2
        echo "  got:      ${got:-<download failed>}" >&2
        fail=1
    fi
}

# Record: https://psycharchives.org/en/item/25837266-04fa-40e5-b00a-24b3aff49d19
#         https://hdl.handle.net/20.500.12034/9672  (published 2024-03-01)

# Anonymised respondent-level dataset (2,451 rows x 73 columns; sep=';' decimal=',')
fetch a7ee57b4-1c4b-4a29-afc8-59aca28889df \
    downloads/20221202_ESM_dataset_publication_anonymized.csv \
    62a9dde0a48a6e676348fe97e4bc6abbae3e3e267a88455fa09058278b3ad4ba

# Codebook (73 variables; sep=';', ISO-8859-1)
fetch c1707c2e-f05e-4e77-a938-04ce67132a70 \
    downloads/20221202_ESM_Codebook.csv \
    c361260d98fb1c45eb9ff2a911bcde5da8d90b7eb44a663ed87d4c4526c7049b

# Authors' knitted R output (analysis log for the paper)
fetch 339ce463-738b-48b6-9b1d-90097c7f26b9 \
    downloads/20230921_ESM_R_Output.html \
    3ac80dd8fd7b73a3e3e12d6da5f9919e8b70da1b0029d6e7f0849c5c4a4e8e4f

exit $fail
