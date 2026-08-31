# ANES Time Series 2020 and 2024 — American National Election Studies

## Version

Two ANES Time Series Study full releases, downloaded 2026-08-24 directly from
electionstudies.org (no account; direct links and pinned sha256 hashes are in
`fetch.sh`):

- **ANES 2020 Time Series Study, Full Release**, CSV version dated
  February 10, 2022. Pre-election survey fielded Aug 18 – Nov 3, 2020;
  post-election re-interviews Nov 8, 2020 – Jan 4, 2021. N = 8,280
  pre-election / 7,449 post-election (fresh address-based cross-section
  5,441/4,779 by web, phone and video, plus the 2016–2020 panel 2,839/2,670).
  Zip: `https://electionstudies.org/wp-content/uploads/2022/02/anes_timeseries_2020_csv_20220210.zip`
  Codebook (HTML): `https://electionstudies.org/wp-content/uploads/2026/04/anes_timeseries_2020_userguidecodebook_accessible_html.html`
- **ANES 2024 Time Series Study, Full Release**, CSV version dated
  May 19, 2026 (codebook "User Guide and Codebook, May 19, 2026").
  Pre-election survey fielded Aug 3 – Nov 5, 2024; post-election
  re-interviews Nov 7, 2024 – Feb 17, 2025. N = 5,521 pre-election / 4,964
  post-election (1,042 fresh in-person, 2,308 fresh web, 2,171 panel
  2016–20–24; by pre mode 966 face-to-face, 76 phone, 4,234 internet, 245
  paper-and-pencil).
  Zip: `https://electionstudies.org/wp-content/uploads/2026/05/anes_timeseries_2024_csv_20260519.zip`
  Codebook (HTML): `https://electionstudies.org/wp-content/uploads/2026/04/anes_timeseries_2024_userguidecodebook_accessible_html.html`

Both studies are address-based probability samples of the non-institutional
U.S. **citizen** population aged 18+ in the 50 states and DC.

## Contents

- `fetch.sh` — re-downloads the four files below from the pinned URLs into
  `downloads/` (browser User-Agent + HTTP/1.1 needed to pass Cloudflare;
  retries intermittent 403s), verifies sha256, and unpacks the zips. The two
  HTML codebooks are hashed after blanking Cloudflare's per-request
  email-obfuscation tokens (`email-protection#…`, `data-cfemail="…"`), since
  the bytes on disk differ between downloads while the content does not.
- `downloads/anes_timeseries_2020_csv_20220210.zip` — 7,777,954 B,
  sha256 `70450eb6bf7b8f34…`
  - `downloads/anes_timeseries_2020_csv/anes_timeseries_2020_csv_20220210.csv`
    — 39,668,110 B, sha256 `9e7a4d585fa88ef3…`; 8,280 rows × 1,771 columns
  - `downloads/anes_timeseries_2020_csv/anes_timeseries_2020_userguidecodebook_20220210.pdf`
    — 1,773,718 B, sha256 `2052f63635638aaf…` (PDF codebook shipped in the zip)
- `downloads/anes_timeseries_2020_userguidecodebook_accessible_html.html` —
  2,930,879 B, normalised sha256 `c86dd06720d0a73c…`
- `downloads/anes_timeseries_2024_csv_20260519.zip` — 6,516,359 B,
  sha256 `31082da127f1ebcf…`
  - `downloads/anes_timeseries_2024_csv/anes_timeseries_2024_csv_20260519.csv`
    — 25,127,905 B, sha256 `f80a276e64a5653a…`; 5,521 rows × 1,738 columns
  - `downloads/anes_timeseries_2024_csv/anes_timeseries_2024_userguidecodebook_20260519.pdf`
    — 1,877,868 B, sha256 `fbad3417cc50b189…`
- `downloads/anes_timeseries_2024_userguidecodebook_accessible_html.html` —
  3,637,886 B, normalised sha256 `ffbfaed474df7367…`

The CSVs are comma-separated, one row per respondent, UTF-8 with a BOM (read
with `encoding="utf-8-sig"`; otherwise the first column shows as
`ï»¿version`). All values are numeric codes; labels are in the codebooks.

## Key variables

Verified 2026-08-24 by loading both CSVs with pandas; every variable named
below is present.

