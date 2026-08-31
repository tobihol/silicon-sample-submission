# Climate Change in the American Mind, 2008–2024 Cumulative File

## Version

CCAM cumulative national survey data, waves 1–31 (Nov 2008 – Dec 2024),
April 2025 OSF release (files last modified 2025-04-30).
Downloaded 2026-08-15 from the canonical OSF project (no account required):
https://osf.io/jw79p/ (DOI: 10.17605/OSF.IO/JW79P)

Data citation: Yale Program on Climate Change Communication (YPCCC) & George
Mason University Center for Climate Change Communication (Mason 4C). (2025).
Climate Change in the American Mind: National survey data on public opinion
(2008–2024) [Data file and codebook]. doi: 10.17605/OSF.IO/JW79P

Companion article: Ballew, M. T., Leiserowitz, A., Roser-Renouf, C., Rosenthal,
S. A., Kotcher, J. E., Marlon, J. R., Lyon, E., Goldberg, M. H., & Maibach,
E. W. (2019). Climate Change in the American Mind: Data, tools, and trends.
Environment: Science and Policy for Sustainable Development, 61(3), 4–18.

Terms of use (YPCCC, see "Terms of Use.pdf" on the OSF project): non-exclusive
license for research/scholarly/academic, internal business, or personal
non-commercial use; no redistribution of the data; limited portions may appear
in publications with acknowledgment of the YPCCC as source.

## Contents

- `downloads/CCAM SPSS Data 2008-2024.sav` — the full cumulative microdata
  (35,309 respondents × 58 variables, all 31 waves 2008–2024, SPSS format;
  read with `pyreadstat`/`haven`)
- `downloads/Survey Methods and Codebook 2008-2024.pdf` — survey methods,
  weighting notes, variable/question documentation, and data tables

## Why it is here

This repo is a Silicon Sample Benchmark entry predicting a climate-trust
messaging megastudy, and CCAM is the reference survey for U.S. climate
opinion. It provides nationally representative baseline distributions for
climate beliefs (`happening`, `cause_recoded`, `sci_consensus`), worry and
risk perceptions (`worry`, `harm_personally`, `harm_future_gen`), and policy
preferences (`reg_CO2_pollutant`, `fund_research`, `priority_cleanenergy`),
crossed with demographics and politics (age, education, income, race,
`party_w_leaners`, `ideology`). It serves as playbook asset D2, the baseline
corpus for calibrating and sanity-checking silicon-sample predictions.
