# Gligorić, van Kleef & Rutjens 2025 — Political ideology and trust in scientists in the USA

## Version

OSF project "Political ideology and trust in scientists in the US"
(https://osf.io/n63mz/), full osfstorage contents as of 2026-08-15
(project last modified on OSF 2025-02-14). Main study data file:
https://osf.io/download/8ae3k/. Downloaded 2026-08-15 via the OSF API
(no account required).

Paper citation: Gligorić, V., van Kleef, G. A., & Rutjens, B. T. (2025).
Political ideology and trust in scientists in the USA. Nature Human
Behaviour. (Registered Report; Stage 1 protocol accepted in NHB, included
on the OSF project.)

License: none specified on the OSF project (`node_license` is empty and no
license is attached). Publicly posted for a published Registered Report;
kept here privately for research use only, not redistributed.

## Contents

All from OSF osfstorage, mirrored under `downloads/` with the project's
folder structure (manuscript/protocol .docx files at the project root were
skipped):

- `downloads/Main Study/Analyses (data and codes)/dataMainStudy.csv` — main
  experiment microdata, 7,800 rows × 82 columns (the canonical file at
  osf.io/download/8ae3k)
- `downloads/Main Study/Analyses (data and codes)/R Code Main Study.R`,
  `R Code Markdown.Rmd`, `R-Code-Markdown.html` — the authors' analysis code
  and rendered output (serve as the de-facto codebook: variable recodes,
  condition levels, trust-score construction)
- `downloads/Main Study/Materials/Qualtrics file.qsf` and
  `Materials (word exported from Qualtrics).docx` — full survey instrument
  (exact item wording, response scales, message texts)
- `downloads/Pilot Study 1/IdeologyTrust data.csv` (3,509 × 1,271) and
  `Data analysis Ideology.R` — pilot on ideology and trust across many
  scientist occupations
- `downloads/Pilot Study 2/Pilot Study 2 data.csv` (201 × 21),
  `Pilot Study 2 data output.html`, and
  `Pre-test_ideology_and_trust_manipulations.docx` — pre-test of the trust
  manipulations/messages

Key main-study variables (verified against the data and the QSF):

- Trust in scientists: 35 occupations, each rated on two 7-point bipolar
  items (`<occupation>_1` = not credible–credible, `<occupation>_2` =
  untrustworthy–trustworthy; 1–7). Occupations include climate-adjacent
  fields: `climatologists`, `meteorologists`, `environmental scient`,
  `ecologists`, `oceanographers`. The authors average the two items per
  occupation into a trust score.
- Ideology: `Ideology`, 1–10 self-placement from "Extremely Liberal" (1) to
  "Extremely Conservative" (10); `PolIdentification` is 7-point strength of
  identification with one's political group.
- Experiment: `Condition` with 6 levels — Control (n = 2,248) and five
  randomized trust-raising messages: Norms (1,116), ConservativeScientists
  (1,116), RespectableConservatives (1,114), ValueBased (1,111), Co-Benefit
  (1,095) — plus `BelievabilityExper_1..3` manipulation checks.

## Why it is here

The only open source in our set that measures the target study's headline
construct — trust in scientists — crossed with political ideology in a US
sample, and that additionally ran five randomized messages designed to raise
conservatives' trust, all of which failed. That null pattern is a directly
usable prior against predicting large trust ATEs from messaging
interventions. Serves D3 for trust outcomes and provides a 7-point Likert
anchor for scale bridging.
