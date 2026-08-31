# Beall, Myers, Kotcher, Vraga & Maibach 2017 — Controversy matters: topic × solution controversy and the credibility of an advocating scientist

## Version

Zenodo concept record 794991, "PLOS ONE Submission Dataset", depositor
Lindsey Beall (George Mason University), two versions:

- v1, record 495653 (doi:10.5281/zenodo.495653), published 2017-04-08 —
  the Qualtrics export used for the original article.
- v2, record 1407096, added 2018-08-31 — adds the authors' re-cleaned
  analysis file that underlies the January 2019 correction
  (doi:10.1371/journal.pone.0211289: "errors to the cleaned data set …
  re-downloaded the data from Qualtrics, re-cleaned … several
  coefficients in Tables 2–5 and S1 Table are incorrect"; significance
  pattern unchanged). An earlier correction (doi:10.1371/journal.pone.0196620,
  April 2018) also exists.

Paper: Beall L, Myers TA, Kotcher JE, Vraga EK, Maibach EW (2017).
Controversy matters: Impacts of topic and solution controversy on the
perceived credibility of a scientist who advocates. *PLOS ONE* 12(11):
e0187511. doi:10.1371/journal.pone.0187511. Fielded October–November 2015
by Qualtrics (online panel, quota-sampled to US population on gender, age
and education). Respondents who failed two of three attention checks were
dropped before N = 2,453.

Downloaded 2026-08-24 with `fetch.sh` (Zenodo API + PLOS supplementary
endpoint; no account required). Zenodo md5s match the record metadata.

License: CC BY 4.0 (declared on both Zenodo records; PLOS article and S1
Appendix are CC BY 4.0 as well).

## Contents

Mirrored flat under `downloads/` (gitignored; run `sh data/beall2017/fetch.sh`):

| file | bytes | sha256 |
|---|---|---|
| `downloads/PLOS ONE Data.sav` (Zenodo 495653) | 3,457,289 | `728d3941a190f7ae6417c163da63dff0e611d09eee9da20b1f1b0bb8716bf99f` |
| `downloads/Updated Plos One Data.sav` (Zenodo 1407096) | 82,507 | `aea77e75c9cb13d4f8cf4c86b7fe966ffe0a49d70314b9b1a24ca85a35713826` |
| `downloads/pone.0187511.s001.docx` (PLOS S1 Appendix) | 220,407 | `8bb42bb978f343703309d87c8c745fde74a2757dd8aae24bd819a3dd99fed208` |

- `PLOS ONE Data.sav` — 2,453 rows × 47 columns, SPSS with variable and
  value labels (read with pyreadstat). The 3.4 MB is almost entirely the
  twelve stimulus columns `Q3`–`Q14`, whose *variable labels* carry the
  full op-ed text, plus the long string `Solution`.
- `Updated Plos One Data.sav` — 2,453 rows × 24 columns: derived `Topic`
  (1 Flu, 2 Marijuana, 3 Severe weather, 4 Climate change), `Position`
  (1 Information only, 2 Noncontroversial solution, 3 Controversial
  solution), `Credibility`, the reversed items `RQ19_1/2/7/8`, the
  outcome items, and one variable **absent from v1**: `Q44` political
  ideology (5-point, Very liberal … Very conservative; n = 2,453, no
  missing). Row order is identical to v1 (Q19_1–9 match cell-for-cell on
  all 2,453 rows), so the files can be joined by row position.
- `pone.0187511.s001.docx` — Appendix 1A: the 12 verbatim stimuli;
  Appendix 1B: the questionnaire. The stimulus texts are also in the v1
  variable labels of `Q3`–`Q14`.

## Design and key variables

