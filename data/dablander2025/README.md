# Dablander, Sachisthal & Aron 2025 — Effects of climate protests by environmental scientists

## Version

OSF project "Out of the Labs and into the Streets: Effects of Climate
Protests by Environmental Scientists" (https://osf.io/ktjh6/), osfstorage
contents as of 2026-08-19 (project last modified on OSF 2025-05-06). Main
data file: https://osf.io/download/mf7ep/ (`dat_num_all.csv`). Downloaded
2026-08-19 via the OSF API (no account required). The vignette texts are
not on OSF; they are in the paper's electronic supplementary material,
mirrored here from the Royal Society's Figshare deposit
(https://doi.org/10.6084/m9.figshare.c.7776120, file
`rsos241001_si_001.pdf`).

Paper citation: Dablander, F., Sachisthal, M. S. M., & Aron, A. R. (2025).
Out of the labs and into the streets: Effects of climate protests by
environmental scientists. Royal Society Open Science, 12(4), 241001.
https://doi.org/10.1098/rsos.241001 (Registered Report; PMCID
PMC12035554.)

License: the article and its supplementary material (the ESM PDF with the
vignettes) are CC BY 4.0. The OSF project itself has no license attached
(`node_license` is empty) — data are cited only, kept here privately for
research use, never re-hosted.

## Contents

From OSF osfstorage, mirrored under `downloads/` with the project's folder
structure (compiled `analysis.html`, 19 MB, and the `results/` RDS files
and `figures/` PDFs were skipped); the ESM PDF added under
`downloads/esm/`:

- `downloads/data/dat_num_all.csv` — main experiment microdata, numeric
  Qualtrics export, 3,359 rows × 34 columns (the canonical file at
  osf.io/download/mf7ep)
- `downloads/data/dat_text.csv` — text-labeled export of the same survey,
  3,148 rows × 34 columns (use for value labels; slightly fewer rows than
  the numeric file)
- `downloads/data/demographics_all.csv` — Prolific-side demographics
  (Age, Sex, U.S. political affiliation), 3,416 rows × 4 columns, joined
  to the survey on `SESSION_ID` = `Submission.id`
- `downloads/data/openAnswers_coded.csv` — hand-coded open answers
  (`Usable`, `Check`, `MentionsScientist`), 2,874 rows × 5 columns; drives
  the coherence exclusions
- `downloads/analysis.Rmd`, `helpers.R`, `analysis_stage1.R`,
  `power_analysis.R` — the authors' full analysis code (de-facto codebook:
  exclusion pipeline, factor construction, Bayesian ordinal models)
- `downloads/models/df_effects_donation.csv` — posterior effect summaries
  for the donation outcome
- `downloads/esm/rsos241001_si_001.pdf` — electronic supplementary
  material (CC BY 4.0): verbatim vignette texts, consent and debrief
  wording, design table, exclusion breakdown, full demographics tables
- `downloads/README.md` — the authors' repository README

Design and key variables (verified against the data and the ESM):

- US Prolific sample, representative on age and sex, October 2024.
  N = 3,359 raw; the paper's pipeline (Progress == 100, then attention
  check, then open-answer coherence) reproduces exactly: 2,875 after the
  attention check, n = 2,856 analyzed.
- 6 arms, 2×3 between-subjects factorial: protest type {Legal march,
  Civil Disobedience} × scientist involvement {None, Endorse, Join}.
  `condition` values `V_LegalXNone`, `V_LegalXEndorse`, `V_LegalXJoin`,
  `V_CDXNone`, `V_CDXEndorse`, `V_CDXJoin`; randomized n = 559–561/arm.
  After exclusions the arms are unbalanced (398–524/arm): 85% of the 274
  attention-check failures are in the civil-disobedience arms (worst:
  CD×Endorse, 22.5% excluded).
- Vignettes: fictional news article based on real NYC protests of fall
  2023 — a peaceful Midtown march vs. a Federal Reserve blockade with
  100+ arrests, both demanding a stop to new oil and gas drilling. All
  six versions include the same science-context paragraph ("Scientists
  say the world needs to limit warming to 1.5 degrees Celsius … the
  International Energy Agency (IEA) says that no new oil and gas fields
  can be explored"). The scientist is the fictional "Dr. Alex Fraser,
  Environmental scientist at Rochester University", who either joins the
  protest (and, in CD, is arrested) or endorses it in quotes; verbatim
  texts in `downloads/esm/rsos241001_si_001.pdf`, pp. 7–9.
- Outcomes, all single-item 1–5 Likert: `PolicySupport` ("offshore
  drilling … should be expanded", strongly disagree–strongly agree),
  `ActivistSupport`, `Radical` (perceived radicalness),
  `SourceCredibility` (trust in Dr. Fraser as a source on climate change
  — only asked in the four scientist arms, 2,106 non-missing) and
  `ScienceCredibility` (trust in environmental scientists in general).
- Behavioral outcome: `Donation_1`, 0–100 slider allocating a potential
  $100 bonus (10 participants were actually drawn and paid) to one of
  eight climate NGOs; `Donation_NGO` (1–8) records the chosen NGO.
- Moderators/demographics: `Gender` (5), `Age` (8 brackets 18–24 … 75+
  plus prefer-not-to-say), `Ethnicity`, `Income` (13), `EducationLevel`
  (7), `PoliticalAffiliation` (5: Democrat, Democrat leaning,
  Independent, Republican leaning, Republican; the authors collapse
  leaners into Democrat/Republican — analyzed split 1,119 D / 889 I /
  848 R).

## Why it is here

Registered-report nulls on the scientist-credibility outcomes: an
environmental scientist endorsing or even joining a protest (including
civil disobedience with arrest) neither dented his own credibility nor
general science credibility, and did not move policy support — a directly
usable calibration prior for small/null trust effects. Design-wise the
closest open analogue to the target: a 6-arm vignette experiment with
BOTH a scientist-credibility outcome family AND a 0–100 behavioral
donation measure (the target has `donation_ams` 0–10), plus all six
target moderators (gender, age, ethnicity, income, education, political
affiliation). Caveats: outcomes are single-item 5-point Likert scales
(not sliders), the stimuli are news-article vignettes rather than
messages, and the Prolific sample is representative only on age and
gender (by the survey's own measure it over-represents Democrats
relative to Prolific's stratification).
