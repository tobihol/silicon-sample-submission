# TISP Many Labs Dataset (Trust in Science and Science-Related Populism, 68 countries)

## Version

Analysis-ready release (`ds_final`, N = 69,534; survey fielded Nov 2022 – Aug 2023;
data files posted to OSF May 2024). Downloaded 2026-08-15 from the OSF repository
"The TISP Dataset" (no account required): https://osf.io/5c3qd/
(DOI: 10.17605/OSF.IO/5C3QD). License: CC BY 4.0.

Data citation: Mede, N. G., Cologna, V., Berger, S., Besley, J., Brick, C.,
Joubert, M., Maibach, E. W., Mihelj, S., Oreskes, N., Schäfer, M. S.,
van der Linden, S., . . . Zwaan, R. A. (2025). Perceptions of science, science
communication, and climate change attitudes in 68 countries – the TISP dataset.
*Scientific Data*, 12(1), 114. https://doi.org/10.1038/s41597-024-04100-7

Companion analysis paper: Cologna, V., Mede, N. G., et al. (2025). Trust in
scientists and their role in society across 68 countries. *Nature Human
Behaviour*. https://doi.org/10.1038/s41562-024-02090-5

## Contents

- `downloads/ds_final.sav` — the analysis-ready individual-level microdata
  (69,534 respondents × 140 variables, all 68 countries incl. the U.S.;
  SPSS format with value/variable labels; read with `pyreadstat`/`haven`).
  Includes post-stratification weights `WEIGHT_CNTRY` (within-country),
  `WEIGHT_GLOBL` (global), and `WEIGHT_MLVLM` (multilevel-rescaled).
- `downloads/ds_final.csv` — the same microdata as semicolon-delimited,
  UTF-8-with-BOM CSV (missing values coded "NA"); no value labels.
- `downloads/core-questionnaire_english.pdf` — the TISP core questionnaire
  (English master), the item-level documentation for all variables.

## Why it is here

This repo is a Silicon Sample Benchmark entry predicting a climate-trust
messaging megastudy. TISP measures the exact 12-item, four-dimension
trust-in-scientists scale (competence, integrity, benevolence, openness;
variables `TRUST_SCI_expert` … `TRUST_SCI_otherviews`) that the target study
uses as its outcome, so it is the key baseline-distribution source (playbook
asset D2). The U.S. subsample (n = 2,559) plus climate-attitude items
(`CLIM_*`) and standard demographics allow calibrating simulated respondents
against real weighted distributions.
