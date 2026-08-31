#!/bin/sh
# Fetch the open data + code appendices of Agley et al. 2021 (JMIR 23(10):e32425,
# PMC8519341; CC BY 4.0) into data/agley2021/downloads/.
#
# Primary source: the JMIR "Multimedia Appendix" download API (needs a browser
# User-Agent, otherwise it returns an HTML interstitial). Fallback: the Europe PMC
# supplementary-files bundle for PMC8519341, which contains byte-identical copies
# of app1.docx and app2.zip plus the article figures (fig1/fig2 = the two stimulus
# infographics) and app3.pdf (CONSORT-EHEALTH checklist). The bundle zip itself is
# generated on the fly (fresh timestamps), so it is NOT pinned; the files inside it
# are verified against sha256s computed at first download (2026-08-24).
#
# Usage: sh data/agley2021/fetch.sh

set -eu

cd "$(dirname "$0")"
mkdir -p downloads
cd downloads

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

JMIR_API="https://www.jmir.org/api/download"
EPMC_BUNDLE="https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8519341/supplementaryFiles"

SHA_APP1=46d60afcc7bde723da49f522906ba7d79db6dce30f41547c4f1ee48b20a43aa8
SHA_APP2=9a3e831c0fc528ace248dff5b9bc38c17f74f47abf224370f7f2b8507858814d
SHA_APP3=15e577a976f6df2dd0fd214e18be6b9b95b408bb373407df017f96bac8f692d4
SHA_FIG1=6454debdb2aef49e37a3ebde31501effb85b0d3c0398ece43a8c8aebc9c248a2
SHA_FIG2=b5614f2184627c8ab1ca29ea8046c85431b014e180d2364221719613efa19b8d
SHA_RAW=a2c8fac88144e9c370ec789e5ba3f76abc06e87d8d76cce5095bcf1e24b9e786
SHA_LPA=b699c17ce43c6fd66d8f83394ad6beff8c320a13bf0f8e2e394b3f2c802cfa44
SHA_CP=d6a17b2bf86d99c31e62a5ef2f65139c8862167d1b9423d00dc3f33b6fdcb04a

sha256() {
    if command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "$1" | awk '{print $1}'
    else
        sha256sum "$1" | awk '{print $1}'
    fi
}

ok() {
    # ok <file> <sha256>  -> 0 if file exists and matches
    [ -f "$1" ] && [ "$(sha256 "$1")" = "$2" ]
}

verify() {
    # verify <file> <sha256>  (prints, sets fail)
    if ok "$1" "$2"; then
        echo "ok (verified) $1"
    else
        echo "SHA256 MISMATCH or missing: $1" >&2
        [ -f "$1" ] && echo "  got: $(sha256 "$1")" >&2
        fail=1
    fi
}

fail=0

# --- 1. Appendices from the JMIR API (primary) ---------------------------------
for spec in "app1.docx $SHA_APP1" "app2.zip $SHA_APP2"; do
    f=${spec% *}; want=${spec#* }
    if ok "$f" "$want"; then
        echo "ok (cached)   $f"
        continue
    fi
    echo "downloading   $f (JMIR API)"
    if ! curl -fsSL -A "$UA" -o "$f" "$JMIR_API?alt_name=jmir_v23i10e32425_$f&filename=$f"; then
        echo "JMIR API download failed for $f; will fall back to the Europe PMC bundle" >&2
        rm -f "$f"
    fi
done

# --- 2. Europe PMC bundle: figures + CONSORT checklist, and fallback copies ------
need_bundle=0
for spec in "epmc/jmir_v23i10e32425_fig1.jpg $SHA_FIG1" \
            "epmc/jmir_v23i10e32425_fig2.jpg $SHA_FIG2" \
            "epmc/jmir_v23i10e32425_app3.pdf $SHA_APP3"; do
    ok "${spec% *}" "${spec#* }" || need_bundle=1
done
ok app1.docx "$SHA_APP1" || need_bundle=1
ok app2.zip "$SHA_APP2" || need_bundle=1

if [ "$need_bundle" -eq 1 ]; then
    echo "downloading   epmc_supplementaryFiles.zip (Europe PMC, unpinned bundle)"
    curl -fsSL -A "$UA" -o epmc_supplementaryFiles.zip "$EPMC_BUNDLE"
    rm -rf epmc && mkdir -p epmc
    unzip -q -o epmc_supplementaryFiles.zip -d epmc
    # fallback for the appendices if the JMIR API did not deliver them
    ok app1.docx "$SHA_APP1" || cp epmc/jmir_v23i10e32425_app1.docx app1.docx
    ok app2.zip  "$SHA_APP2" || cp epmc/jmir_v23i10e32425_app2.zip  app2.zip
else
    echo "ok (cached)   epmc/ (figures + app3.pdf)"
fi

verify app1.docx "$SHA_APP1"
verify app2.zip  "$SHA_APP2"
verify epmc/jmir_v23i10e32425_fig1.jpg "$SHA_FIG1"
verify epmc/jmir_v23i10e32425_fig2.jpg "$SHA_FIG2"
verify epmc/jmir_v23i10e32425_app3.pdf "$SHA_APP3"

# --- 3. Unzip the data appendix -----------------------------------------------
mkdir -p app2
unzip -q -o app2.zip -d app2
verify "app2/COVID Misinformation final.csv" "$SHA_RAW"
verify "app2/misinformation_LPA.csv"         "$SHA_LPA"
verify "app2/ClassProb.csv"                  "$SHA_CP"

if [ "$fail" -ne 0 ]; then
    echo "FAILED: one or more files did not match their pinned sha256." >&2
    exit 1
fi
echo "All agley2021 files present and verified."