### Trust / attitude toward scientists

- **2020 `V202173`** — POST: feeling thermometer, "How would you rate:
  Scientists", 0–100 (one of 17 randomized thermometer targets). Codes:
  -9 refused (65), -7 no post data/incomplete (77), -6 no post interview
  (754), -5 breakoff (14), -4 technical error (1), **998 don't know (2)**.
  Valid 0–100: **n = 7,367**, unweighted mean 79.3 (SD 20.2), median 85,
  weighted (`V200010b`) mean 78.0. Quantiles 10/25/50/75/90 = 50/70/85/100/100.
  **Heaping**: 98.8% of valid answers are multiples of 5, 70.9% multiples of
  10; 29.7% at 100, 11.6% at 50, 0.6% at 0. Top values: 100 (2,190), 85
  (1,725), 70 (914), 50 (854), 60 (560), 90 (287), 80 (185), 95 (128), 40
  (122), 75 (113). The intro defines 50 as neutral and 50–100 as warm, and
  the mass at 85, 70, 60, 40 (the labelled points of ANES's thermometer
  show-card) marks this as a labelled thermometer, not a free slider.
- **2024 `V242420`** — POST: CSES6 Q07d, "(How about:) Scientists? Do you
  trust them a lot, trust them somewhat, do not trust them very much, or do
  not trust them at all?" 1 = trust a lot … 4 = do not trust at all
  (**higher = less trust**; reverse for a trust score). Codes: -9 refused
  (18), -8 DK (3), -7 insufficient partial (40), -6 no post interview (472),
  -5 breakoff (41), -1 inapplicable (245; the paper-and-pencil cases).
  Valid: **n = 4,702**; unweighted 36.1% / 47.7% / 12.0% / 4.2%; weighted
  (`V240108b`) 34.6% / 48.5% / 12.3% / 4.6%.
- GSS confidence in the scientific community (`V202635` 2020, `V242620`
  2024; 1 a great deal / 2 only some / 3 hardly any) exists in both files but
  is asked **only of the GSS-linked subsample** (universe "IF R IS IN GSS
  SAMPLE"): all other respondents are -1 inapplicable (7,346 in 2020; 4,931
  in 2024). Not usable as a general-population item here.

### The six moderators

| moderator | 2020 | 2024 | coding |
|---|---|---|---|
| party ID | `V201231x` | `V241227x` | 7-pt summary: 1 strong Dem, 2 not very strong Dem, 3 Ind-Dem, 4 Independent, 5 Ind-Rep, 6 not very strong Rep, 7 strong Rep; -9 refused, -8 DK, -4 error (2024) |
| race/ethnicity | `V201549x` | `V241501x` | 1 White non-Hisp, 2 Black non-Hisp, 3 Hispanic, 4 Asian/NHPI non-Hisp, 5 Native American/other non-Hisp, 6 multiple races non-Hisp; -9/-8/-4 |
| education | `V201511x` | `V241465x` | 5-cat: 1 < HS, 2 HS, 3 some post-HS no BA, 4 BA, 5 graduate; -9/-8/-4, -2 other-specify not codable |
| income | `V201617x` | `V241566x` (28 cats), `V241567x` (6 cats, incl. PAPI) | 2020: 22 bands, 1 < $10k … 22 ≥ $250k. 2024: `V241566x` 28 bands 1 < $5k … 28 ≥ $250k, -1 for the 245 PAPI cases; `V241567x` six bands (1 < $10k, 2 $10–30k, 3 $30–60k, 4 $60–100k, 5 $100–250k, 6 ≥ $250k) covers everyone |
| age | `V201507x` | `V241458x` | years, top-coded at 80; -9 refused (348, 2020) / -2 no exact birth date (279, 2024) |
| gender | `V201600` "What is your sex?" | `V241551` "What is your gender?" | 2020: 1 male, 2 female. 2024: 1 man, 2 woman, 3 nonbinary (46), 4 something else (18); -1 PAPI (245) |

Counts, 2020 (unweighted): party 1,961/900/975/968/879/832/1,730; race
5,963/726/762/284/172/271; education 376/1,336/2,790/2,055/1,592; gender
3,763 male / 4,450 female. 2024: party 1,314/616/714/380/716/577/1,166;
race 3,946/508/582/197/33/188; education 283/973/1,738/1,384/1,087;
gender 2,397/2,773/46/18.

