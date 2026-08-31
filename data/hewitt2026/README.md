# Hewitt, Ashokkumar, Ghezae & Willer (Nature 2026) — 70-experiment archive

## Version

Code Ocean capsule **9843791, v1.0** — "Predicting Results of Social Science
Experiments Using Large Language Models" (Luke Hewitt, Ashwini Ashokkumar,
Isaias Ghezae, Robb Willer; Stanford / Harvard). Capsule git commit
`10f2140ab6f49e004c3bd107420babade9c8213f`, tag `v1.0`, authored
2026-06-01 by Luke Hewitt. Capsule page (not needed to fetch):
`https://codeocean.com/capsule/9843791/tree/v1`.

Obtained **2026-08-24** by anonymous `git clone
https://git.codeocean.com/capsule-9843791.git` — no login, no browser, no
export dialog. `fetch.sh` reproduces the folder from that URL pinned to the
commit above, applies the same prune, and hash-verifies every kept file.

Only the **primary archive** (Archive 1: 50 TESS experiments 2016–2022 plus
20 Coppock, Leeper & Mullinix 2018 experiments — TESS originals and their
MTurk replications) is kept here, as **raw participant-level responses** with
coarse demographics. The paper's secondary archive of 15 megastudies, the
GPT-4 outputs, the human forecasts and the scientists' survey were deleted
locally (see "What was deleted and why").

## Contents (`downloads/capsule/`, 1.1 MB, gitignored)

| file | size | sha256 (first 16) | what |
|---|---|---|---|
| `data/rct_responses.RDS` | 919,469 | `4c7e28206585972b` | all original human responses: nested tibble, 134 study×outcome rows, 71 studies |
| `data/RA_hypotheses.RDS` | 75,023 | `70f6ebe388f2488f` | RA-coded author hypotheses: 165 rows (52 studies) with nested condition → hypothesised-direction table |
| `data/RA_study_features.csv` | 19,257 | `f61b466932c3fe73` | 70 studies: publication-status flags, TESS flag, discipline flags, authors, title, field, link |
| `data/RA_outcome_features.csv` | 4,459 | `594371ca375687cf` | 134 study×outcome rows: `outcome_existing_attitude` flag |
| `data/LICENSE` | 6,555 | `36ffd9dc085d529a` | CC0 1.0 Universal (data) |
| `code/LICENSE` | 1,068 | `82751d23fd427c7d` | MIT (code), (c) 2026 Luke Hewitt |
| `code/README.md` | 3,788 | `272fda4c3904ee9c` | capsule README (file inventory, run instructions) |
| `code/PLOT_DATA_CODEBOOK.docx` | 14,246 | `9d77317d41c45ad1` | codebook for the paper's per-figure plot-data CSVs (not the raw data) |
| `code/util.R` | 14,349 | `26be019d432baf23` | helper functions (effect estimation, rescaling, caching) |
| `code/load_archive1_results.R` | 9,693 | `630e61fe7bef1e86` | how Archive-1 condition means / effects are computed from `rct_responses.RDS` (incl. subgroup filters on `race_4`, `GENDER`, `pid_3`) |
| `code/5_heterogeneity_archive1.R` | 13,096 | `6b06b12f74e0d8ea` | subgroup (gender / race / party) heterogeneity analysis |
| `metadata/metadata.yml` | 1,951 | `02f1c2651e4338b3` | capsule metadata: title, abstract, authors |

Full sha256 for every file is pinned in `fetch.sh`.

## Key variables

`rct_responses.RDS` is a tibble with one row per study × outcome:
`study` (id, e.g. `KrupnikovS34`, `immigration`), `outcome.variable`,
`outcome.name`, `outcome.min`, `outcome.max`, `outcome.limits`, and a
list-column `data` holding the participant-level rows for that outcome:

- `y` — the response on the original scale (`outcome.min`–`outcome.max`;
  mostly 1–7 (49 outcomes) and 1–5 (42), ten 0–100 items, a few 0/1)
