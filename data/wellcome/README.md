# Wellcome Global Monitor 2018 and 2020 — U.S. subsets

## Version

Two waves of the Wellcome Global Monitor (a Wellcome-commissioned module
fielded by Gallup inside the Gallup World Poll), downloaded 2026-08-24 from
Wellcome's CMS (no login, no DUA; direct links and pinned sha256 hashes are
in `fetch.sh`; the CMS answers 403 to non-browser User-Agents, so the script
sends a browser UA):

- **2018 wave** (report "Wellcome Global Monitor 2018", published June 2019;
  144 countries, n=149,014). One xlsx with sheets `Crosstabs all countries`,
  `Full dataset` (microdata) and `Data dictionary`.
  Report page: https://wellcome.org/reports/wellcome-global-monitor/2018
  Data: https://cms.wellcome.org/sites/default/files/wgm2018-dataset-crosstabs-all-countries.xlsx
  **U.S.: n=1,006, fielded 12 Jul–23 Aug 2018, landline + mobile telephone,
  English/Spanish, design effect 1.63, MOE ±4.0** (methodology Appendix table).
- **2020 wave** (report "Wellcome Global Monitor 2020: How Covid-19 affected
  people's lives and their views about science", published Nov 2021;
  113 countries, n=119,088). Zip containing one csv
  (`wgm_full_wave2_public_file_final (1)_csv.csv`, 27.3 MB unzipped); a
  `.sav` twin is on the same page.
  Report page: https://wellcome.org/reports/wellcome-global-monitor-covid-19/2020
  Data: https://cms.wellcome.org/sites/default/files/2021-11/wgm_full_wave2_public_file.zip
  **U.S.: n=1,001, fielded 4 Aug–9 Oct 2020, telephone (CATI), design
  effect 1.86, MOE ±4.2** (methodology table).

Both waves are Gallup World Poll samples: civilian, non-institutionalised
population **aged 15 and older**; in the U.S. a dual-frame (landline + mobile)
RDD telephone sample; national weight `wgt`/`WGT` post-stratifies to the
15+ population (mean 1.0, sums to n).

## Contents

- `fetch.sh` — re-downloads all files below from the pinned Wellcome URLs
  into `downloads/` (gitignored) and verifies sha256
- `extract_us.py` — filters both raw files to the U.S. rows and writes
  `downloads/derived/wgm2018_us.csv` (n=1,006, 75 KB) and
  `downloads/derived/wgm2020_us.csv` (n=1,001, 74 KB) with the key items,
  demographics and the national weight only (98/99 → NA). Run with
  `uv run --with pandas --with openpyxl python data/wellcome/extract_us.py`
  (the xlsx read takes ~1–2 min). Its stdout prints the verification tables
  reproduced below.
- `downloads/wgm2018-dataset-crosstabs-all-countries.xlsx` — 52,593,312 B,
  sha256 `8bcbacd403a4ee531a526913364c163005be6b497ee429214ec2dd6d7a500c90`
- `downloads/wgm2018-questionnaire.pdf` — 2,228,376 B,
  sha256 `c0dd7669e636139f10494e265622bec7c7eba7f21dec9f6466e64f4d001c65b0`
- `downloads/wgm2018-methodology.pdf` — 552,482 B (Appendix A: country table
  with dates, n, mode, DEFF, MOE),
  sha256 `2e37d365ce059f8638cb282e495cb22a26339d8838dd74541475976a8c592d64`
- `downloads/wgm_full_wave2_public_file.zip` — 5,850,179 B,
  sha256 `b8ef272ff38a78dcc1dd8a9e1aeb51682c963edef2e42b5df522bf1994ca8991`
- `downloads/wgmdata-covid-data-dictionary-user-guide.docx` — 37,102 B (2020
  data dictionary),
  sha256 `12860196e34bbb6e7bb8c7f727f810607e62048d6b38117d056485eb65a14e97`
- `downloads/WGM_Full_Questionnaire_2020.pdf` — 152,854 B,
  sha256 `05369ff739a452d6811532f5488aa46763a70523e2a9faeb316a91e63ea37d90`
- `downloads/wgm2020-methodology.pdf` — 142,968 B,
  sha256 `65d9b946f2203a49f2dfc7b1562138acfcdd15b537751dddf7e13c6863eafb32`

Total on disk ~60 MB. Nothing in `downloads/` is committed.

## Key variables

All trust items are 4-point, **1 = A lot, 2 = Some, 3 = Not much,
4 = Not at all** (note the reverse direction vs. most scales; 98 = DK,
99 = Refused in the raw files, NA in the derived csvs).

### 2018 (`Full dataset` sheet; U.S. filter `WP5 == 1`)

