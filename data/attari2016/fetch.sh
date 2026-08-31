#!/bin/sh
# Fetch the three Attari, Krantz & Weber (2016, 2019) experiment workbooks from
# the first author's publications page (https://www.szattari.com/publications)
# into data/attari2016/downloads/.
#
# The raw workbooks are NOT committed: the page states no licence and carries
# the disclaimer "for educational use only", so the respondent-level files are
# disk-only. Run this script to reproduce downloads/, then
# `uv run --with pandas --with openpyxl --with xlrd python data/attari2016/build_derived.py`
# to rebuild the PII-free derived CSVs in downloads/derived/. Every file is
# verified against a pinned sha256 computed at first download (2026-08-24).
#
# Do NOT fetch SimpleInterventions_Data.xlsx from the same page: it is the
# Marghetis et al. 2019 energy dataset, not a credibility experiment.
#
# Usage: sh data/attari2016/fetch.sh

set -eu

cd "$(dirname "$0")"
mkdir -p downloads/derived

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

# Attari, Krantz & Weber 2016 (Climatic Change 138:325-338): Survey 1 (Oct 2014,
# n=2,028, 7 arms) + Survey 2 (Dec 2014, n=2,915, 11 arms) in one workbook.
fetch "https://www.szattari.com/s/Ad_Hom_Final.xls" downloads/Ad_Hom_Final.xls \
    c77558415d2c4e54c86d31f72252270975527ef20f755f15f35eb905f8b4adc9

# Attari, Krantz & Weber 2019 (Climatic Change 154:529-545), Study 1: policy
# support x researcher footprint (May 2017, n=3,646, 12 arms). Contains ZIP codes.
fetch "https://www.szattari.com/s/Study1_Policy.xlsx" downloads/Study1_Policy.xlsx \
    aec1c4aa8bd51e87d226c319fad21ff6c27482ce079e41aea11b8e6bf524e86a

# Attari, Krantz & Weber 2019, Study 2: credibility lost/regained via reform
# (Mar 2016, n=1,772, 6 arms).
fetch "https://www.szattari.com/s/Study2_Reformation.xls" downloads/Study2_Reformation.xls \
    1bac4e065174d04a3255ca0968024121d096a213704e473ffeba09b9b0310114

if [ "$fail" -ne 0 ]; then
    echo "FAILED: one or more files did not match their pinned sha256." >&2
    exit 1
fi
echo "All Attari 2016/2019 workbooks present and verified."
echo "Next: uv run --with pandas --with openpyxl --with xlrd python build_derived.py"
