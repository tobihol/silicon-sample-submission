#!/bin/sh
# Fetch the ANES Time Series 2020 and 2024 CSV releases (plus the accessible
# HTML codebooks) from electionstudies.org into data/anes/downloads/.
#
# The raw files are NOT committed: the ANES terms of use permit research use
# with citation and forbid re-identification, and grant no explicit
# redistribution licence. Run this script to reproduce the downloads/ folder;
# every file is verified against a pinned sha256 computed at first download
# (2026-08-24). The zips are unpacked in place after verification.
#
# electionstudies.org sits behind Cloudflare bot management:
#   - default curl gets HTTP 403; a browser User-Agent AND HTTP/1.1
#     (--http1.1) got HTTP 200 on 2026-08-24 (HTTP/2 + same UA still 403);
#   - even then some requests are intermittently refused with 403, so each
#     download is retried up to 5 times with a short pause;
#   - Cloudflare's email obfuscation rewrites the two e-mail addresses in the
#     HTML codebooks with a per-request random key, so the HTML files are
#     hashed AFTER blanking the `email-protection#<hex>` and
#     `data-cfemail="<hex>"` tokens (the bytes on disk vary from download to
#     download, the content does not).
#
# Usage: sh data/anes/fetch.sh

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

# sha256 of an HTML file with Cloudflare's per-request email-obfuscation
# keys blanked out (see header comment).
sha256_html() {
    if command -v shasum >/dev/null 2>&1; then
        cf_normalise "$1" | shasum -a 256 | awk '{print $1}'
    else
        cf_normalise "$1" | sha256sum | awk '{print $1}'
    fi
}
cf_normalise() {
    sed -e 's/email-protection#[0-9a-f]*/email-protection#X/g' \
        -e 's/data-cfemail="[0-9a-f]*"/data-cfemail="X"/g' "$1"
}

fail=0

download() {
    # download <url> <dest>  (up to 5 attempts; Cloudflare 403s are intermittent)
    url=$1; dest=$2; n=1
    while :; do
        if curl -fsSL --http1.1 -A "$UA" -o "$dest.part" "$url"; then
            mv "$dest.part" "$dest"
            return 0
        fi
        rm -f "$dest.part"
        if [ "$n" -ge 5 ]; then
            echo "download failed after $n attempts: $url" >&2
            return 1
        fi
        echo "  attempt $n failed, retrying in 5s ..."
        n=$((n + 1))
        sleep 5
    done
}

fetch() {
    # fetch <url> <dest> <sha256> [hashfn]
    url=$1; dest=$2; want=$3; hashfn=${4:-sha256}
    if [ -f "$dest" ] && [ "$($hashfn "$dest")" = "$want" ]; then
        echo "ok (cached)   $dest"
        return 0
    fi
    echo "downloading   $dest"
    download "$url" "$dest" || { fail=1; return 0; }
    got=$($hashfn "$dest")
    if [ "$got" = "$want" ]; then
        echo "ok (verified) $dest"
    else
        echo "SHA256 MISMATCH for $dest" >&2
        echo "  expected: $want" >&2
        echo "  got:      $got" >&2
        fail=1
    fi
}

BASE="https://electionstudies.org/wp-content/uploads"

# ANES 2020 Time Series Study, full release CSV (2022-02-10), 8,280 pre / 7,449 post
fetch "$BASE/2022/02/anes_timeseries_2020_csv_20220210.zip" \
    downloads/anes_timeseries_2020_csv_20220210.zip \
    70450eb6bf7b8f34cbf53fbeb99d43f45ce154a42b8e187bec7270f34f1bbfda
fetch "$BASE/2026/04/anes_timeseries_2020_userguidecodebook_accessible_html.html" \
    downloads/anes_timeseries_2020_userguidecodebook_accessible_html.html \
    c86dd06720d0a73c9c012b3a7dd15f03ee248d87f576d7db64058f9ecf00f68a sha256_html

# ANES 2024 Time Series Study, full release CSV (2026-05-19), 5,521 pre / 4,964 post
fetch "$BASE/2026/05/anes_timeseries_2024_csv_20260519.zip" \
    downloads/anes_timeseries_2024_csv_20260519.zip \
    31082da127f1ebcfb1d2736ba650d52cd67a4a6ab13fbe639c2db2515779773c
fetch "$BASE/2026/04/anes_timeseries_2024_userguidecodebook_accessible_html.html" \
    downloads/anes_timeseries_2024_userguidecodebook_accessible_html.html \
    ffbfaed474df73673b686dee6e8461f47eb4571b4587922874ae428b75ad7c28 sha256_html

if [ "$fail" -ne 0 ]; then
    echo "FAILED: one or more files could not be fetched or did not match their pinned sha256." >&2
    exit 1
fi

# Unpack the verified zips (each contains one CSV + the PDF codebook) and
# check the CSVs against their pinned sha256.
unpack() {
    # unpack <year> <zip> <csv-basename> <csv-sha256>
    year=$1; zip=$2; csv=$3; want=$4
    dir=downloads/anes_timeseries_${year}_csv
    if [ -f "$dir/$csv" ] && [ "$(sha256 "$dir/$csv")" = "$want" ]; then
        echo "ok (unpacked) $dir/$csv"
        return 0
    fi
    echo "unpacking     $zip -> $dir"
    unzip -o -q "$zip" -d "$dir"
    got=$(sha256 "$dir/$csv")
    if [ "$got" = "$want" ]; then
        echo "ok (verified) $dir/$csv"
    else
        echo "SHA256 MISMATCH for $dir/$csv (expected $want, got $got)" >&2
        fail=1
    fi
}
unpack 2020 downloads/anes_timeseries_2020_csv_20220210.zip anes_timeseries_2020_csv_20220210.csv \
    9e7a4d585fa88ef39b82e47e18948663155f959c648704fb737d34749be35e8c
unpack 2024 downloads/anes_timeseries_2024_csv_20260519.zip anes_timeseries_2024_csv_20260519.csv \
    f80a276e64a5653abd6a9d1dcd96b94717367d39b21152630fa9e30c46cf30d7

if [ "$fail" -ne 0 ]; then
    exit 1
fi
echo "All ANES files present and verified."
