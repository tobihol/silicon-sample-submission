# Spampatti, Hahnel, Trutnevyte & Brosch 2023 — Psychological inoculation strategies to fight climate disinformation across 12 countries

## Version

OSF project "Open repository for Psychological inoculation strategies to
fight climate disinformation around the world" (https://osf.io/m58zx/),
selected osfstorage contents as of 2026-08-16 (project last modified on OSF
2023-09-28). Canonical files: US raw data https://osf.io/download/ph6n2/,
merged preprocessed data https://osf.io/download/6hdz5/, survey QSF
https://osf.io/download/yvfma/. Downloaded 2026-08-16 via the OSF API (no
account required).

Paper citation: Spampatti, T., Hahnel, U. J. J., Trutnevyte, E., &
Brosch, T. (2023). Psychological inoculation strategies to fight climate
disinformation across 12 countries. Nature Human Behaviour.

License: CC-By Attribution 4.0 International (set on the OSF project).
Cleanly reusable with attribution; per house policy raw survey data is
still fetched, not committed, and never deposited.

## Contents

Selected from OSF osfstorage, mirrored under `downloads/` with the
project's folder structure. Skipped: the 11 non-US per-country RAW CSVs,
`Data/RAW/UK_IDs.csv`, and the `Stimuli_Validation` and
`Materials/Tweet_Images` folders.

- `downloads/Data/RAW/Showdown_USA_RAW.csv` — US raw Qualtrics export,
  919 rows × 943 columns. Plain single header row (no Qualtrics
  question-text/ImportId metadata rows). 834 randomized respondents
  across the 8 arms plus 85 early dropouts with `Condition` empty.
- `downloads/Data/Preprocessed/Showdown.csv` — merged cleaned data, all
  12 countries, 6,816 rows × 161 columns; exactly 568 respondents per
  country (the authors equalized country n), all 8 arms.
- `downloads/Data/Preprocessed/Showdown_short.csv` — 5,948 rows × 162
  columns; same as above minus the pure-control arm (−1), which saw no
  disinformation statements.
- `downloads/Data/Preprocessed/Showdown_MLM.csv` — trial-level long
  format for the multilevel models, 118,960 rows × 23 columns
  (5,948 participants × 20 disinformation trials).
- `downloads/Data/Codebook_Spampatti_et_al.xlsx` — variable codebook,
  one sheet, ~60 variable entries with value labels.
- `downloads/Materials/Main_Survey_Spampatti_et_al.qsf` — full Qualtrics
  survey; contains the six inoculation treatment texts verbatim
  (`Inoc_*` items) plus exact wording of all outcome items.
- `downloads/Materials/Truth_Discernment_Raw.docx` — provenance document
  for the 20-statement truth discernment task: the raw ChatGPT output
  (with the authors' queries in blue) used to generate the statements.
  Not a clean stimulus list; final item wordings are in the QSF.
- `downloads/OSF_Script_Spampatti_et_al.R` — the authors' full analysis
  script (preprocessing, ANOVAs, MLMs).

Key variables (verified against the data and the codebook):

- Design: `Condition` with 8 levels — −1 = Pure control, 0 = Passive
  control, 1 = Scientific consensus, 2 = Trust in scientists,
  3 = Transparent communication, 4 = Moralization, 5 = Accuracy,
  6 = Positive emotions inoculation. US raw randomized counts:
  −1: 100, 0: 101, 1: 101, 2: 106, 3: 103, 4: 111, 5: 105, 6: 107.
  US rows in cleaned `Showdown.csv`: 568 (per arm 65–80).
- Primary outcome: 0–100 affect-toward-climate-mitigation slider —
  `Affect_T1_1` at baseline, then `Sci_1..10_Affect_1` and
  `Act_1..10_Affect_1` after each of the 20 disinformation statements
  (10 about climate science, 10 about climate action); long-format
  `Affect` per `Trial` in `Showdown_MLM.csv`.
- Other outcomes: climate belief, 9 Likert items (`CCB_real_1..3`,
  `CCB__cause_1..3`, `CCB__cons_1..3`; averaged `CCB` 1–5); 20-item
  truth discernment (`MIST_score`, `MIST_dprime`, per-item
  `T_/F_Support_*`, `T_/F_Delay_*`); WEPT behavioral task (`WEPT_90`,
  count of pages completed at ≥90% accuracy, 0–8).
- Demographics/moderators: `Age`, `Gender` (0 = Male, 1 = Female,
  2 = Binary/other, 3 = Not disclosed), `Education` (years),
  `Pol_ideo` 1–10 left–right ideology. No US party-ID item.

## Why it is here

An 8-arm text-treatment experiment with a 0–100 slider outcome and a US
subsample — structurally close to our target: randomized verbatim text
stimuli (all six inoculation treatments are in the QSF word-for-word,
alongside every item wording), so it adds practice arms where both the
treatment texts and the measured response scale are fully known. The
repeated post-statement slider gives 21 affect measurements per person
for within-person dynamics. CC-BY 4.0 makes it cleanly reusable, though
per house policy raw data is still never committed or deposited.
Caveats: no US party-ID moderator (only 1–10 left-right `Pol_ideo`), and
modest US per-arm n (~100 raw, 65–80 in the cleaned data).
