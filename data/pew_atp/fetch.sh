#!/bin/sh
# Fetch the Pew American Trends Panel waves used by this repo (W42, W100, W114)
# from TheARDA's public OSF mirrors into data/pew_atp/downloads/.
#
# The raw files are NOT committed: the Pew EULA (as distributed via ARDA)
# permits research use only and forbids redistribution. Run this script to
# reproduce the downloads/ folder; every file is verified against a pinned
# sha256 computed at first download (2026-08-15).
#
# Usage: sh data/pew_atp/fetch.sh

set -eu

cd "$(dirname "$0")"
mkdir -p downloads/w114 downloads/w42 downloads/w100

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

# W114 - COVID-19, Scientists and Religion (Sept 2022, n=10,588)
fetch "https://osf.io/download/qc9pn" downloads/w114/ATP_W114.sav \
    ee175232a05378a790b0a44e5937da97f4f365891e41bce151482f013766f143
fetch "https://osf.io/download/whfdp" downloads/w114/ATP_W114_codebook.txt \
    7cfd8110dbee3cd814caf5c9fe8fde815f88efaa49f733c78f8bca02a59693cb
fetch "https://www.thearda.com/ARDA/pdf/originalCodebooks/ATPW114.pdf" \
    downloads/w114/ATP_W114_instrument.pdf \
    d3879be8cee8cc5107bcfc412a2412175ee30975737880224c2f25fbf78ccf74

# W42 - Trust in Science (Jan 2019, n=4,464)
fetch "https://osf.io/download/zhvbk" downloads/w42/ATP_W42.sav \
    d246ead79c9d301d168f71197a3eeeacf4507d9caca35f17e88e12caf133864f
fetch "https://osf.io/download/38j74" downloads/w42/ATP_W42_codebook.txt \
    3b4824306c102dc2fcf59a1677eef295d067a96203838469763dbab99b1f6bc5

# W100 - Black and Hispanic Perspectives on Science and Society (late 2021, n=14,497)
fetch "https://osf.io/download/7tv62" downloads/w100/ATP_W100.sav \
    77f37b1c448912459e30243dbbb0e7a334b391679baa699f72f377a5b6a71249
fetch "https://osf.io/download/kjmnz" downloads/w100/ATP_W100_codebook.txt \
    348847d8fd2fd159e1a658e3d8f726d83250d6f87894caa721340e270c60ecce

if [ "$fail" -ne 0 ]; then
    echo "FAILED: one or more files did not match their pinned sha256." >&2
    exit 1
fi
echo "All Pew ATP files present and verified."