- `condition.name` — experimental arm (2–12 arms per outcome; verbatim arm
  labels from the original studies)
- `GENDER` (Female/Male), `race_4` (Black/White, else NA), `age_5`
  (Younger/Older than 50), `EDUC4` (College/Non-College) — present in every
  study
- `pid_3` (Democrat/Independent/Republican), `ideo_3`
  (Liberal/Moderate/Conservative) — present in 70 of 71 studies (absent in
  `bucci1408`)
- `Z` (0/1) — only in the 20 Coppock et al. studies; sample indicator
  (original TESS vs MTurk replication)

No participant id, weight, survey date, free text, or geography is included.

Counts (verified locally, 2026-08-24):

- **71 studies** in `rct_responses.RDS` (50 TESS + 20 Coppock + `willer845`,
  the senior author's own TESS study, which is absent from
  `RA_study_features.csv` and hence from the analysed **70**);
- **134 study×outcome rows**; **482 condition-vs-reference contrasts** in the
  raw file (paper reports 469 effects after its exclusions);
- **121,388 participants** summing each study's largest outcome table
  (paper: 119,330 for the 70 analysed studies).

## Reading the files

`pyreadr` **cannot** read `rct_responses.RDS` or `RA_hypotheses.RDS` (nested
list-columns / glue class → "unsupported features"). Use R (installed locally,
4.6.1):

```sh
Rscript -e 'library(dplyr); r <- readRDS("data/hewitt2026/downloads/capsule/data/rct_responses.RDS");
  long <- tidyr::unnest(select(r, study, outcome.name, outcome.min, outcome.max, data), data);
  readr::write_csv(long, "hewitt2026_long.csv")'
```

This yields a 233,601 × 13 participant×outcome long table (27 MB CSV; tested
2026-08-24). The two CSVs read with pandas directly.

## Why it is here

Train / calibration only (docs/dataset-scouting-2026-08-24.md §3, §6): an
empirical distribution of ATE magnitudes from ~70 probability-sample text /
vignette survey experiments on the original response scales, with party,
ideology, gender, race, age and education for subgroup effects — a shrinkage
prior for effect sizes and a source for the paper's documented LLM overshoot
(the published calibration slope). It carries no climate or
trust-in-scientists outcome and must never be used as a validation set
(the 70 TESS effects have long been public; the paper's headline numbers are
likely memorised by any frontier model).

## Caveats

- **Red-line procedure followed.** Before any data row was read, the study
  ids of the secondary archive `data/megastudies.RDS` were enumerated (59
  `dataset` values) and each was mapped to one of the 15 megastudies named in
  the scouting review: `Allen2023` → Allen et al. 2024; 42 `Broockman-*`
  issue×side rows → Broockman et al. 2024; `Dellavigna` → DellaVigna & Linos
  2022; `DellavignaPope` → DellaVigna & Pope 2018; `Doell` → Vlasceanu et
  al. 2024; `Goldwert` → Goldwert et al. 2026; `Mason` → Mason et al. 2025;
  `Milkman2021`/`Milkman2022`/`Milkman2023` → Milkman et al. 2021/2022/2024
  (the archive holds **three** Milkman studies, not four as the review
  wrote; the total is still 15); `SDC` → Voelkel et al. 2024; `Saccardo2024`
  → Saccardo et al. 2024; 4 `Tappin-*` rows → Tappin et al. 2023;
  `Voelkel2025` → Voelkel et al. 2025/26 climate megastudy; `Zickfeld` →
  Zickfeld et al. 2025. No unexplained id; nothing resembling a
  trust-in-climate-scientists megastudy. Its outcome labels (`PA`, `ADA`,
  `belief`, `support`, `concern`, `policies`, `intent`, `immigration`, `ubi`)
  contain no `trust`/`scien` string. The file was then deleted (below). The
  capsule README, metadata and code contain no reference to any sealed
  study; no external link in them was followed.
