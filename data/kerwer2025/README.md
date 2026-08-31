# Kerwer et al. 2025 — Plain-language summaries of psychological meta-analyses: 18-arm text RCT with METI trust outcome

## Version

PsychArchives record "Dataset for: A randomized controlled study on the
effectiveness of plain language summaries of psychological meta-analyses:
Targeting knowledge, user experience, relevance and trust"
(doi:10.23668/psycharchives.14209, hdl:20.500.12034/9672), published
2024-03-01, single version. Downloaded 2026-08-24 via `fetch.sh` (pinned
bitstream ids + sha256; no account required). Both PsychArchives bitstream
hosts (`pada.` and `www.`) returned 5xx intermittently that day; the script
retries across both. The dataset and codebook bytes are identical to the
verifier's 2026-08-24 scratchpad copies (same sha256).

Authors: Martin Kerwer, Mark Jonas, Marlene Stoll, Gesa Benz, Anita
Chasiotis (Leibniz Institute for Psychology, ZPID). Paper: Zeitschrift für
Psychologie 233(1), 2025 (article DOI not verified in this pass; the deposit
cites it as "in press").

License: **CC-BY-SA 4.0** (declared on the record: `DC.rights` =
`CC-BY-SA 4.0`, https://creativecommons.org/licenses/by-sa/4.0/). Share-alike:
keep this dataset and anything derived from it as separately licensed
material; never merge it into a permissively licensed (CC0 / CC-BY / MIT)
bundle or deposit.

## Contents

All three bitstreams of the record, mirrored flat under `downloads/`
(gitignored; reproduce with `sh data/kerwer2025/fetch.sh`):

- `downloads/20221202_ESM_dataset_publication_anonymized.csv` — 740,221 B,
  sha256 `62a9dde0a48a6e676348fe97e4bc6abbae3e3e267a88455fa09058278b3ad4ba`.
  Respondent-level wide file, 2,451 rows × 73 columns, `sep=';'`,
  `decimal=','`, UTF-8 (`pd.read_csv(..., sep=';', decimal=',')`).
  Bitstream `a7ee57b4-1c4b-4a29-afc8-59aca28889df`.
- `downloads/20221202_ESM_Codebook.csv` — 46,296 B, sha256
  `c361260d98fb1c45eb9ff2a911bcde5da8d90b7eb44a663ed87d4c4526c7049b`.
  73 variable rows (Name / Description / Item Text / Values / Missing Values /
  Level of Measurement), German with English in brackets, `sep=';'`,
  **ISO-8859-1** (`encoding='latin-1'`). Bitstream
  `c1707c2e-f05e-4e77-a938-04ce67132a70`.
- `downloads/20230921_ESM_R_Output.html` — 1,569,371 B, sha256
  `3ac80dd8fd7b73a3e3e12d6da5f9919e8b70da1b0029d6e7f0849c5c4a4e8e4f`.
  Authors' knitted RMarkdown (R 4.3.1, lme4/lmerTest) with every model and
  descriptive in the paper. It reads a *pre-anonymisation* file
  (`20220531_dataset_publication.csv`) that also had `duration`, `s_sex`,
  `s_age`, `s_schule`; those columns were stripped from the deposit, but the
  log prints their aggregate descriptives and the quota-cell decoding (see
  Caveats). Bitstream `339ce463-738b-48b6-9b1d-90097c7f26b9`.

Not vendored (per the scouting recipe): the two Frontiers 2021 deposits from
the same group (10- and 32-condition pilot studies, no trust outcome).

## Design

German general-population online quota sample (12 cells = gender × age band
× school track, see Caveats), fielded 2022 by ZPID. Each respondent was
randomised to **one of 18 between-subject text conditions** (`Bedingung`
1–18) and then read **two** research summaries in that condition, one per
topic, each followed by the same outcome block:

- exposure `_1` = meta-analysis on **action video games and perception**
  (`pls == "Videospiele"` in the R output),
- exposure `_2` = meta-analysis on **psychotherapy for depression**
  (`pls == "Psychotherapie"`).

The suffix-to-topic mapping is fixed in the authors' reshape code; whether
presentation order was counterbalanced is not recorded in the deposit. For a
clean between-subject ATE use the `_1` block only (verified below); the
authors analyse both blocks in a long format with random intercepts for `id`
and topic.

### Factor structure of the 18 arms

`Bedingung` is a single categorical arm code; the five `s_iv_*` string
columns are its factor decomposition. Verified: every `Bedingung` maps to
exactly one combination of the five factors, and the 18 combinations are
distinct. The design is an **incomplete factorial** — a PLS core with
one-factor-at-a-time statement manipulations plus a 4-cell abstract
comparison, not a full crossing:

| `Bedingung` | summary type | # effects | COI statement | publication-bias statement | practical-relevance statement | words (`_1` / `_2`) | n all | n analysis |
|---|---|---|---|---|---|---|---|---|
| 1 | PLS | 4 | none | none | none | 415 / 523 | 141 | 131 |
| 2 | PLS | 4 | none | none | **included** | 469 / 546 | 139 | 129 |
| 3 | PLS | 4 | none | lay: authors provide no information | none | 506 / 585 | 134 | 123 |
| 4 | PLS | 4 | none | lay: publication bias likely | none | 501 / 580 | 137 | 125 |
| 5 | PLS | 4 | none | lay: authors provide no information | **included** | 560 / 633 | 140 | 122 |
| 6 | PLS | 4 | none | lay: publication bias likely | **included** | 555 / 628 | 124 | 113 |
| 7 | PLS | **1** | none | none | none | 305 / 327 | 141 | 138 |
| 8 | PLS | **7** | none | none | none | 576 / 667 | 131 | 125 |
| 9 | PLS | 1 | **no COI** | none | none | 331 / 353 | 134 | 124 |
| 10 | PLS | 4 | **no COI** | none | none | 441 / 524 | 139 | 132 |
| 11 | PLS | 7 | **no COI** | none | none | 602 / 693 | 141 | 127 |
| 12 | PLS | 1 | **COI** | none | none | 337 / 359 | 131 | 120 |
| 13 | PLS | 4 | **COI** | none | none | 447 / 530 | 131 | 118 |
| 14 | PLS | 7 | **COI** | none | none | 608 / 699 | 142 | 132 |
| 15 | **Abstract** | 1 | none | none | none | 220 / 159 | 134 | 127 |
| 16 | **Abstract** | 4 | none | none | none | 262 / 219 | 143 | 130 |
| 17 | **Abstract** | 7 | none | none | none | 338 / 275 | 132 | 117 |
| 18 | **Abstract** | 4 | none | scientific: publication bias likely | none | 273 / 228 | 137 | 123 |

Factor levels (`s_iv_*` values, verbatim): `s_iv_research_summary_type`
∈ {PLS, Abstract}; `s_iv_number_effects` ∈ {1, 4, 7}; `s_iv_conflict_of_interest`
∈ {no statement, statement: no COI, statement: COI}; `s_iv_publication_bias`
∈ {no statement, lay statement "authors provide no information", lay
statement "publication bias likely", scientific statement "publication bias
likely" (abstract wording, arm 18 only)}; `s_iv_practical_relevance`
∈ {no statement, statement included}. Word counts are the authors' per-arm
stimulus lengths hard-coded in the R output (German texts); the stimuli
themselves are **not** in the deposit.

Sub-designs the paper actually tests (all within the `_1`/`_2` structure):
H1 PLS vs abstract at matched effect count (7/8/1 vs 15/16/17); H2 number of
effects within PLS (7 vs 1 vs 8); H3 COI statement within PLS
(1,7,8 vs 9,10,11 vs 12,13,14); publication-bias and relevance statements
(1 vs 2–6; 16 vs 18).

### Outcomes (per exposure, `_1` and `_2`)

- **METI** (Münster Epistemic Trustworthiness Inventory, Hendriks et al.
  2015), 14 bipolar 7-point semantic differentials about "the researchers
  whose review I just read a summary of": `pls_METI_{1..14}_k`, all 1–7,
  higher = more trustworthy. Item order in the deposit is interleaved, not
  grouped by subscale. Verified against the deposit's own subscale means
  (`pls_METI_Exp_k`, `_Int_k`, `_Ben_k`, max abs diff < 1e-9):
  - Expertise = items {1 intelligent, 7 qualified, 8 experienced,
    9 well-educated, 10 professional, 13 competent} (6 items);
  - Integrity = items {2 just, 6 fair, 12 honest, 14 sincere} (4 items);
  - Benevolence = items {3 ethical, 4 considerate, 5 responsible, 11 moral}
    (4 items).
  No missing METI cells in the analysis sample (both exposures).
- **Credibility of the evidence**, single item `pls_credibility_k`
  ("The results of the presented review are credible"), 1–8 agree scale
  (10 missing in `_1`).
- User experience: `pls_accessibility_k`, `pls_understanding_k`,
  `pls_empowerment_k` (1–8); topic relevance `pls_relevance_k` (1–8);
  epistemic emotions `pls_cur_k` / `pls_bor_k` / `pls_con_k` / `pls_frust_k`
  (codebook says 0–5, observed 1–5); content knowledge
  `pls_knowledge_{1..4}_k` (4-option forced choice, raw option 1–4, not
  scored).
- Person-level: `s_interest` (interest in psychological research, 1–8;
  observed 4–8, so the panel was screened on interest ≥ 4),
  `s_knowledge_pub_bias`, `s_knowledge_evidence` (0/1 correct).
- Bookkeeping: `id` (1–2451), `dispcode` (22 interrupted / 31 completed /
  32 completed after interruption), `dropout` (TRUE iff dispcode 22),
  `quota_assignment` (1–12).

## Verification (2026-08-24, pandas)

- N total = **2,451** (ids unique). `dispcode`: 31 → 2,000; 32 → 256; 22 → 195.
  `dropout` is exactly `dispcode == 22` (195 TRUE).
- Analysis sample (`dispcode ∈ {31, 32}` and `dropout == FALSE`) =
  **2,256**. Per-arm n (all / analysis) as in the table above: analysis n
  ranges 113–138, mean 125.3.
- Quota cells (analysis sample): 191, 194, 197, 195, 198, 198, 188, 198,
  119, 199, 193, 186 for cells 1–12 (cell 9 = young men with Hauptschule
  under-filled, as in the authors' log).
- METI composite for the first exposure = mean of the 14 `_1` items
  (analysis sample; overall mean 5.565, SD 1.161; item-total r ≥ 0.85):

| `Bedingung` | n | METI_1 mean | METI_1 SD | credibility_1 mean | credibility_1 SD |
|---|---|---|---|---|---|
| 1 | 131 | 5.786 | 1.031 | 6.076 | 1.450 |
| 2 | 129 | 5.652 | 1.224 | 5.984 | 1.577 |
| 3 | 123 | 5.620 | 1.142 | 5.911 | 1.449 |
| 4 | 125 | 5.644 | 1.077 | 5.831 | 1.539 |
| 5 | 122 | 5.629 | 1.055 | 5.934 | 1.557 |
| 6 | 113 | 5.512 | 1.248 | 5.777 | 1.541 |
| 7 | 138 | 5.558 | 1.157 | 5.949 | 1.572 |
| 8 | 125 | 5.575 | 1.166 | 5.919 | 1.549 |
| 9 | 124 | 5.661 | 1.112 | 5.967 | 1.639 |
| 10 | 132 | 5.642 | 1.160 | 6.008 | 1.604 |
| 11 | 127 | 5.648 | 1.157 | 6.151 | 1.357 |
| 12 | 120 | 5.383 | 1.252 | 5.750 | 1.552 |
| 13 | 118 | 5.465 | 1.155 | 5.538 | 1.632 |
| 14 | 132 | 5.470 | 1.189 | 5.656 | 1.686 |
| 15 | 127 | 5.366 | 1.159 | 5.480 | 1.699 |
| 16 | 130 | 5.548 | 1.269 | 5.845 | 1.707 |
| 17 | 117 | 5.491 | 1.051 | 5.672 | 1.733 |
| 18 | 123 | 5.494 | 1.248 | 5.732 | 1.680 |

  Arm means span 5.37–5.79 (SD of the 18 arm means 0.108, i.e. ≈ 0.09 of a
  within-arm SD): a near-null ATE-dispersion prior for content variants of
  long science texts. Marginal contrasts on METI_1: PLS 5.591 vs abstract
  5.475; COI statement 5.441 vs no-COI statement 5.650 vs none 5.574 (the
  paper's one reliable trust effect); effects 1/4/7 → 5.494/5.602/5.546;
  publication-bias and relevance statements within ±0.07 of their controls.

## Caveats

- **German general-population quota sample**, not probability-based;
  screened on interest in psychological research (≥ 4 of 8). Texts are
  German plain-language summaries / abstracts of psychology meta-analyses
  (video games & perception; psychotherapy for depression) — long stimuli
  (159–699 words), not short persuasive messages; the trust target is "the
  researchers who wrote this review", not scientists in general.
- **No respondent-level demographics released.** The deposit keeps only the
  unlabelled 12-cell `quota_assignment`. The R output, however, prints the
  authors' cell labels and cross-tabs, from which the cells decode as
  gender × age band × highest school track (G: m = male / w = female;
  A: h = 45+ / n = 18–44; S: h = Abitur / m = Realschule / n = Hauptschule):
  1 GmAhSh, 2 GmAhSm, 3 GmAhSn, 4 GwAhSh, 5 GwAhSm, 6 GwAhSn, 7 GmAnSh,
  8 GmAnSm, 9 GmAnSn, 10 GwAnSm, 11 GwAnSh, 12 GwAnSn. So gender, a
  two-band age and a three-level education proxy are recoverable per row;
  treat the decoding as reconstructed (it is not in the codebook). Aggregate
  demographics from the log: 52.7% female; age 18–90, mean 47.5 (SD 15.2);
  school track 32.8% Abitur / 34.4% Realschule / 32.8% Hauptschule; median
  completion 20.8 min. No party, ideology, income or region.
- All outcomes are Likert / semantic-differential (1–7, 1–8); nothing on a
  0–100 slider. Ceiling-ish: METI means ≈ 5.6 of 7.
- Two exposures per person in the same arm; `_2` is not an independent
  replication of `_1` (same respondent, different topic, possibly order
  effects).
- Codebook is ISO-8859-1 with occasional mojibake (e.g. `gro§` for `groß`);
  the codebook's stated 0–5 range for the epistemic-emotion items does not
  match the data (1–5).

## PII scan (2026-08-24)

Dataset: 68 numeric/boolean columns plus five `s_iv_*` factor strings with
2–4 fixed levels each; no free text, no timestamps, no IP/e-mail/phone/date
patterns, `id` is a 1–2451 sequence. Codebook: variable documentation only.
R output: one e-mail address, `aidan@php.net`, inside the embedded jQuery
"Sticky Tabs" plugin header (library credit, not respondent data); author
name in the document header is "removed for blind review"; no local file
paths. Clean.

## Citation

Kerwer, M., Jonas, M., Stoll, M., Benz, G., & Chasiotis, A. (2025). A
randomized controlled study on the effectiveness of plain language summaries
of psychological meta-analyses: Targeting knowledge, user experience,
relevance and trust. *Zeitschrift für Psychologie, 233*(1).

Kerwer, M., Jonas, M., Stoll, M., Benz, G., & Chasiotis, A. (2024). Dataset
for: A randomized controlled study on the effectiveness of plain language
summaries of psychological meta-analyses: Targeting knowledge, user
experience, relevance and trust [Data set]. PsychArchives.
https://doi.org/10.23668/psycharchives.14209 (CC-BY-SA 4.0)

METI instrument: Hendriks, F., Kienhues, D., & Bromme, R. (2015). Measuring
laypeople's trust in experts in a digital age: The Muenster Epistemic
Trustworthiness Inventory (METI). *PLoS ONE, 10*(10), e0139309.
