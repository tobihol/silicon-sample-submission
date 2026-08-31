# Cooperative Election Study (CES) Common Content, 2024

## Version

CES Common Content, 2024 — Harvard Dataverse dataset version 9.0 (released
2025-09-05; dataset first published 2025-04-02). Distributed under **CC0 1.0**
(public domain dedication); downloaded 2026-08-15 from the Harvard Dataverse
public file-access API (no account required):
https://doi.org/10.7910/DVN/X11EP6
(landing page:
`https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/X11EP6`)

Data citation: Schaffner, Brian; Shih, Marissa; Ansolabehere, Stephen; Pope,
Jeremy, 2025, "Cooperative Election Study Common Content, 2024",
https://doi.org/10.7910/DVN/X11EP6, Harvard Dataverse, V9.

The bundled cumulative file (2006–2025) comes from a separate dataset:
CCES Cumulative Common Content, Harvard Dataverse version 12.0, CC0 1.0,
https://doi.org/10.7910/DVN/II2DB6 (Kuriwaki, Shiro, "Cumulative CES Common
Content", Harvard Dataverse, V12).

## Contents

CES 2024 Common Content (n = 60,000; DOI 10.7910/DVN/X11EP6):
- `downloads/CCES24_Common_OUTPUT_vv_topost_final.csv` — the individual-level
  microdata (60,000 rows × 694 columns, CSV; read with `pandas`). The
  companion Stata `.dta` (~993 MB) was not vendored; the CSV carries the same
  records.
- `downloads/CES_2024_GUIDE_vv.pdf` — the 2024 Guide (variable/codebook
  documentation for the Common Content)
- `downloads/CCES24_Common_pre.docx`, `downloads/CCES24_Common_post.docx` —
  the pre- and post-election questionnaires

CCES Cumulative Common Content, 2006–2025 (n = 718,955; DOI 10.7910/DVN/II2DB6):
- `downloads/cumulative_2006-2025.feather` — harmonized cumulative microdata
  (718,955 rows × 109 columns, Apache Arrow/Feather; read with
  `pandas`/`pyarrow`). The `.dta` (~725 MB) and `.rds` variants were not
  vendored.
- `downloads/guide_cumulative_2006-2025.pdf` — guide to the cumulative file

## Why it is here

This repository is a Silicon Sample Benchmark entry: it predicts the results of
a climate-trust messaging megastudy run on a census-quota sample of U.S. adults.
The CES supplies large-n, current U.S. individual-level microdata for the
party-identification, education, and income composition of the adult population —
serving as playbook asset D1, the profile pool from which synthetic respondent
profiles are drawn. It complements the ACS (which lacks party identification) by
providing `pid3`/`pid7` alongside `educ` and `faminc_new` and standard
demographics. The 60,000-respondent 2024 wave gives the most recent snapshot,
while the cumulative file adds historical depth for calibration and validation.
