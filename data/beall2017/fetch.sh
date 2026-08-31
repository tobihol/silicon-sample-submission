#!/bin/sh
# Fetch the Beall, Myers, Kotcher, Vraga & Maibach (2017, PLOS ONE) deposit
# from Zenodo, plus the paper's S1 Appendix (stimuli + questionnaire) from
# PLOS, into data/beall2017/downloads/.
#
# The raw files are NOT committed (repo policy: data/*/downloads/ is
# gitignored). Both sources are CC BY 4.0, so re-fetching is unrestricted.
# Every file is verified against a pinned sha256 computed at first download
# (2026-08-24); the two Zenodo md5s also match the record metadata
# (02e9942b8cd7a63c5594e2b82ed786e5, da9d983803ee8877bb59cb2ddd484c9c).
#
# Usage: sh data/beall2017/fetch.sh

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

# Zenodo record 495653 (v1, 2017-04-08) - Qualtrics export, 2,453 x 47
fetch "https://zenodo.org/api/records/495653/files/PLOS%20ONE%20Data.sav/content" \
    "downloads/PLOS ONE Data.sav" \
    728d3941a190f7ae6417c163da63dff0e611d09eee9da20b1f1b0bb8716bf99f

# Zenodo record 1407096 (v2 of the same concept record 794991) - the authors'
# reduced analysis file with Topic / Position / Credibility already derived
# (2,453 x 24). Used here only to cross-check the reconstruction rule.
fetch "https://zenodo.org/api/records/1407096/files/Updated%20Plos%20One%20Data.sav/content" \
    "downloads/Updated Plos One Data.sav" \
    aea77e75c9cb13d4f8cf4c86b7fe966ffe0a49d70314b9b1a24ca85a35713826

# PLOS ONE S1 Appendix (doi:10.1371/journal.pone.0187511.s001): the 12
# verbatim stimuli (Appendix 1A) and the questionnaire (Appendix 1B).
fetch "https://journals.plos.org/plosone/article/file?type=supplementary&id=10.1371/journal.pone.0187511.s001" \
    downloads/pone.0187511.s001.docx \
    8bb42bb978f343703309d87c8c745fde74a2757dd8aae24bd819a3dd99fed208

if [ "$fail" -ne 0 ]; then
    echo "FAILED: one or more files did not match their pinned sha256." >&2
    exit 1
fi
echo "All beall2017 files present and verified."