### Weights and design

- 2020: `V200010a` full-sample pre-election weight (all 8,280 rows,
  mean 1), `V200010b` full-sample post-election weight (7,453 rows > 0,
  mean 1); `V200010c`/`V200010d` are the matching stratum/PSU variables.
  `V200004` = 1 pre only / 3 pre and post; `V200003` sample type.
- 2024: `V240107a`/`V240107b` pre/post weights for panel + FTF + web
  **including** PAPI (5,521 / 4,964 rows > 0); `V240108a`/`V240108b`
  pre/post weights **excluding** PAPI (5,276 / 4,764). Use `V240108b` for
  `V242420` (which is inapplicable for PAPI). `V240003` sample type
  (1 panel, 2 fresh web, 3 fresh FTF).
- Missing-value convention: **all negative codes are missing** (-9 refused,
  -8 DK, -7 deleted incomplete, -6 no post interview, -5 breakoff, -4
  error, -2 not codable, -1 inapplicable); the 2020 thermometers also use
  **998 = don't know where to rate** (and 999 = don't recognize on the
  person thermometers; not present for `V202173`). Recode `< 0` and
  `>= 998` to NA.

## Caveats

- **Universe is U.S. citizens 18+ (eligible voters)**, not all adults; the
  target study's opt-in panel with census quotas draws on all adults.
- **2024 has no scientists feeling thermometer.** The 0–100 item exists in
  2020 only; 2024 offers a 4-point CSES trust item. The two are not the same
  construct or scale.
- The thermometer is about "scientists" generically (affect), not climate
  scientists, and not a TISP-style trust scale. No experiment, no
  treatment arms.
- 2020 was fielded during COVID-19 (Aug 2020 – Jan 2021), which may
  inflate the scientist thermometer relative to other years.
- Post-election items are subject to panel attrition (10% of the 2020
  pre-election sample has no post interview; 2024 post weights cover 4,964
  of 5,521).
- The 2024 -1 codes on `V242420`, `V241551`, `V241566x` are the 245
  paper-and-pencil respondents; drop them or use `V240108b`.
- Use the design variables for standard errors; the raked weights alone
  understate uncertainty.

## License

ANES Terms of Use (electionstudies.org/data-center): (1) use the datasets
solely for research or statistical purposes and not for investigation of
specific survey respondents; (2) make no use of the identity of any survey
respondent discovered intentionally or inadvertently, and advise ANES of any
such discovery; (3) cite ANES data and documentation in work that uses them
and send citations to the ANES bibliography; (4) ANES and its funders bear no
responsibility for uses or interpretations. There is **no explicit
redistribution licence** and no CC/open licence statement. The files are
therefore kept in the gitignored `downloads/` folder and are never committed
or deposited; anyone reproducing this repo runs `sh fetch.sh` to re-download
and hash-verify them. No login or DUA was required for the download. The
public-use files are de-identified (no names, addresses, geocodes or contact
data; see PII scan below).

PII scan 2026-08-24: header regex over all 1,771 (2020) and 1,738 (2024)
column names for IP/e-mail/name/zip/postal/lat/lon/address/phone/SSN/DOB
returned no hits; every column except `version` and `V160001_orig` (2016
panel case ID) follows the `V2xxxxx` pattern. Respondent identifiers are
study case IDs (`V200001`, `V240001`) only.

## Citation

- American National Election Studies. 2021. *ANES 2020 Time Series Study
  Full Release* [dataset and documentation]. February 10, 2022 version.
  www.electionstudies.org
- American National Election Studies. 2025. *ANES 2024 Time Series Study
  Full Release* [dataset and documentation]. May 19, 2026 version.
  www.electionstudies.org

ANES is a collaboration of Duke University, the University of Michigan, the
University of Texas at Austin and Stanford University, funded by the National
Science Foundation (2024: grant SES-2209438).

## Why it is here

The only probability-sample 0–100 rating of scientists with all six target
moderators (2020 thermometer: heaping and shape prior, subgroup levels by
party/race/education/income/age/gender) and the freshest probability-sample
trust-in-scientists point (2024 CSES item, fielded Nov 2024 – Feb 2025).
Baseline levels and gradients, not effects.
