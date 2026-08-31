# Bago, Muller & Bonnefon 2025 — LLM-personalized climate headlines

## Version

GitHub repository bencebago/climate_headlines_personalization
(https://github.com/bencebago/climate_headlines_personalization), `data/`
directory at `main` (commit 6c68342, 2025-08-06). Downloaded 2026-08-19
via raw.githubusercontent.com. Archived snapshot (v1.0) on Zenodo:
concept DOI 10.5281/zenodo.16755109 (version DOI 10.5281/zenodo.16755110).

Paper citation: Bago, B., Muller, P., & Bonnefon, J.-F. (2025). Using
generative AI to increase sceptics' engagement with climate science.
Nature Climate Change. https://doi.org/10.1038/s41558-025-02424-9

License: **CC BY 4.0** (set on the Zenodo archive of the repository; the
GitHub repo itself carries no license file).

## Contents

The four files of the repo's `data/` directory, under `downloads/`:

- `downloads/anonim_df.csv` — participant-level (wide) Qualtrics export,
  **2,002 rows × 133 columns**. 1,999 real participants; **3 all-NaN junk
  rows (NaN `prolific` and NaN `condition`) — drop them.** Verified:
  - `condition`: personal (1,002) vs original (997) — LLM-personalized vs
    original climate headlines, randomized between subjects.
  - Six 0–100 belief sliders, pre and post: `prior_/posterior_happen_1`
    (probability climate change is happening), `prior_/posterior_cause_1`
    (caused by humans), `prior_/posterior_risk_1` (threat significance);
    all span the full 0–100 range, no missings among real participants.
  - Skeptic-heterogeneity variables: `climate1` (happening? 1,717 yes /
    141 no / 141 don't know), `climate2` (cause; 1,414 human / 412
    natural / 173 other), `Q6..Ideology_econ` + `Q7..Ideology_social`
    (coded 1–6 in this file), `DemRep_C` (1–6, Strongly Dem → Strongly
    Rep).
  - Behavior: per-headline `vote0..19`, `bookmarked0..19`, `title0..19`,
    `selectedValue` (self-selected article read), `bookmark_regret_1`,
    `upvote_regret`, `credibility_1` (0–100 trust in the read article).
  - Demographics: `Educational.Level` (1–8). **No income variable
    anywhere in the deposit.**
- `downloads/climate_headlines_processed.csv` — long format,
  **semicolon-delimited** (`sep=";"`), **40,000 rows × 32 columns** =
  2,000 participants × 20 headlines (21,989 climate / 18,011 neutral
  rows; 28 unique climate `item_nr`). Adds the composite `Ideology`
  (mean of econ + social, −2…2 in 0.5 steps — the codebook's coding) and
  per-row `vote` / `bookmarked` / `bookmarkorder`.
- `downloads/README.md` — the authors' codebook. NB it describes the
  *processed long file*, and with three slips: the social-ideology column
  is `Q7..Ideology_social` (not `Q6..`), and in `anonim_df.csv` ideology
  and `DemRep_C` are coded 1–6 (not the −2…2 / −3…3 stated).
- `downloads/prolific_export_667bcfe8d8e8186ce82f5edf.csv` — Prolific
  metadata, **2,107 rows × 22 columns** (1,030 APPROVED + 968 AWAITING
  REVIEW ≈ the 1,999 analyzed; plus RETURNED/TIMED-OUT). Join on
  `Participant id` = `prolific` for Age, Sex, Ethnicity, U.S. political
  affiliation, employment status.

Not vendored (in the repo/Zenodo if needed): the raw Qualtrics CSV,
`analysis/` R code, and the headline-corpus JSON files at the repo root.

## Why it is here

The only vendored experiment using **LLM-generated climate text as a
randomized treatment** with continuous **0–100 pre/post belief sliders**
(happening / human-caused / risk) and measured prior-belief
heterogeneity — the paper's engagement and belief effects are strongest
among climate sceptics, making it an HTE-curve asset (effect as a
function of prior belief) and a response-format asset alongside
`orchinik2024`/`sce`. Caveats: the treatment is
personalization-for-engagement (upvotes/bookmarks of headlines), not a
persuasive appeal, so belief ATEs are not message-persuasion ATEs; no
income variable; and post sliders follow reading a *self-selected*
article, so belief change is partly conditional on engagement — analyze
as ITT under randomized condition.

## PII caveat (audit 2026-08-24)

`downloads/prolific_export_667bcfe8d8e8186ce82f5edf.csv` contains a `Participant id`
column of live Prolific PIDs joined to demographics, and `downloads/anonim_df.csv`
retains `RecipientEmail`/`RecipientFirstName`/`RecipientLastName`/`ExternalReference`/
`prolific` columns despite its name. Both are gitignored (`data/*/downloads/`) and must
stay disk-only: never commit, deposit, quote identifiers from, or upload these files
anywhere. Analysis should use the outcome columns only.
