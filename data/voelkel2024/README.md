# Strengthening Democracy Challenge Megastudy (Voelkel et al. 2024)

## Version

Public OSF release of the Strengthening Democracy Challenge megastudy
("Megastudy testing 25 treatments to reduce antidemocratic attitudes and
partisan animosity", Science 386, eadh4764, 2024; 25 interventions plus two
controls, N = 32,059 after preregistered exclusions).
Downloaded 2026-08-15 from the project's "Main Survey" component (no account
required): https://osf.io/jzbnt/ (component: https://osf.io/2sv7p/,
DOI: https://doi.org/10.17605/OSF.IO/JZBNT).

Data citation: Voelkel, J. G., Stagnaro, M. N., Chu, J., Pink, S. L.,
Mernyk, J. S., Redekopp, C., ... Willer, R. (2024). Megastudy testing 25
treatments to reduce antidemocratic attitudes and partisan animosity.
Science, 386(6719), eadh4764. Data: The Strengthening Democracy Challenge,
OSF (2024); https://doi.org/10.17605/OSF.IO/JZBNT.

No explicit license is set on the OSF project; the data are publicly posted
for reuse per the paper's data availability statement. Treat as
research-use; cite the paper and the OSF repository.

## Contents

- `downloads/SDC - Data - Anonymized.csv` — individual-level microdata as
  collected (35,252 rows x 70 cols, before exclusions; `Condition` column
  with 27 arms = 25 interventions + Null_Control + Alternative_Control;
  raw outcome items and demographics)
- `downloads/SDC - Data - Recoded.csv` — recoded analysis dataset
  (35,252 rows x 113 cols) with constructed outcome scales: `PA` (partisan
  animosity), `ADA` (support for undemocratic practices), `SPV` (support
  for partisan violence), `SUC` (support for undemocratic candidates),
  plus secondary outcomes (`OppBip`, `SocDistrust`, `SocDis`, `BEPF`,
  `EleDen`, `ODR_1..4`) and mediators
- `downloads/SDC - Data - Outcome Names.csv`,
  `downloads/SDC - Data - Intervention Names.csv` — mappings from data
  labels to manuscript names
- `downloads/SDC - Data - Intervention - Coding J.xlsx`,
  `downloads/SDC - Data - Intervention - Coding N.xlsx` — intervention
  feature codings
- `downloads/SDC - Read Me.pdf` — repository read-me / documentation
- `downloads/SDC - Questionnaire.pdf` — full questionnaire (codebook for
  item wordings and response scales)

## Why it is here

This repo is a Silicon Sample Benchmark entry predicting the results of a
climate-trust messaging megastudy. This dataset is the second proxy corpus
(playbook asset D3): an open U.S. megastudy with many short text
interventions and a shared control, structurally analogous to the target
study. We run it through the same prediction pipeline to calibrate how much
to trust our effect-level predictions before the 2026-08-31 lock.
