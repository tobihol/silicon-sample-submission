# Altenmüller, Wingen & Schulte 2024 — Explaining polarized trust in scientists: a political stereotype-approach

## Version

OSF project "Explaining polarized trust in scientists: A political
stereotype-approach" (https://osf.io/rvj4q/), full osfstorage contents as of
2026-08-17 (project last modified on OSF 2024-01-22). Downloaded 2026-08-17
via the OSF API (no account required).

Paper citation: Altenmüller, M. S., Wingen, T., & Schulte, A. (2024).
Explaining Polarized Trust in Scientists: A Political Stereotype-Approach.
Science Communication. https://doi.org/10.1177/10755470231221770

License: CC BY 4.0 (attached to the OSF node). Note the node's copyright
holder field reads "Wingen, Berkessel, & Dohle (2021)" — an artifact of the
node being created from a template project (osf.io/egkpb); the license itself
is genuine.

## Contents

All from OSF osfstorage, mirrored under `downloads/` with the project's
folder structure:

- `downloads/Data & Code/Data/rawdata_study{1,2,4a,4b}.csv` — raw Qualtrics
  exports (comma-separated, three header rows: variable names, question text,
  ImportId) for the four MTurk studies; `rawdata_study3.csv` — a
  semicolon-separated, decimal-comma subset (325 × 15, partly pre-composited)
  of a German COVID-19 dataset from a collaborator's larger project
- `downloads/Data & Code/Analysis Scripts/analysis_study{1,2,3,4a,4b}.Rmd`
  and `analysis_study5.rmd` — the authors' full analysis code (serves as the
  de-facto codebook: row-deletion counts, exclusion rules, variable recodes,
  composite construction, condition labels)
- `downloads/Materials/Qualtrics Survey Study {1,2,4a,4b}.pdf` — full survey
  instruments (exact vignette wording, item wording, response scales)
- `downloads/Preregistrations/Preregistration Study {1,2,4a,4b}.pdf` —
  anonymized AsPredicted preregistrations (Study 1 is #81146,
  aspredicted.org/PZ6_7CM; sequential-testing sampling plans, one-tailed
  tests, exclusion rules)
- `downloads/SupplementaryInformation.pdf` — supplementary figures
  (mediated-moderation path models, per-discipline trust × ideology slopes)
- `downloads/Materials for the Shiny-App/` — `app.R` plus `data_trupol.rds`
  (aggregated data behind the authors' interactive figure)
- Study 5 (Twitter follower overlap, N = 3,977,868) has **no raw data on the
  OSF** — only the collection/analysis code in `analysis_study5.rmd`.

Per-study design (verified against the raw data, scripts, and survey PDFs;
final n reproduced exactly by re-running the scripts' exclusion rules):

- **Study 1** (US MTurk, randomized, analyzed n = 199: 101/98): vignette
  describes a research institute as **liberal** (topics consistent with the
  Democratic Party, scientists disclosed liberal views) vs. **conservative**
  (Republican mirror). Trust DV: METI (Hendriks et al. 2015), 14 bipolar
  adjective pairs on 7 points, averaged into expertise-based (6 items:
  competent…qualified) and morality-based trust (8 items:
  honest…considerate). Manipulation check, perceived ideological similarity,
  perceived societal value (7-pt). Respondent politics: `pol_orientation`
  (1 = very liberal … 7 = very conservative) and `pol_preference` (1 =
  strongly prefer Democrats … 7 = strongly prefer Republicans), averaged
  into `conservative`.
- **Study 2** (US MTurk, correlational, n = 1,000): 20 scientific
  disciplines (incl. Climate_scientists, Environmental_scientists) each
  rated on 0–10 sliders for agency/power, **perceived political orientation**
  (very liberal–very conservative), **trustworthiness**, and
  communion/warmth; plus 0–10 self-ratings incl. own political orientation
  (`part_beliefs_1`). The stereotype-measurement study.
- **Study 3** (Germany, correlational, n = 325): COVID-19 scientists;
  conservatism and stereotype `beliefs_scientists` on 1–10, trust composite
  and protection motivation on 1–7. Subset of a collaborator's larger
  pandemic project; no manipulation, no survey PDF or preregistration.
- **Study 4a** (US MTurk, randomized, analyzed n = 840: 438/402 after ~19%
  memory-check exclusions): two policies (financial-literacy classes;
  public-TV license "paid by all U.S. citizens") counterbalanced as
  recommended by **economists vs. sociologists** — discipline as a
  stereotype-based proxy for scientists' political orientation. DVs: policy
  support (7-pt), $100 donation split (0–100), general trust in
  sociologists/economists (7-pt), similarity; same two 7-pt politics items.
- **Study 4b** (US MTurk, randomized, analyzed n = 741: sociological 245 /
  economic 250 / interdisciplinary 246; the interdisciplinary arm is
  exploratory and excluded from the preregistered analyses, leaving
  n = 495): institute described as sociological vs. economic vs. both. DVs:
  METI 14 items plus support and information-seeking intentions; same
  politics items.

The paper's headline "total controlled N = 2,859" reproduces exactly as
199 + 1,000 + 325 + 840 + 495 (i.e., Study 4b counted without its
exploratory arm).

## Why it is here

Randomized scientist-identity vignettes that move a trust-in-scientists
outcome, with respondent ideology/party measured as a moderator: Study 1
manipulates scientists' explicit political label (liberal vs. conservative
institute) and Studies 4a/4b manipulate discipline as a stereotyped proxy,
all showing the trust effect flips sign with the respondent's own
conservatism (crossover interaction, mediated by perceived ideological
similarity). This is direct evidence for how trust ATEs interact with
politics — the *target's* party as moderator — complementing koetke2024's
message-strategy arms and the gligoric2025 trust-ATE null prior. Study 2's
20-discipline stereotype + trust sliders map which fields (climate and
environmental scientists at the liberal extreme) carry the largest
polarization potential. Caveat: the manipulation is identity information
about the scientists, not a persuasive message strategy — effects speak to
source-identity moderation, not to message-intervention ATEs.