- **No trust-in-scientists / climate outcome anywhere in the kept data.**
  `grep -i 'scien|trust|climate'` over the study and outcome features and
  over `outcome.name`/`hypothesis` hits only `trust_democrats` /
  `trust_republicans` (Connors 1226, affective polarization) and the string
  "Political Science" in field labels.
- **What was deleted and why** (never keep model outputs or forecasts as
  data): `data/llm_responses.RDS` (21.2 MB, GPT-4 and other LLM prompts +
  responses), `data/megastudies.RDS` (secondary archive — preprocessed
  effects *with a `prediction.gpt-4` column*; redundant with the vendored
  voelkel2026 / goldwert2026 / vlasceanu2024 / voelkel2024 / tappin2023 raw
  data), `data/gpt_author_recognition.csv` (GPT-4 output),
  `data/forecasting_responses.RDS` (layperson forecasts, keyed by
  `PROLIFIC_PID`), `data/individual_expert_predictions.rds` (expert
  forecasts for the megastudies), `data/survey_data/` (the 460-scientist
  survey), the 14 analysis scripts that drive the LLM pipeline, the Docker
  environment, and the `.git` directory (so deleted files are not
  recoverable from objects). `fetch.sh` re-clones the full capsule and
  re-applies the same prune.
- **PII scan: clean.** The only character columns are `condition.name` and
  the six demographic variables (cardinality ≤ 12); no id, name, email, IP,
  ZIP, date-of-birth, free-text or open-ended column exists. Demographics are
  coarse binaries/trichotomies. `RA_study_features.csv` lists study authors
  and article links — bibliographic, not respondent data. The corresponding
  author's e-mail is in `metadata/metadata.yml` (public capsule metadata).
- Raw effect counts differ from the paper (482 vs 469 contrasts; 121,388 vs
  119,330 participants) because the raw file includes `willer845` and
  contrasts the paper excluded; use `RA_study_features.csv` to restrict to
  the 70 analysed studies and `load_archive1_results.R` for the paper's
  effect definition.
- The Coppock studies pool the TESS original and the MTurk replication in
  one table (`Z` indicator); do not treat them as a single probability
  sample.
- `PLOT_DATA_CODEBOOK.docx` documents the paper's *figure* CSVs, which are
  not in the capsule's `data/` (they are outputs of the run); it is kept for
  variable naming only.

## License

Two LICENSE files, both read in full.

`data/LICENSE` — **CC0 1.0 Universal**: "Affirmer hereby overtly, fully,
permanently, irrevocably and unconditionally waives, abandons, and surrenders
all of Affirmer's Copyright and Related Rights and associated claims and
causes of action … in the Work (i) in all territories worldwide, … (iv) for
any purpose whatsoever, including without limitation commercial, advertising
or promotional purposes". Redistribution is therefore permitted; the raw copy
is nevertheless kept under the gitignored `downloads/` by repo convention.
Note CC0 §4(c): "Affirmer disclaims responsibility for clearing rights of
other persons that may apply to the Work" — the underlying TESS and Coppock
et al. data are themselves public.

`code/LICENSE` — **MIT License, Copyright (c) 2026 Luke Hewitt**: "Permission
is hereby granted, free of charge, to any person obtaining a copy of this
software … to deal in the Software without restriction, including without
limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies … subject to the following conditions: The
above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software."

## Citation

Hewitt, L., Ashokkumar, A., Ghezae, I., & Willer, R. (2026). Predicting
results of social science experiments using large language models. *Nature*.
Data and code: Code Ocean capsule 9843791, v1.0 (data CC0 1.0, code MIT).
Preprint: PsyArXiv 3svep. Also cite the original TESS studies (see
`RA_study_features.csv` for authors/titles) and Coppock, Leeper & Mullinix
(2018, PNAS, "Generalizability of heterogeneous treatment effect estimates
across samples") for the 20 replication experiments.
