# Hackenburg et al. 2025 — Scaling language model size yields diminishing returns for single-message political persuasion

## Version

GitHub repository `kobihackenburg/scaling-LLM-persuasion`
(https://github.com/kobihackenburg/scaling-LLM-persuasion), shallow clone of
the default branch at commit `4ce433248ec4d5a765297b7cc91c7f4caa88e376`
(2025-02-07, the latest as of download). Downloaded 2026-08-16 via
`git clone --depth 1`; selected files mirrored under `downloads/` with the
repo's folder structure (model-completion CSVs, instruction-tuning corpora,
fitted-model .rds outputs, and the pilot study were skipped).

Paper citation: Hackenburg, K., Tappin, B. M., Röttger, P., Hale, S. A.,
Bright, J., & Margetts, H. (2025). Scaling language model size yields
diminishing returns for single-message political persuasion. PNAS.
(Preprint: arXiv:2406.14508.)

License: MIT (Copyright (c) 2024 Kobi Hackenburg; `downloads/LICENSE`).
Redistribution is permitted, but per house policy raw data is still never
committed to this repo or deposited — it stays in the gitignored
`downloads/` tree and is re-fetched from source.

## Contents

- `downloads/main_study/code/analysis/final_data_with_metrics.csv` — the
  canonical participant-level main-study file, 25,982 rows × 113 columns
  (one row per US Prolific respondent). Verified structure:
  - Arms: `condition` = AI (19,529), control (5,163, no message), human
    (1,290). 730 distinct verbatim `treatment_message` texts
    (`treatment_message_id`/`message_id`): 720 LLM-generated (72 per issue,
    from 24 models across 7 families — pythia, Qwen1.5, Llama-2, Yi, falcon,
    GPT-4-0125-preview, Claude 3 Opus — crossed with prompt variants) plus
    10 human expert-written benchmark messages, one per
    issue. Full generation provenance per row: `model`, `model_family`,
    `parameters`, `pretraining_tokens`, `prompt_variant_number`,
    `prompt_full_text`, sampling settings.
  - Issues: 10 US policy issues (`issue`): affirmative_action, assisted
    suicide, border_restrictions, electoral_college, felons_voting,
    foreign_aid, medicaid, solitary_confinement, veteran healthcare,
    worker_pensions; plus `issue_valence`, `issue_stance_partisanship`.
  - Outcomes: 4 policy-attitude items per issue (`<issue>-1..4`, 0–100
    sliders, item 2 reverse-scored as `<issue>-2-reversed`), per-issue
    `<issue>_mean`, and the primary DV `dv_response_mean` (0–100; each
    respondent answers only their assigned issue's items).
  - Demographics/covariates: `party_affiliation` (6 categories from Strong
    Democrat to Strong Republican + Other) with numeric `political_party`
    (0–4), `ideo_affiliation` (6 categories) with `political_ideology`
    (0–4), `age`, `education` (6 levels), `gender`, 3 political-knowledge
    items, `attention_check`, `authorship` ("is this AI?" perception).
  - Message-level text metrics: `flesch`, `moral_nonmoral_ratio`,
    `emotion_proportion`, `type_token_ratio`, `gpt_legibility`,
    `gpt_on_topic`, `gpt_valence`, `task_completion`.
- `downloads/main_study/code/analysis/raw_data_final.csv` — raw Qualtrics
  export before cleaning/exclusions, 35,859 rows × 67 columns (includes
  incompletes; useful for attrition checks).
- `downloads/main_study/code/analysis/prompts.csv` — the 30 prompt
  templates (30 rows × 8 columns) used to generate the treatment messages.
- `downloads/main_study/code/analysis/1_prepare_data.R` … `5_nonlinear_comparisons.R`
  — the authors' full analysis pipeline (serves as the de-facto codebook:
  variable construction, exclusions, meta-analytic ATE estimation).
- `downloads/SI_Appendix.pdf` — supplementary information (survey
  instrument details, human-message provenance, robustness).
- `downloads/README.md`, `downloads/LICENSE` — repo documentation and MIT
  license.

## Why it is here

Highest-arm-count practice/power dataset in the repo: 720 static
LLM-generated message arms (plus 10 human-benchmark arms and a 5,163-person
control) with verbatim treatment texts, party ID, and ideology per
respondent. The harness needs tasks with ~30+ message arms to shrink
arm-clustered CIs (REPORT §7), and no other source here comes close — 72
arms per issue on 10 separate policy issues, each usable as an independent
high-arm task. Caveat: the stimuli are LLM-generated (single persuasion
messages, median ~210 words, from a model-size sweep), so this serves
prompt/model-selection power analysis, not human-message realism; the 10
expert-written human messages are the only human-authored arms. License is
MIT so redistribution would be fine, but per house policy the raw data is
still never committed or deposited.