| Variable | Wording (from the xlsx `Data dictionary` sheet) |
|---|---|
| `Q11C` | How much do you trust each of the following? How about scientists in this country? Do you trust them a lot, some, not much, or not at all? |
| `Q12` | In general, would you say that you trust science a lot, some, not much, or not at all? |
| `Q13` | In general, how much do you trust scientists to find out accurate information about the world? (competence) |
| `Q14A` | How much do you trust SCIENTISTS working in colleges/universities in this country ... To do their work with the intention of benefiting the public. (benevolence) |
| `Q14B` | ... SCIENTISTS working in colleges/universities ... To be open and honest about who is paying for their work. (**funding transparency**) |
| `Q15A` / `Q15B` | Same two items for SCIENTISTS working for COMPANIES ("for example, those who make medicines or agricultural supplies") |
| `WGM_Index` | Wellcome Trust in Scientists Index, mean of Q11C, Q13, Q14A, Q14B, Q15A (1–4; requires ≥3 answered) |
| `wgt` | National weight (use for country-level analysis); `PROJWT` is the pooled population projection weight (not extracted) |
| `Age` | 15–98, 99 = 99+, 100 = Refused (→ NA); `AgeCategories` 1 = 15–29, 2 = 30–49, 3 = 50+ |
| `Gender` | 1 = Male, 2 = Female |
| `Education` | 1 = Primary, 2 = Secondary, 3 = Tertiary (Gallup standardised recode) |
| `Household_Income` | Per-capita household income quintile, 1 = Poorest 20% … 5 = Top 20% (within country) |

Other 2018 items in the raw file but not extracted: Q1–Q10 (science
knowledge/interest, confidence in NGOs/hospitals), Q11A–G (trust in
neighbours, government, journalists, doctors, NGOs, healers), Q16–Q19
(benefit of science), Q20–Q22 (health advice), Q23–Q28 (vaccines), D1/Q29/Q30
(religion vs. science), `WGM_Indexr`, `ViewOfScience`, `Urban_Rural`,
`Subjective_Income`, `EMP_2010`, `Regions_Report`, `WBI`.

### 2020 (csv in the zip; U.S. filter `COUNTRYNEW == 'United States'`)

| Variable | Label (from the 2020 data dictionary docx) |
|---|---|
| `W5C` | Trust Scientists in This Country (same wording as 2018 Q11C) |
| `W6` | Trust Science (= 2018 Q12) |
| `W7A` | Trust Scientists to Find Accurate Information About the World (= 2018 Q13) |
| `W7B` | Trust Scientists to Do Work With Intention of Benefiting Public (= 2018 Q14A, but no longer restricted to college/university scientists) |
| `W7C` | Leaders in National Govt Value Opinions/Expertise of Scientists (new) |
| `W15` | Threat of Climate Change/Global Warming to People in (Country): 1 = Major threat, 2 = Minor threat, 3 = Not a threat, 4 = (not happening), 99 = DK/Ref; asked only of those who had heard of climate change (W13) |
| `WGT` | National weight; `PROJWT` pooled projection weight (not extracted) |
| `WPID_RANDOM` | Random unique case ID (9-digit integer, range 111176093–210871273 in the U.S. rows) |
| `Age` | 15–98, 99 = 99+, 100 = DK/Refused (→ NA); `age_var1` 1 = 15–29, 2 = 30–49, 3 = 50+, 99 → NA |
| `Gender` | 1 = Male, 2 = Female |
| `Education` | 1 = Elementary or less (≤8 yrs), 2 = Secondary (9–15 yrs), 3 = Tertiary (16+ yrs) |
| `Household_Income` | Per-capita household income quintile, 1 = Poorest 20% … 5 = Richest 20% |

**There is no funding-transparency item in 2020** (the 2018 Q14B/Q15B
were dropped). Other 2020 content not extracted: W1–W4, W5A/B/D–G, W8–W11,
W13/W14, W15_1A–E (base COVID decisions on scientific advice: government,
friends, WHO, doctors, religious leaders), W15_2A/B, MH1–MH9 (mental health
module), W27–W30, WP21757–WP21768 (COVID impact, vaccine intent),
`Subjective_Income`, `EMP_2010`, `Global11Regions`, `wbi`.

Neither wave carries **party identification, ideology, race/ethnicity,
religion (2018 only has a named/secular recode `D1`), or state/region**;
geography is country-level only.

## U.S. sample and marginals (from `extract_us.py`)

| | 2018 | 2020 |
|---|---|---|
| U.S. n | 1,006 | 1,001 |
| Gender (M/F) | 542 / 464 | 516 / 485 |
| Age 15–29 / 30–49 / 50+ | 111 / 241 / 654 | 107 / 231 / 654 (9 NA) |
| Education 1/2/3 | 12 / 502 / 485 (7 NA) | 17 / 476 / 505 (3 NA) |
| Income quintile 1–5 | 135 / 160 / 211 / 247 / 253 | 117 / 149 / 201 / 251 / 283 |
| Mean age (unweighted) | 55.0 | 55.6 |

The unweighted sample skews old (65% aged 50+), as usual for RDD phone;
the weight corrects this.

**Trust in scientists in this country** (2018 `Q11C`, 2020 `W5C`), U.S.:

