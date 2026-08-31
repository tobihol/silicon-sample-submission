# BB-PRIME Phase II Climate Change Intervention Tournament (Sinclair et al., PNAS 2025)

## Version

OSF project "BB-PRIME Phase II: Climate Change Intervention Tournament",
https://osf.io/x9c6j/ (project last modified 2025-07-09; identity verified via
the OSF API — title and contributor list match the paper). Downloaded
2026-08-15 from the project's `data/` folder (public, no account required).

Paper: Sinclair, Alyssa H.; Cosme, Danielle; Lydic, Kirsten; Reinero, Diego A.;
Carreras-Tartak, José; Mann, Michael E.; and Falk, Emily B. (2025). Behavioral
interventions motivate action to address climate change. *PNAS* 122(20),
e2426768122. https://doi.org/10.1073/pnas.2426768122

License: the OSF project declares no explicit license (`node_license: null`);
the data are publicly posted as the paper's shared materials. Treat as
research-use; cite the paper.

## Contents

All microdata are individual-level and in **long format** (one row per
participant × scale × item). The join key across files is **`SID`** (anonymous
participant ID, present in every CSV); `group` (the randomized condition) is
also carried in every file and is consistent per SID. N = 7,624 participants
(main exclusions) across 18 conditions: 17 theory-driven interventions
(`STPB`, `CF_general`, `CF_personalized`, `impact_text`, `impact_quiz`,
`letter`, `ES_promotion_self`, `ES_promotion_other`, `ES_prevention_self`,
`ES_prevention_other`, `MCII_individual`, `MCII_collective`, `moral_values`,
`norm_text`, `norm_quiz`, `social_relevance`, `self_relevance`) + `control`
(n = 850; interventions n = 370–428 each).

- `downloads/messages_data.csv` — 266,787 × 11; per-participant ratings of 5
  news headlines each, incl. **sharing intentions** (`msg_share_broad`,
  `msg_share_narrow`, 0–100 sliders) plus reading interest, relevance, emotion
- `downloads/petitions_data.csv` — 106,169 × 8; 3 petitions per participant:
  **`petition_sign`** (yes/no/no_later/no_unsure), `petition_clicked`,
  `petition_link_clicks`, **`petition_share_broad`/`_narrow`**
- `downloads/actions_data.csv` — 517,214 × 9; 24 daily-life actions
  (intention, current behavior, ease, approval, impact; categories: transit,
  energy, diet, recycle, conversations, collective)
- `downloads/emotions_data.csv` — 60,991 × 6; 8 climate emotions
- `downloads/other_dvs_data.csv` — 84,039 × 7; belief/attitude DVs and
  moderators (politics, concern_risk, self_efficacy, uncertainty/skepticism,
  psychological distance, climate knowledge, perceived cause)
- `downloads/demographics_data.csv` — 85,449 × 5; age, gender, race/ethnicity,
  Hispanic/Latinx, SES (income, savings, degree, subjective), state, zipcode
- `downloads/indiv_diffs_data_few_excl.csv` — 28,659 × 7; individual-difference
  moderators (political affiliation/ideology, climate anxiety, IAF); only
  shipped in the `few_excl` variant (N = 7,767)
- `downloads/actions_data_notmaxed_few_excl.csv` (459,271 × 9),
  `downloads/other_dvs_data_few_excl.csv` (62,136 × 7),
  `downloads/demographics_data_few_excl.csv` (87,064 × 5) — the `_few_excl`
  variants keep climate-change skeptics (N = 7,767); these are the inputs the
  moderator script loads
- `downloads/tournament_analysis_OSF.Rmd` — main analysis script
- `downloads/tournament_analysis_moderators.Rmd` — moderator analyses:
  condition × moderator mixed models (e.g. `lmer(action_intention_s ~ group *
  ideology_s + action_current_s + (1|SID))`), control as reference level
- `downloads/SOP_and_measures.docx` — measures documentation / codebook (item
  wordings, scales, procedure); DV/moderator items only — it does **not**
  contain the intervention scripts
- `downloads/materials/` — intervention materials from the OSF
  `intervention_materials/` folder: the full participant-facing scripts of all
  17 interventions live in the two Qualtrics exports
  `Intervention_Tournament_Intervention_Set_1.qsf` (e.g. CF_general = block
  "Carbon Footprint - General - Feedback"; norm_text = "Social Norms - Text",
  whose statistics sit in the block's `Options.LoopingOptions.Static`
  loop-and-merge fields) and `Intervention_Tournament_Intervention_Set_2.qsf`
  (e.g. letter = "Letter to Future Gen", moral_values, STPB = "Personal
  Benefits"); plus `Intervention_Tournament_DVs.qsf` and
  `Intervention_Tournament_DVs.docx` (outcome battery)

Verified with pandas: `group` ships in every file with exactly the 18 arms;
sharing/petition outcomes are individual-level (e.g. `msg_share_broad`:
38,113 rows = 7,623 SIDs × 5 headlines, values 0–100); SID overlap with
`demographics_data.csv` is 100% for all main-exclusion files.

## Why it is here

A 17-arm + control randomized tournament of theory-driven climate
interventions whose outcome battery includes **information sharing**
(willingness to share climate news headlines broadly/narrowly and to share
petitions) alongside petition signing and behavioral intentions — a target
outcome essentially absent from every other open source in `data/`. With
per-participant condition assignment, demographics, and political/ideology
moderators joinable on `SID`, it supports estimating condition × moderator
effects on message-sharing outcomes. Playbook asset D3.
