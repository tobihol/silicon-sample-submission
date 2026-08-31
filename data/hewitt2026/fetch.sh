#!/bin/sh
# Reproduce data/hewitt2026/downloads/capsule/ from the public Code Ocean
# capsule 9843791 (Hewitt, Ashokkumar, Ghezae & Willer, Nature 2026,
# "Predicting Results of Social Science Experiments Using Large Language
# Models"), version 1.0, commit 10f2140ab6f49e004c3bd107420babade9c8213f.
#
# Route: anonymous `git clone https://git.codeocean.com/capsule-9843791.git`
# (no login, no browser; verified working 2026-08-24). The data are CC0 1.0
# and the code MIT, so redistribution would be allowed; the raw copy still
# lives in the gitignored downloads/ folder by repo convention.
#
# After cloning, this script PRUNES the capsule to the files this repo uses
# and deletes every model-output / forecast / survey file (see README.md
# "What was deleted and why"), then strips .git so the deleted files cannot be
# recovered from git objects, and verifies sha256 of every kept file.
#
# Usage: sh data/hewitt2026/fetch.sh

set -eu

cd "$(dirname "$0")"

REPO="https://git.codeocean.com/capsule-9843791.git"
COMMIT="10f2140ab6f49e004c3bd107420babade9c8213f"
DEST="downloads/capsule"

sha256() {
    if command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "$1" | awk '{print $1}'
    else
        sha256sum "$1" | awk '{print $1}'
    fi
}

verify() {
    # verify <path> <sha256>
    if [ ! -f "$1" ]; then echo "MISSING  $1" >&2; fail=1; return; fi
    got=$(sha256 "$1")
    if [ "$got" = "$2" ]; then
        echo "ok       $1"
    else
        echo "SHA256 MISMATCH for $1" >&2
        echo "  expected: $2" >&2
        echo "  got:      $got" >&2
        fail=1
    fi
}

fail=0

if [ ! -f "$DEST/data/rct_responses.RDS" ]; then
    echo "cloning $REPO -> $DEST"
    mkdir -p downloads
    rm -rf "$DEST"
    GIT_TERMINAL_PROMPT=0 git clone --quiet "$REPO" "$DEST"
    (
        cd "$DEST"
        git checkout --quiet "$COMMIT"
        head=$(git rev-parse HEAD)
        if [ "$head" != "$COMMIT" ]; then
            echo "unexpected commit $head (wanted $COMMIT)" >&2
            exit 1
        fi
        # --- prune: never keep LLM output, forecasts, or the scientists' survey
        rm -f  data/llm_responses.RDS \
               data/forecasting_responses.RDS \
               data/gpt_author_recognition.csv \
               data/megastudies.RDS \
               data/individual_expert_predictions.rds
        rm -rf data/survey_data
        # --- prune: analysis scripts not used here (they drive the LLM pipeline)
        rm -f  code/00_requirements.R code/00_run_all_analyses.R \
               code/0_minimal_example.R code/1_main_archive1.R \
               code/2_main_archive2.R code/3_survey.R code/4_uses.R \
               code/capsule.Rproj code/config.R code/main.sh \
               code/predicting-effects-with-llms.Rproj code/run \
               code/supplement_ensemble_size.R code/supplement_table_archive1.R
        rm -rf environment .codeocean .gitignore
        # --- strip git objects so the deleted files are really gone
        rm -rf .git
    )
else
    echo "ok (cached) $DEST"
fi

# Pinned sha256 of every kept file (computed 2026-08-24 from commit 10f2140).
verify "$DEST/data/rct_responses.RDS"          4c7e28206585972bc8ee2d6ea838204f0a5679febd0591105a7553375ba1b36b
verify "$DEST/data/RA_hypotheses.RDS"          70f6ebe388f2488f8624774ab1e8a2f3722afc5f7a9e3808bd2d81c754eaeea6
verify "$DEST/data/RA_outcome_features.csv"    594371ca375687cfb8adb3ac826f797b40d59aa09e78b6e3b25365f2c3245c8a
verify "$DEST/data/RA_study_features.csv"      f61b466932c3fe73d4106e5cf66980fd9a8893f5a67d4ca80835bedbcac472ae
verify "$DEST/data/LICENSE"                    36ffd9dc085d529a7e60e1276d73ae5a030b020313e6c5408593a6ae2af39673
verify "$DEST/code/LICENSE"                    82751d23fd427c7db35e30ebbca99cee5d1bcd2d883688021b1d07120662b0fd
verify "$DEST/code/README.md"                  272fda4c3904ee9c38842c30073ee0539ed276af4a7aeb9c18fd1cba993ffab2
verify "$DEST/code/PLOT_DATA_CODEBOOK.docx"    9d77317d41c45ad1abc4bb7beaf9189ca88c3a835a3a0dbb9c069cd4b63cfccf
verify "$DEST/code/util.R"                     26be019d432baf2332a64946d2987274996237d8ee4fadc81b4dffbe44bcc068
verify "$DEST/code/load_archive1_results.R"    630e61fe7bef1e866027b1a182e920db06b7cdea55f8719e99e742ec3d22cc76
verify "$DEST/code/5_heterogeneity_archive1.R" 6b06b12f74e0d8ea1b8babb4f80878dbf2d974e81412f61ff19bc198b5257d7b
verify "$DEST/metadata/metadata.yml"           02f1c2651e4338b3fc4ea249b0e09a84c688b00a4ed1356a1d1bcecfefc4cf18

# Assert the pruned files are really absent.
for f in data/llm_responses.RDS data/forecasting_responses.RDS \
         data/gpt_author_recognition.csv data/megastudies.RDS \
         data/individual_expert_predictions.rds data/survey_data .git; do
    if [ -e "$DEST/$f" ]; then
        echo "PRUNE FAILED: $DEST/$f still present" >&2
        fail=1
    fi
done

if [ "$fail" -ne 0 ]; then
    echo "FAILED: one or more files did not verify." >&2
    exit 1
fi
echo "All hewitt2026 files present, pruned and verified."
