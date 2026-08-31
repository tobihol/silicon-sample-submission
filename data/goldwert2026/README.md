# Climate Advocacy Megastudy (Goldwert et al., PNAS Nexus 2026)

## Version

Study materials and cleaned analysis data for the Climate Advocacy Megastudy
(Goldwert et al., PNAS Nexus 2026). Downloaded 2026-08-15 from the canonical
OSF project (no account required): https://osf.io/wv7c3/
(main data file: https://osf.io/download/qsv43/, codebook:
https://osf.io/download/3cfhy/).

Data citation: Goldwert et al., Climate Advocacy Megastudy. [Data and
materials]. OSF, https://osf.io/wv7c3/. Paper: PNAS Nexus, 2026.

No license is declared on the OSF project (checked via the OSF API:
`node_license` is empty). Treat as all-rights-reserved: cite and use for
analysis, do not re-host or redistribute.

## Contents

- `downloads/advocacy_data.csv` — primary cleaned, anonymized analysis dataset
  (31,324 rows x 113 columns; exclusions applied, no timers, no
  intervention-specific columns)
- `downloads/codebook_advocacy.pdf` — codebook (note: `belief_1` and
  `policy_1` are NOT documented in it; see below)
- `downloads/Advocacy_Cleaning_main.ipynb` — the cleaning/preparation
  notebook; documents variable recoding and the columns the codebook omits
- `downloads/readme.txt` — the project's own file manifest
- `downloads/intervention_docx/` — 18 .docx files with the verbatim
  intervention materials (17 interventions + neutral control)
- `downloads/intervention_qsfs/` — the matching 18 Qualtrics .qsf survey
  exports (intervention blocks only, not the shared DV battery)

Skipped: the preprint/paper PDF, the preregistration, the 108 MB raw XLSX
(`ClimateAdvocacy_RAW_anon.xlsx`), and the remaining analysis scripts.

Verified structure: 18 arms in `cond` (0–17) / `condName` (16 crowdsourced
interventions + benchmark + `Control`), ~1,733–1,745 participants per arm.
Moderators present: `Age`, `Gender` (string labels), `Edu` (1–4), `Income`
(1–8), `MacArthur_SES` (1–10), ideology (`Politics_Soc`, `Politics_Econ`,
`ide`, all 0–100; `ide_ms` binary), plus `Party` (Democrat/Republican/Other).
Behavioral-commitment DVs (`pol_campaign`, `pol_candidate`, `march`,
`conversation`, `flyless`, `lessbeef`, `bank_raw`) and mediators
(`Pefficacy`, `Cefficacy`, emotions) are 0–100 sliders; `petition`,
`newsletter1/2`, `video` are 0/1; `donation` / `donation_keep` are 0–10.

`belief_1` / `policy_1` (undocumented in the codebook): empirically both are
0–100 integer sliders (101 unique integer values, means ≈ 55.8 / 52.9). Per
`DV_order` they form the randomized "BeliefandPolicySupport" block of the DV
battery, i.e. post-intervention climate-change belief and climate-policy
support. Each is missing for ~24% of rows (7,537 / 7,585), with missingness
varying by arm (16.5%–35%) — attrition/order effects, so handle missingness
per arm.

## Why it is here

Structurally the closest twin to the target study (playbook asset D3): 16
crowdsourced interventions plus 2 control-like arms, a quota-matched US
opt-in panel, mostly 0–100 slider outcomes, and real behavioral outcomes
(newsletter signup, donation allocation) analogous to two target outcomes —
usable as training/validation ground truth for effect-direction and
effect-ranking predictions. Caveats: it has no trust items, and its
interventions are videos/writing tasks rather than the target's message
format, so use it for ranking intervention effects, not for absolute effect
magnitudes.
