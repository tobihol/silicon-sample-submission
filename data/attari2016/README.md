# Attari, Krantz & Weber 2016 / 2019 — Climate researchers' carbon footprints and their credibility

## Version

Three Excel workbooks posted by the first author on her publications page
(https://www.szattari.com/publications), no DOI, no version number. Fetched
2026-08-24 with `fetch.sh` from the pinned URLs below; sha256 pinned at first
download. (`SimpleInterventions_Data.xlsx` on the same page is the Marghetis
et al. 2019 energy dataset, not a credibility experiment, and is not fetched.)

- `Ad_Hom_Final.xls` — https://www.szattari.com/s/Ad_Hom_Final.xls — Attari,
  Krantz & Weber 2016, Survey 1 (Oct 2014) + Survey 2 (Dec 2014).
- `Study1_Policy.xlsx` — https://www.szattari.com/s/Study1_Policy.xlsx —
  Attari, Krantz & Weber 2019, Study 1 (May 2017).
- `Study2_Reformation.xls` — https://www.szattari.com/s/Study2_Reformation.xls
  — Attari, Krantz & Weber 2019, Study 2 (Mar 2016).

Authors: Shahzeen Z. Attari (Indiana University Bloomington), David H. Krantz
(Columbia), Elke U. Weber (Columbia / Princeton). All four surveys were
fielded on Amazon Mechanical Turk (US).

License: **none stated**. The page carries the disclaimer "for educational
use only" — see the License section below.

## Contents

Raw workbooks, mirrored flat under `downloads/` (gitignored, reproduced by
`sh data/attari2016/fetch.sh`). Each has a `Data` sheet and a `Codes` sheet
(the codebook: variable name, verbatim question, coding, recoding notes).

| file | size | sha256 | rows × cols |
|---|---|---|---|
| `downloads/Ad_Hom_Final.xls` | 1,558,528 B | `c77558415d2c4e54c86d31f72252270975527ef20f755f15f35eb905f8b4adc9` | 4,943 × 45 |
| `downloads/Study1_Policy.xlsx` | 766,566 B | `aec1c4aa8bd51e87d226c319fad21ff6c27482ce079e41aea11b8e6bf524e86a` | 3,646 × 45 |
| `downloads/Study2_Reformation.xls` | 558,080 B | `1bac4e065174d04a3255ca0968024121d096a213704e473ffeba09b9b0310114` | 1,772 × 42 |

Derived, PII-free, recoded respondent-level CSVs, built by the committed
`build_derived.py` (`uv run --with pandas --with openpyxl --with xlrd python
data/attari2016/build_derived.py`). Also gitignored (they are respondent-level
derivatives of a no-licence source); the sha256 below are those of the
2026-08-24 build and are reproducible bit-for-bit from the raw workbooks.

| file | size | sha256 | rows × cols |
|---|---|---|---|
| `downloads/derived/attari2016_adhom.csv` | 1,191,880 B | `5b2b735cd0cb3432bccd2023d9f34487e033a4143d97a6c360855938904b7ed4` | 4,943 × 63 |
| `downloads/derived/attari2019_study1_policy.csv` | 844,075 B | `b86b022d72779563f334ef1d704e440fc078e04fc3b9366319f0dab0886e6429` | 3,646 × 61 |
| `downloads/derived/attari2019_study2_reformation.csv` | 410,444 B | `0a040805b1821b0060c7dab15f21d937771eaf6c15fa27a70f35b4c09b8c15bb` | 1,772 × 58 |
| `downloads/derived/arm_summary.csv` | ~4.6 KB | (per-arm aggregates; the only table intended for a deposit) | 36 × 16 |

What `build_derived.py` does: drops `Zip` (Study 1), renames the
check-all-that-apply column `None` to `No_Action`, keeps every other raw
column under its codebook name, reconstructs the arm and its factors, builds
the six credibility items in the credibility direction plus `cred_sum` /
`cred_mean` / `cred_score`, recodes the Qualtrics income quirk (code 8 → 7 =
"> $200,000"; occurs in `Ad_Hom_Final.xls`, 51 rows, not in Study 2 whose
codebook mentions it), adds `gender` ∈ {male, female, other} and `male` (1/0,
other → NA; Ad_Hom's `MaleC` codes other as 3), and coerces the handful of
blank / `"-"` cells in Study 2's open-ended numeric answers (`MPG` 4,
`Flights` 3, `Meat` 3) to NA.

## Design

All studies: MTurk US adults, between-subjects, one ~150-word vignette about
a climate researcher who gives a talk on climate change and advises the
audience to conserve energy; the vignette then reveals something about the
researcher's own energy use. **There is no control arm** (every respondent
sees some footprint information) and **no pre-treatment measure** of
credibility. The manipulation is messenger consistency (does the researcher
practice what they preach), not an informational or persuasive text.

