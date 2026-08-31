# Voelkel et al. 2026 — Climate-Messages Megastudy (CCC)

## Version

OSF-published replication data for the registered-report megastudy on the
persuasiveness of the most-cited climate messages. Downloaded 2026-08-15 via
the OSF API from the "Main Study" data component https://osf.io/2mcf8/
(DOI: 10.17605/OSF.IO/2MCF8) and its parent project https://osf.io/va27p/
(DOI: 10.17605/OSF.IO/VA27P); individual files fetched from
`https://osf.io/download/<file-id>/`.

Citation: Voelkel, Jan G.; Ashokkumar, Ashwini; Malhotra, Neil; and
Willer, Robb. A Registered Report Megastudy on the Persuasiveness of the
Most-Cited Climate Messages. *Nature Climate Change*, 2026.

License note: **no license is declared on either OSF node** (the API reports
`node_license: null` for both 2mcf8 and va27p). Treat as all-rights-reserved
research data: analyze internally and cite the authors — do **not** re-host,
redistribute, or publish the raw files.

## Contents

All in `downloads/`:

- `CCC - Data - Recoded.csv` — analysis-ready microdata (13,821 rows ×
  139 cols): raw items plus the composites and recodes built by the
  preparation script (e.g. `Belief_Pre/Post`, `ConditionR`, `PartyC3`,
  `AgeCategory`, `RaceEthnicity_*` dummies)
- `CCC - Data - Deidentified.csv` — the deidentified source data
  (13,821 rows × 164 cols) that the preparation script reads in
- `CCC - Script - Step 2 - Preparation.R` — the recoding script; serves as
  the de-facto codebook mapping raw items to analysis variables
- `CCC - Questionnaire.pdf`, `CCC - Questionnaire - Qualtrics.pdf` — the
  full survey instruments (item wordings, sliders, treatment texts)
- `Interventions.csv` — the citation-screening table of the 157 candidate
  climate-message studies from which the 10 tested messages were drawn

Deliberately skipped: `CCC - Script - 5 Bayesian.zip` (454 MB) and the
manuscript / supporting-information PDFs.

Key structure (verified with pandas): 13 arms of ~1,057–1,069 each in
`Condition` — 10 message treatments (Consensus Framing 1/2, Dire But
Solvable, Gains, Binding, Purity, Warmth, Free Market, System Preservation,
High Social Distance) and 3 innocuous-text controls (Control Baseball,
Control Neckties, Control Dances), pooled to `Control` in `ConditionR`.
13,546 respondents provide at least one post-treatment outcome (the paper's
analysis N ≈ 13,544). Nine outcome families, all on 0–100 sliders, each
measured pre and post (`Belief_*`, `Concern_*`, `Policies_*`, `Intent_*`,
`PoliciesSp_*`, `Candidate_*`, `Companies_*`, `IntentNp_*`) plus a
post-only `Donation` measure. Six scored moderators: `Gender`, `Age` /
`AgeCategory`, `RaceEthnicity_*`, `Education`, `Income_B`, and party ID
(`PartyC3` / `PartyC8` / `Party_N`).

## Why it is here

Closest design twin to the target study: short text-based climate messages
delivered in a single-shot survey experiment to a census-quota US opt-in
panel, with 0–100 slider outcomes and all six of our scored moderators
present at the individual level — the playbook's asset D3 and the anchor
for scale-bridging (calibrating predicted effect sizes and response
distributions onto real 0–100 slider behavior). Two caveats to respect
when bridging: it contains **zero trust outcomes**, and it uses a
**pre/post design** — post-treatment control-arm responses are primed by
the pre-measures, so use the control arms' **PRE**-treatment distributions
as the unprimed baselines.
