#!/bin/sh
# Fetch the Wellcome Global Monitor 2018 and 2020 public-use files (plus
# documentation) from Wellcome's CMS into data/wellcome/downloads/.
#
# The raw files are NOT committed (they are 5.9 MB + 52.6 MB, world-wide
# samples of which we only use the U.S. rows). Run this script to reproduce
# the downloads/ folder; every file is verified against a pinned sha256
# computed at first download (2026-08-24). Wellcome's CMS returns 403 to
# non-browser User-Agents, hence the -A header.
#
# Usage: sh data/wellcome/fetch.sh
# Then:  uv run --with pandas --with openpyxl python data/wellcome/extract_us.py

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
    # fetch <url> <dest> <sha256>
    url=$1; dest=$2; want=$3
    if [ -f "$dest" ] && [ "$(sha256 "$dest")" = "$want" ]; then
        echo "ok (cached)   $dest"
        return 0
    fi
    echo "downloading   $dest"
    curl -fsSL -A "$UA" -o "$dest" "$url"
    got=$(sha256 "$dest")
    if [ "$got" = "$want" ]; then
        echo "ok (verified) $dest"
    else
        echo "SHA256 MISMATCH for $dest" >&2
        echo "  expected: $want" >&2
        echo "  got:      $got" >&2
        fail=1
    fi
}

# --- 2018 wave (Wellcome Global Monitor 2018; 144 countries, n=149,014) ---
# Single xlsx: sheets 'Crosstabs all countries', 'Full dataset', 'Data dictionary'
fetch "https://cms.wellcome.org/sites/default/files/wgm2018-dataset-crosstabs-all-countries.xlsx" \
    downloads/wgm2018-dataset-crosstabs-all-countries.xlsx \
    8bcbacd403a4ee531a526913364c163005be6b497ee429214ec2dd6d7a500c90
fetch "https://cms.wellcome.org/sites/default/files/wgm2018-questionnaire.pdf" \
    downloads/wgm2018-questionnaire.pdf \
    c0dd7669e636139f10494e265622bec7c7eba7f21dec9f6466e64f4d001c65b0
fetch "https://cms.wellcome.org/sites/default/files/wgm2018-methodology.pdf" \
    downloads/wgm2018-methodology.pdf \
    2e37d365ce059f8638cb282e495cb22a26339d8838dd74541475976a8c592d64

# --- 2020 wave (Wellcome Global Monitor 2020 / COVID-19; 113 countries, n=119,088) ---
# zip containing one csv: 'wgm_full_wave2_public_file_final (1)_csv.csv'
fetch "https://cms.wellcome.org/sites/default/files/2021-11/wgm_full_wave2_public_file.zip" \
    downloads/wgm_full_wave2_public_file.zip \
    b8ef272ff38a78dcc1dd8a9e1aeb51682c963edef2e42b5df522bf1994ca8991
fetch "https://cms.wellcome.org/sites/default/files/2021-11/wgmdata-covid-data-dictionary-user-guide.docx" \
    downloads/wgmdata-covid-data-dictionary-user-guide.docx \
    12860196e34bbb6e7bb8c7f727f810607e62048d6b38117d056485eb65a14e97
fetch "https://cms.wellcome.org/sites/default/files/2021-11/WGM_Full_Questionnaire.pdf" \
    downloads/WGM_Full_Questionnaire_2020.pdf \
    05369ff739a452d6811532f5488aa46763a70523e2a9faeb316a91e63ea37d90
fetch "https://cms.wellcome.org/sites/default/files/2021-10/wgm2020-methodology.pdf" \
    downloads/wgm2020-methodology.pdf \
    65d9b946f2203a49f2dfc7b1562138acfcdd15b537751dddf7e13c6863eafb32

if [ "$fail" -ne 0 ]; then
    echo "FAILED: one or more files did not match their pinned sha256." >&2
    exit 1
fi
echo "All Wellcome Global Monitor files present and verified."
