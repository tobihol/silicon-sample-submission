# Vlasceanu et al. 2024 — Global Climate Intervention Tournament (63 countries)

## Version

Downloaded 2026-08-15 from the two open archives named in the paper's data
availability statement:

- Zenodo: https://zenodo.org/records/10345806 (DOI 10.5281/zenodo.10345806,
  CC BY 4.0) — the paper's analysis dataset (`data63.xlsx`)
- OSF: https://osf.io/ytf89/ ("International Collaboration to Understand
  Climate Action", CC0 1.0) — the full ICPC data release (cleaned microdata
  `data_notimers.csv`, `codebook.xlsx`, project READme)

Analysis code (no data) lives at https://github.com/josephbb/ManyLabsClimate
and https://github.com/mvlasceanu/ClimateTournament.

Data citation: Vlasceanu, M., Doell, K. C., Bak-Coleman, J. B., et al. (2024).
Addressing climate change with behavioral science: A global intervention
tournament in 63 countries. *Science Advances*, 10(6), eadj5778.
https://doi.org/10.1126/sciadv.adj5778. Full-release descriptor: Doell, K. C.,
et al. (2024). The International Climate Psychology Collaboration: Climate
change-related data collected from 63 countries.
https://doi.org/10.31234/osf.io/7fy2g

## Contents

- `downloads/data63.xlsx` — the paper's individual-level analysis dataset:
  59,440 rows × 28 cols; `cond`/`condName` give the randomized condition
  (11 interventions + Control); outcomes are climate belief (`Belief1-4`),
  policy support (`Policy1-9`), social-media sharing (`SHAREcc`), and the
  WEPT tree-planting task (`WEPTcc`); plus country and demographics
- `downloads/data_notimers.csv` — full cleaned ICPC microdata (59,508 rows ×
  196 cols, timers removed; latin-1 encoded): raw item-level responses
  (`Belief.in.CC_*`, `CC_policy_*`, `Share*`, `WEPT*`), `condName`, `country`
- `downloads/codebook.xlsx` — variable-level codebook for the cleaned data
  (1,107 variables: label, question type, values)
- `downloads/OSF_READme.txt` — the OSF project's file inventory/READme
- `downloads/materials/` — intervention materials from OSF: `usa_1.qsf`
  (U.S. Qualtrics survey; the full participant-facing text of all 11
  interventions + control lives in the numbered intervention blocks, e.g.
  "4. Scientific Consensus Intervention", "10. Dynamic Social Norms",
  "9. A Letter to Future GenerationsV2"), `master_survey.pdf` (English master
  survey, 80 pp.; custom font encoding defeats text extraction — use the QSF
  for machine-readable text), `intervention_adaptation_manual.pdf`
  (per-intervention adaptation instructions). Other countries' QSFs remain in
  the OSF `ClimateManylabs_QSF/` folder (76 files)

U.S. subsample: n = 8,253 (`Country == "Usa"` in `data63.xlsx`).

## Why it is here

This repo is a Silicon Sample Benchmark entry predicting a climate-trust
messaging megastudy. The tournament is the closest open analogue — a
randomized multi-intervention climate messaging experiment with belief,
policy-support, sharing, and behavioral outcomes across 63 countries
(including a large U.S. arm). It therefore serves as the primary proxy corpus
for measuring how much to trust our own effect-level predictions
(playbook asset D3).