| | 2018 n | 2018 unweighted % | 2018 weighted % | 2020 n | 2020 unweighted % | 2020 weighted % |
|---|---|---|---|---|---|---|
| 1 A lot | 474 | 49.0 | 44.6 | 571 | 57.5 | 54.7 |
| 2 Some | 411 | 42.5 | 44.9 | 359 | 36.2 | 36.6 |
| 3 Not much | 56 | 5.8 | 6.8 | 54 | 5.4 | 7.8 |
| 4 Not at all | 27 | 2.8 | 3.6 | 9 | 0.9 | 0.9 |
| DK/Ref (NA) | 38 | | | 8 | | |

**2018 `Q14B` — trust university scientists "to be open and honest about who
is paying for their work"** (U.S.; 172 DK/Refused, the highest item
non-response in the module):

| | n | unweighted % | weighted % |
|---|---|---|---|
| 1 A lot | 192 | 23.0 | 23.1 |
| 2 Some | 414 | 49.6 | 50.0 |
| 3 Not much | 167 | 20.0 | 18.5 |
| 4 Not at all | 61 | 7.3 | 8.4 |

For comparison, 2018 `Q14A` (benefit the public) weighted: 35.6 / 47.6 /
12.2 / 4.6; `Q13` (accurate information): 50.6 / 41.3 / 6.2 / 1.9; 2020 `W7B`
(benefit the public, all scientists): 42.5 / 44.6 / 8.8 / 4.2.

Item non-response (NA after 98/99 recode), 2018: Q11C 38, Q12 48, Q13 45,
Q14A 88, Q14B 172, Q15A 77, Q15B 107, WGM_Index 45, Age 5, Education 7.
2020: W5C 8, W6 42, W7A 20, W7B 11, W7C 3, W15 13, Age 9, Education 3.

## Caveats

- **Telephone RDD, age 15+**: not directly comparable to 18+ online panels;
  restrict to `Age >= 18` for adult comparisons (loses ~2–3% of cases).
- **4-point scale without a midpoint**, reverse-coded (1 = a lot).
- **No party ID, no race/ethnicity, no ideology, no state** — every
  heterogeneity cut the target study needs beyond age/gender/education/income
  is unavailable. For U.S. trust-in-scientists baselines this source is
  dominated by `pew_atp`, `gss` and `tisp` (which have party and race and
  are more recent); the one item those do not carry is the 2018 `Q14B`
  funding-transparency question in a probability sample (plus its
  company-scientist twin `Q15B`).
- 2018 and 2020 U.S. samples are independent cross-sections (not a panel);
  the 2020 U.S. fieldwork (Aug–Oct 2020) sits inside the pandemic.
- `FIELD_DATE` in both files is a single per-country "study completion
  date" (2018-01-08 for 2018 — evidently a placeholder, since the U.S.
  fieldwork was Jul–Aug 2018 — and 10/01/2020 for 2020), not the interview
  date.
- The 2018 file is a 52.6 MB xlsx that pandas/openpyxl read in ~1–2 minutes;
  use the derived csv.
- PII scan (2026-08-24): the only non-numeric columns in the U.S. rows are
  `COUNTRYNEW` (2020) and `FIELD_DATE`; IDs are `WPID_RANDOM` random
  integers (2020) and no ID at all (2018); geography is country-level. No
  free text, no names, no dates of birth.

## License

**CC BY 4.0 — assumed from Wellcome's site-wide terms; there is no
dataset-specific licence text** on either report page, in the xlsx, in the
2020 data dictionary docx or in the zip. The site-wide statement, at
https://wellcome.org/about-us/our-people/governance/privacy-and-terms
(the page https://wellcome.org/about-us/terms-use redirects there; retrieved
2026-08-24), section "Disclaimer", reads:

> "Unless otherwise stated, content on the Wellcome website is © The
> Wellcome Trust and is licensed under a Creative Commons Attribution 4.0
> International (CC-BY 4.0) licence. This means you can share the content on
> the Wellcome website by copying and distributing it, but you must comply
> with the terms of the CC-BY-4.0 licence, which includes acknowledging
> Wellcome as the copyright owner and providing a link to the source page on
> the Wellcome website."

The data files are served from that website (cms.wellcome.org) and nothing
"states otherwise" for them, so CC BY 4.0 with attribution to Wellcome and
a link to the report page is the operative assumption. The underlying
fieldwork is Gallup's; the report PDFs credit "Gallup" as the data
collector. If in doubt, cite both and do not redistribute the raw world
files (they are reproducible via `fetch.sh` anyway).

## Citation

- Wellcome (2019). *Wellcome Global Monitor 2018*. London: Wellcome Trust.
  https://wellcome.org/reports/wellcome-global-monitor/2018 (data:
  `wgm2018-dataset-crosstabs-all-countries.xlsx`; fieldwork by Gallup).
- Wellcome (2021). *Wellcome Global Monitor 2020: How Covid-19 affected
  people's lives and their views about science*. London: Wellcome Trust.
  https://wellcome.org/reports/wellcome-global-monitor-covid-19/2020 (data:
  `wgm_full_wave2_public_file.zip`; fieldwork by Gallup).
- Methodology: Wellcome (2019) *Wellcome Global Monitor 2018 — Appendix A:
  Methodology*; Wellcome (2021) *Wellcome Global Monitor 2020 — Methodology*
  (both in `downloads/`).