Between-subjects 4 (topic) × 3 (solution position) = 12 cells, one op-ed
excerpt per respondent attributed to a fictitious "Dr. Dave Wilson,
a recognized international expert in the field of public health /
meteorology / earth science", published in *USA Today*. Every cell starts
with the same ~70-word "informative" paragraph (the problem is more
dangerous and costly than believed; it raises everyone's insurance
costs); the two solution cells append one paragraph in which he
advocates a specific piece of legislation ("My research, and research
conducted by many other experts, suggests that this simple and
inexpensive action is an effective way …"):

| topic | information only | non-controversial solution | controversial solution |
|---|---|---|---|
| flu (`Q3`–`Q5`) | — | hand-washing signs in public buildings | mandatory annual flu shots |
| marijuana (`Q6`–`Q8`) | — | warning labels on marijuana products | stricter medical-marijuana rules, prohibit legalization |
| severe weather (`Q9`–`Q11`) | — | better early-warning systems | restrict building in high-risk areas |
| climate change (`Q12`–`Q14`) | — | tax rebates for EVs / solar panels | carbon tax on all fossil fuels |

**Arm reconstruction.** The string columns `Topic` and `Solution` are
Qualtrics embedded fields and are incomplete (`Topic` blank for 205 rows
= exactly the marijuana × controversial cell; `Solution` blank for 1,013
rows = all 808 information-only rows plus the same 205). Do not use them.
Instead: each of `Q3`–`Q14` is the exposure indicator of one stimulus
page (the variable label holds the stimulus text), constant 1 where
shown and missing otherwise; **every row has
exactly one non-missing column among `Q3`–`Q14`** (verified: 2,453 rows
with exactly one, none with zero or two). Column → cell: `Q3`,`Q6`,`Q9`,`Q12`
= information only; `Q4`,`Q7`,`Q10`,`Q13` = non-controversial solution;
`Q5`,`Q8`,`Q11`,`Q14` = controversial solution; blocks of three = flu,
marijuana, severe weather, climate change. This reproduces the authors'
`Topic`/`Position` in the v2 file exactly (0 disagreements). Cell counts:

| topic | information only | non-controversial | controversial | total |
|---|---|---|---|---|
| flu | 206 | 190 | 225 | 621 |
| marijuana | 213 | 199 | 205 | 617 |
| severe weather | 197 | 200 | 220 | 617 |
| climate change | 192 | 202 | 204 | 598 |
| total | 808 | 791 | 854 | 2,453 |

**Outcome — scientist credibility** (McCroskey & Teven 1999
competence/goodwill/trustworthiness semantic differentials), `Q19_1`–`Q19_9`,
8-point, "Please indicate your impression of Dr. Wilson …". Four items
are anchored high-to-low and must be reversed as `9 − x`: `Q19_1`
(Extremely intelligent : Not at all intelligent), `Q19_2` (Is concerned
about society a great deal : Isn't concerned at all), `Q19_7` (Cares
about society a great deal : Doesn't care at all), `Q19_8` (Extremely
sincere : Not at all sincere). The other five (`Q19_3` competent, `Q19_4`
expert, `Q19_5` sensitive, `Q19_6` trustworthy, `Q19_9` honest) run
low-to-high. Credibility = mean of the nine. Verified: n = 2,452 (one row
with all nine items missing), **M = 5.709, SD = 1.417**, Cronbach α = 0.913;
identical to the authors' `Credibility` in the v2 file (max |diff| = 0).
The article text reports M = 5.77 — that figure comes from the erroneous
cleaned set corrected in 2019; the data give 5.71. Cell means: flu
5.96 / 6.17 / 5.57, marijuana 5.43 / 5.38 / 5.26, weather 5.71 / 5.98 /
5.98, climate 5.61 / 5.91 / 5.60 (info / non-controversial / controversial).

**Other post-treatment items** (all 7-point Strongly disagree … Strongly
agree unless noted): `Q15` op-ed's goal was to provide impartial
information; `Q16` goal was to persuade people to take action; `Q17` he
clearly separated expert analysis from personal views; `Q18_12`–`Q18_15`
perceived motivation ("Dr. Wilson's op-ed was motivated by …" his
evaluation of the scientific evidence / desire for personal promotion
and gain / desire to serve the public / political views); `Q20` how
controversial is Dr. Wilson's research in general (5-point); `Q33` how
controversial is the proposed solution (5-point; asked only in the two
solution arms, n = 1,644).

**Moderators / demographics** (Qualtrics quota variables; pre-treatment
`Q46`–`Q48`, post-treatment `Q49`/`Q50`):

- `Q46` age in years, 18–87, M = 46.3, SD = 16.6.
- `Q47` gender: 1 Male (1,178), 2 Female (1,275).
- `Q48` education: 1 Less than high school (278), 2 High school graduate
  (750), 3 Some college/tech (725), 4 College graduate (450),
  5 Post graduate (250).
- `Q49` ethnicity: 1 Hispanic or Latino (210), 2 Not Hispanic or Latino
  (2,238), missing 5.
- `Q50_1`–`Q50_5` race check-all-that-apply, coded 1 = ticked, missing =
  not ticked: American Indian/Alaska Native 65, Asian 78, Black/African
  American 241, Native Hawaiian/Pacific Islander 17, White 2,110 (50
  multi-racial, 12 with no box ticked).
- `Q44` ideology, **v2 file only**: 1 Very liberal (227), 2 Somewhat
  liberal (404), 3 Moderate (1,106), 4 Somewhat conservative (450),
  5 Very conservative (266).
- `Attn1`–`Attn3` string flags ("1" / blank) marking a failed attention
  check: 142 / 260 / 286 respondents failed exactly one, nobody two
  (consistent with the paper's exclusion rule). `Q1` consent, `Q2`
  instruction page, `Q51` debriefing are constants (= 1).

## Caveats

- Post-only: no pre-treatment credibility or trust measure; the
  within-topic information-only cell is the only baseline (no no-message
  control).
- Credibility of a single fictitious scientist after one ~80–150-word
  op-ed excerpt, not trust in scientists as a group or institution.
- Only three climate-change cells (n = 598); the other nine cells concern
  flu, marijuana and severe weather.
- No party identification, no income; ideology (`Q44`) only via the v2
  file (joined by row position). Race is checkbox-coded with 12 blanks.
- Non-probability Qualtrics quota sample (gender/age/education quotas),
  fielded 2015; no survey weights in the deposit.
- The published tables were corrected in 2019; use the v2 derived
  variables (or the reconstruction above, which matches them) rather than
  figures in the original article text.

## PII

None found. All 47 columns are Likert/numeric codes or the three
embedded-field strings (`Topic`, `Solution`, `Attn*`), whose values are
the fixed stimulus labels. No IP, e-mail, name, ZIP, latitude/longitude,
timestamps, panel/worker IDs or free-text columns; the usual Qualtrics
ResponseID/metadata columns are not in the deposit.

## Citation

Beall L, Myers TA, Kotcher JE, Vraga EK, Maibach EW (2017). Controversy
matters: Impacts of topic and solution controversy on the perceived
credibility of a scientist who advocates. PLOS ONE 12(11): e0187511.
https://doi.org/10.1371/journal.pone.0187511 (corrections:
10.1371/journal.pone.0196620, 10.1371/journal.pone.0211289).

Data: Beall L (2017/2018). PLOS ONE Submission Dataset. Zenodo.
https://doi.org/10.5281/zenodo.495653 (v1), record 1407096 (v2). CC BY 4.0.
