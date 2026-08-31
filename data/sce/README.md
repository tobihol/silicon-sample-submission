# FRBNY Survey of Consumer Expectations (SCE), Public Microdata 2013–2025

## Version

Federal Reserve Bank of New York, Survey of Consumer Expectations — complete
public microdata (core monthly module), covering June 2013 through October 2025
(the "latest" file is a rolling window updated by FRBNY; downloaded state:
2025-01 to 2025-10). Downloaded 2026-08-15 from the SCE downloads section (no
account required; the server requires a browser User-Agent):
https://www.newyorkfed.org/microeconomics/sce#/

Data citation, in the form FRBNY requires (from the first row of each
microdata file): "Source: Survey of Consumer Expectations, © 2013-26 Federal
Reserve Bank of New York (FRBNY). The SCE data are available without charge at
www.newyorkfed.org and may be used subject to license terms posted there.
FRBNY disclaims any responsibility or legal liability for this analysis and
interpretation of Survey of Consumer Expectations data."

Terms of use: data are free of charge and licensed for reuse subject to the
license terms on the FRBNY site; the questionnaire PDF (p. 1) additionally
requires the attribution/disclaimer above when publishing results, and forbids
implying FRBNY endorsement or attributing derivative surveys to FRBNY.

## Contents

- `downloads/frbny-sce-public-microdata-complete-13-16.xlsx` — 56,444 rows
  (2013-06 to 2016-12, 43 monthly waves) × 220 columns
- `downloads/frbny-sce-public-microdata-complete-17-19.xlsx` — 47,681 rows
  (2017-01 to 2019-12, 36 waves) × 220 columns
- `downloads/frbny-sce-public-microdata-20-24.xlsx` — 71,976 populated rows
  (2020-01 to 2024-12, 60 waves) × 229 columns (sheet dimension claims 82,535
  data rows; the trailing ~10.6k rows are empty styled cells)
- `downloads/frbny-sce-public-microdata-latest.xlsx` — 10,559 rows
  (2025-01 to 2025-10 as downloaded) × 229 columns
- `downloads/frbny-sce-survey-core-module-public-questionnaire.pdf` — the
  44-page core-module questionnaire/codebook (question wording, response
  scales, license terms on p. 1)

Each xlsx is a single sheet; row 1 is the FRBNY source/disclaimer line, row 2
the variable-name header (read with `pandas.read_excel(..., skiprows=1)`;
files are large — 300–560 MB of sheet XML — so prefer streaming/`read_only`
access or convert to parquet once). ~186k person-month responses pooled, from
a rotating, nationally representative panel of ~1,300 household heads
(respondents stay up to 12 months).

Key 0–100 "percent chance" items (elicited on a 0–100 slider, integer-valued
in practice): `Q4new` (chance US unemployment rate higher in 12 months),
`Q5new` (interest rates higher), `Q6new` (stock prices higher), `Q13new`
(losing job), `Q14new` (leaving job voluntarily), `Q22new` (finding a job
within 3 months), `Q9_bin1..10` / `Q24_bin*` / `C1_bin*` (probabilities
assigned to inflation / home-price bins, sum to 100).

Demographics: raw items `Q32` (age), `Q33` (gender), `Q34`/`Q35_*`
(Hispanic/race), `Q36` (education, 9 levels), `Q38` (marital), `Q47` (HH
income, 11 brackets) are asked at panel entry, so they are populated only in
each respondent's first interview month; the derived categoricals `_AGE_CAT`,
`_EDU_CAT`, `_HH_INC_CAT`, `_REGION_CAT`, `_NUM_CAT` (numeracy) and `_STATE`
are carried on (nearly) every row. Sampling weight: `weight`.

## Why it is here

No climate content — this is a pure response-format asset. It is the largest
open US source of 0–100 "percent chance" responses linked to demographics,
used to fit an empirical rounding/heaping model for probability-scale items:
real respondents pile up on 0/50/100 and on multiples of 5 and 10, with the
degree of heaping varying by education and numeracy. Verified on `Q4new`
pooled across all files (n = 186,302; 100% integer-valued): 75.3% of responses
are multiples of 5, 61.2% multiples of 10, 16.8% exactly 50, 1.7% at 0, 1.3%
at 100 — and heaping declines with education (non-multiple-of-5 share: 28.9%
high school, 25.6% some college, 23.2% college). The benchmark's headline
Tier-1 diagnostic is distribution shape, so layering this empirical heaping
structure onto smooth model-predicted distributions is cheap accuracy.