Credibility composite (identical in all studies, verified against both
papers' reported means): six agree–disagree items (1 = strongly agree … 5 =
strongly disagree) — `Consistent`, `Sincere`, `No_Authority` ("I do not trust
the researcher's authority with respect to climate science"), `Good_Reason`,
`No_Cred` ("I am doubtful of the researcher's credibility"), `Advice`. The
four positively worded items are reversed to 5..1; the two negatively worded
ones are kept; `cred_sum` = sum (6..30), `cred_mean` = mean (1..5),
`cred_score` = (sum − 18)/12 ∈ [−1, +1] is the papers' reported scale
(α ≈ 0.85–0.91).

### `attari2016_adhom.csv` — 2016 paper, Survey 1 (7 arms) + Survey 2 (11 arms), N = 4,943

`arm_id` = `S{survey}_C{Condition}`; factors `domain` (fly / home),
`footprint` (high / low / offset / offset_supercharged), `frame`
(later_learn = "You later find out…" vs audience_question = the footprint
comes up through an audience question), `researcher_gender` (male default;
Survey 1 arms 6–7 use a female researcher). Mean `cred_score` from the build:

| survey | cond | arm | n | mean cred_score |
|---|---|---|---|---|
| 1 | 1 | High Fly | 292 | +0.10 |
| 1 | 2 | Low Fly | 288 | +0.65 |
| 1 | 3 | Offset (flies, buys carbon offsets) | 286 | +0.29 |
| 1 | 4 | High Home | 291 | −0.27 |
| 1 | 5 | Low Home | 285 | +0.74 |
| 1 | 6 | High Fly, female researcher | 295 | +0.14 |
| 1 | 7 | Low Fly, female researcher | 291 | +0.65 |
| 2 | 1 | High Fly | 264 | +0.19 |
| 2 | 2 | Low Fly | 264 | +0.57 |
| 2 | 3 | Offset | 262 | +0.36 |
| 2 | 4 | High Home | 268 | −0.19 |
| 2 | 5 | Low Home | 261 | +0.66 |
| 2 | 6 | Audience-question High Fly | 262 | +0.24 |
| 2 | 7 | Audience-question Low Fly | 269 | +0.55 |
| 2 | 8 | Offset "supercharged" (maximally excusing wording) | 265 | +0.36 |
| 2 | 9 | Audience-question Offset supercharged | 267 | +0.39 |
| 2 | 10 | Audience-question High Home | 265 | +0.00 |
| 2 | 11 | Audience-question Low Home | 268 | +0.55 |

Survey 1 n = 2,028, Survey 2 n = 2,915 (both exactly as in the paper). Arms
10/11 reproduce the paper's +0.55 / 0.00.

### `attari2019_study1_policy.csv` — 2019 paper, Study 1, 12 arms, N = 3,646

`Condition` 1–12 = policy × researcher home carbon footprint (odd = low CF,
even = high CF); factors `policy` ∈ {CCS, Carbon tax, Nuclear, Population,
Renewables, Transit}, `footprint` ∈ {low, high}. The researcher advocates the
policy; the footprint is introduced via an audience question (home energy use
only).

| cond | policy | footprint | n | mean cred_score |
|---|---|---|---|---|
| 1 | CCS | low | 309 | +0.53 |
| 2 | CCS | high | 305 | +0.10 |
| 3 | Carbon tax | low | 304 | +0.49 |
| 4 | Carbon tax | high | 303 | +0.05 |
| 5 | Nuclear | low | 300 | +0.46 |
| 6 | Nuclear | high | 301 | −0.00 |
| 7 | Population | low | 305 | +0.46 |
| 8 | Population | high | 301 | +0.01 |
| 9 | Renewables | low | 304 | +0.54 |
| 10 | Renewables | high | 304 | +0.15 |
| 11 | Transit | low | 306 | +0.57 |
| 12 | Transit | high | 304 | +0.12 |

Pooled low CF +0.51 vs high CF +0.07 — exactly the paper's figures.
Additional outcomes: `Policy_Support` (1 strongly support … 5 strongly
oppose; low CF 2.26 vs high 2.45), 14 policy-attribute items incl. `Trust`
("I trust the officials, scientists, and companies that would carry out this
policy"), `Influence` (climate researchers should influence policy). `Time`
= completion seconds.

### `attari2019_study2_reformation.csv` — 2019 paper, Study 2, 6 arms, N = 1,772

`Condition` 1–6 = `domain` {fly (Travel), home} × `reform` {none, some,
complete}: the researcher either still has a high footprint, has partly
reformed, or has fully reformed.

| cond | arm | n | mean cred_score |
|---|---|---|---|
| 1 | Travel, no reform | 297 | +0.22 |
| 2 | Travel, some reform | 294 | +0.55 |
| 3 | Travel, complete reform | 294 | +0.53 |
| 4 | Home, no reform | 296 | −0.16 |
| 5 | Home, some reform | 296 | +0.28 |
| 6 | Home, complete reform | 295 | +0.50 |

## Key variables (all studies unless noted)

- Behavioral intentions, check-all-that-apply after the advice: `Fly` (fly
  less), `Home` (use less energy at home), `Transport` (public transit more),
  `Some` (think about changing some actions; not in Study 2), `No_Action`
  (change nothing), `Other`, `Conserve` (already conserve).
- `No_Influence` (advice will not influence me; not in Study 1), and
  attitudes to scientists as advocates (`Practice` scientists should practice
  what they preach, `Doctor` overweight doctor / dieting advice, `Best`,
  `Research`, `Do_Best` (Ad_Hom only), `Impacts`, `I_Practice`), 1–5.
- Climate beliefs: `CC_Happen` (1 yes definitely … 4 no definitely),
  `CC_Cause` (1 human … 6 other — **code order differs**: Ad_Hom/Study 2 use
  3 = "isn't happening", 4 = "both"; Study 1 uses 3 = "both", 4 = "isn't
  happening"), `CCScientist`/`CC_Scientist` (perceived consensus, 1–4),
  `CC_Important` (1–4), `CC_Sure` (1–4), `CC_Inform` (Ad_Hom only).
- Moderators: `Political` 1 = extremely liberal … 7 = extremely conservative
  (no party ID); `gender`/`male`; `Age` (18–86); `Education` 1–6; `Income`
  1–7 household brackets (None … > $200k; 2013 / 2015 / 2016 income);
  `Courses` science courses (Ad_Hom 1–3; Study 1 0–4); `DegreeC` science
  degree (Ad_Hom, Study 2). **No race/ethnicity anywhere.**
- Energy-use self-reports (Ad_Hom, Study 2): `E_Bill`, `Miles`, `Flights`,
  `People`, plus `Energy_Use` (Ad_Hom), `MPG`, `Meat`, `Children` (Study 2).
  Science-literacy items `Chem_React`, `Exp`, `Gas` (Ad_Hom); attention check
  `Reader` (Study 2; not in the Ad_Hom Data sheet although its codebook lists it).

## Caveats

- MTurk convenience samples 2014–2017, not probability-based; ideology only,
  no party ID, no race.
- No control arm and no pre/post: effects are contrasts between footprint
  descriptions (e.g. low vs high home energy use), not a message-vs-nothing
  ATE. Between-arm differences are very large (≈0.9 on the −1..+1 scale for
  home energy) and concern the credibility of *one described researcher*,
  not trust in climate scientists in general.
- The manipulation is messenger consistency (ad hominem / practice-what-you-
  preach), a different mechanism from informational or persuasive texts.
- Vignette wording is in the papers and their supplements, not in the
  workbooks; the workbooks hold only condition codes.
- Study 1 `Zip` is a 5-digit ZIP alongside age, gender and income —
  re-identifying in combination; dropped from every derived file. No other
  free-text field exists in any Data sheet (Study 1's codebook lists
  `Other_Text` and `Cause_Text`, but they are absent from the data).

## License

**None stated.** The publications page says the files are "for educational
use only". Consequences for this repo:

- the raw workbooks and the respondent-level derived CSVs are never
  committed and never redistributed (both live under the gitignored
  `downloads/`);
- any deposit or public artifact may use **aggregates only** (e.g.
  `arm_summary.csv`: per-arm n, means, SDs, shares), always with attribution
  to the two papers below and a pointer to https://www.szattari.com/publications
  as the source of the microdata.

## Citation

Attari, S. Z., Krantz, D. H., & Weber, E. U. (2016). Statements about climate
researchers' carbon footprints affect their credibility and the impact of
their advice. *Climatic Change*, 138(1–2), 325–338.
https://doi.org/10.1007/s10584-016-1713-2

Attari, S. Z., Krantz, D. H., & Weber, E. U. (2019). Climate change
communicators' carbon footprints affect their audience's policy support.
*Climatic Change*, 154(3–4), 529–545.
https://doi.org/10.1007/s10584-019-02463-0

Data: Attari, S. Z. Publications page, https://www.szattari.com/publications
(files `Ad_Hom_Final.xls`, `Study1_Policy.xlsx`, `Study2_Reformation.xls`),
accessed 2026-08-24.
