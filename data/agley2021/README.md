# Agley et al. 2021 — "How science works" infographic → trust in science (RCT)

## Version

Agley J, Xiao Y, Thompson EE, Chen X, Golzarri-Arroyo L. *Effects of
briefly viewing an infographic about science on trust in science, belief
in COVID-19 misinformation, and COVID-19 preventive behavioral intentions:
a two-arm, parallel-group randomized controlled trial.* J Med Internet Res
2021;23(10):e32425. doi:10.2196/32425, PMC8519341. Preregistered
NCT04557241; protocol published before data collection (JMIR Res Protoc
2020;9(12):e24383). Fielded via Prolific 22–24 Jan 2021 (Indiana
University IRB).

Data and code are the article's Multimedia Appendices 1–2 (there is no
separate repository). Downloaded 2026-08-24 with `fetch.sh`: the JMIR
download API worked first try for both appendices (a browser User-Agent
is required); the Europe PMC supplementary-files bundle for PMC8519341
holds byte-identical copies (same sha256) and is the scripted fallback,
and is also used for the article figures. All files are verified against
sha256s pinned in `fetch.sh`.

License: CC BY 4.0 (the article and its appendices; stated on the
article page and in the PMC record).

## Contents

Mirrored under `downloads/` (gitignored; reproduce with
`sh data/agley2021/fetch.sh`; 3.3 MB total):

- `downloads/app2.zip` (101,738 B, sha256 `9a3e831c…858814d`) —
  Multimedia Appendix 2, "CSV datasets used with Appendix 1". Unzipped
  into `downloads/app2/`:
  - `COVID Misinformation final.csv` (294,186 B, `a2c8fac8…24b9e786`) —
    raw Qualtrics export, 1,098 rows × 97 columns (includes screened-out
    and quality-rejected respondents; 1,019 rows carry a `RandomID`).
  - `misinformation_LPA.csv` (71,770 B, `b699c17c…802cfa44`) — the
    cleaned analysis file, 1,017 rows × 27 columns: one row per
    completer, with the arm, the two Trust-in-Science composites, the 7
    misinformation items, the covariates, and the Mplus latent-profile
    assignment (`C`, `CPROB1–3`). **Use this file.**
  - `ClassProb.csv` (70,909 B, `d6a17b2b…6fdcb04a`) — same content as
    `misinformation_LPA.csv` from another machine (Mplus-style: missing
    coded as a blank space, `ARM` = `armraw`, no 0/1 `arm` column);
    verified numerically identical row-for-row. Redundant.
- `downloads/app1.docx` (35,070 B, `46d60afc…8a43aa8`) — Multimedia
  Appendix 1: all analysis code (R data-cleaning syntax, R LMM/EFA, Stata
  path models, SAS, Mplus LPA). The R cleaning block is the de-facto
  codebook for the raw file.
- `downloads/epmc/` — the Europe PMC bundle (`epmc_supplementaryFiles.zip`,
  1.1 MB, server-generated so *not* pinned): `jmir_v23i10e32425_app1.docx`
  and `_app2.zip` (identical to the above), `_app3.pdf` (1,198,190 B,
  `15e577a9…f692d4`; CONSORT-EHEALTH checklist, 55 pp.), and the article
  figures. **`_fig1.jpg` (75,067 B, `6454debd…c248a2`) is the control
  infographic and `_fig2.jpg` (94,815 B, `b5614f21…19b8d`) the
  intervention infographic** — i.e. the verbatim stimuli. `_fig3–7`
  are the CONSORT diagram and result plots.

## Design and key variables

Verified against `misinformation_LPA.csv` and by re-running the app1.docx
cleaning code on the raw export (see "Verification" below).

- **Design.** Two-arm, parallel-group, 1:1 individually randomized
  superiority trial on Prolific's US "representative sample" (quota on
  age, sex, race, ethnicity), N = 1,017 completers (1,014 analysed).
  Pre-randomization quality gates: VPN check, honesty item, two attention
  checks (`RejectVPN`, `RejectHonesty`, `RejectAttention1/2` in the raw
  file; the raw file also has fixed-answer checks `Latveria`, `Phone`,
  `Color_1–5`), and a screener `SIS` (1 = in sample). Flow: consent →
  demographics → quality checks → **pre** Trust in Science Inventory →
  randomized infographic (page timer forces ≥ 60 s; median ~65 s in both
  arms) → 7 misinformation-believability items → vaccination status →
  7 preventive-intention items → covariates → **post** Trust in Science
  Inventory.
- **Arm.** `arm` in `misinformation_LPA.csv`: 0 = control (n = 504),
  1 = intervention (n = 513). `armraw`/`ARM`: 1 = intervention,
  2 = control. In the raw export the arm is not a column: it is the
  page-timer that fired — `Timer1_Page_Submit > 0` ⇔ intervention,
  `Timer2_Page_Submit > 0` ⇔ control (verified: exactly one is non-null
  per completer, 100% agreement with `arm`).
- **Treatments (static images, `downloads/epmc/`).** Intervention
  (fig2): a timeline cartoon of a shopper in 1950/1980/2020 with
  "Scientists say use butter" → "use margarine" → "choose what best
  meets your health needs", framed by "Most scientists commit to
  following a careful sequence of making educated guesses and finding
  answers in a transparent, clear, and honest way" and "When most
  scientists learn they are wrong, they are willing to change their
  minds, because their ultimate goal is usually to learn the truth."
  Control (fig1): same artist, same layout, about how hunting dogs
  "point" at a squirrel. Selected from 5 candidates in a separate
  randomized pilot.
- **Trust in Science (primary outcome), PRE and POST.** 21-item Trust in
  Science and Scientists Inventory (Nadelson et al. 2014), 5-point Likert
  (1 = strongly disagree … 5 = strongly agree), composite = item mean
  after reverse-coding, range 1 (low) – 5 (high). Composites:
  `PRETRUST`, `POSTTRUS` (3 decimals; 3 rows have `POSTTRUS` missing).
  Item text is *not* in the deposit (paper quotes two: "When scientists
  change their mind about a scientific idea, it diminishes my trust in
  their work", "Scientists will protect each other even when they are
  wrong"); take the wording from Nadelson et al. 2014, Sch Sci Math
  114(2):76–86. Raw-file items (recomputed composites match `PRETRUST` /
  `POSTTRUS` to < 0.0005):
  - PRE: `Trust1_1_1`…`Trust1_1_11` and `Trust1_2_1`…`Trust1_2_11`
    (22 columns); **`Trust1_1_3` is an embedded attention check, not a
    scale item** — drop it. Reverse-code (6 − x): `Trust1_1_1, _1_2,
    _1_4, _1_5, _1_7, _1_9, Trust1_2_3, _2_7, _2_8, _2_9, _2_10, _2_11`.
  - POST: `Trust2_1_1`…`Trust2_1_10` and `Trust2_2_1`…`Trust2_2_11`
    (21 columns; block 1 has no attention check, so `Trust2_1_k` =
    `Trust1_1_{k+1}` for k ≥ 3). Reverse-code: `Trust2_1_1, _1_2, _1_3,
    _1_4, _1_6, _1_8, Trust2_2_3, _2_7, _2_8, _2_9, _2_10, _2_11`.
  - Pre–post r = 0.956 (no missing items among completers).
- **Misinformation believability (Aim 2), post-treatment**, 1 = extremely
  unbelievable … 7 = extremely believable. `B1`–`B7` in the LPA file
  (= `Narratives_1`–`_7` raw), mapped via Table 3 profile means:
  `B1` 5G rollout caused COVID-19; `B2` SARS-CoV-2 originated in animals
  (the science-consistent item); `B3` Bill Gates spread COVID-19 to
  expand vaccination; `B4` developed as a military weapon; `B5` deaths
  exaggerated to restrict liberties; `B6` masks cause O2 deficiency /
  CO2 intoxication; `B7` masks probably not helpful. Latent profiles
  `C`: 1 = science-consistent (n = 828), 2 = believes everything
  moderately (n = 42), 3 = misinformation-believing (n = 147);
  `CPROB1–3` posterior probabilities.
- **Preventive behavioural intentions (Aim 3), post-treatment** — raw
  file only (`NPB_1`–`NPB_7`, 1 = unlikely … 7 = likely; not in the LPA
  file): hand-washing, 6-ft distancing, mask, cover coughs, disinfect
  surfaces, monitor health, get vaccinated (`NPB_7`, NA for the 49
  already vaccinated; the paper imputes 7).
- **Demographics / covariates** (LPA-file names; raw names in
  parentheses): `AGE` (`Age`, 19–89, mean 45.4, 12 missing); `GENDER`
  (`Gender`) 1 = male 490, 2 = female 517, 3 = nonbinary 6,
  4 = transgender 4; `RACE` (`Race`) 1 = White 785, 2 = Black 132,
  3 = AIAN 5, 4 = Asian 72, 5 = NHPI 1, 6 = other 22; `ETHNICIT`
  (`Ethnicity`) 1 = Hispanic/Latino 63, 2 = not 954; `RELIGIOU`
  (`Religious`, 1 low – 10 high commitment); `POLITICA` (`Political`,
  1 = liberal … 10 = conservative; mean ≈ 4.2 — no party ID);
  `SEVERITY` (`Severity`, 1–10 perceived seriousness of catching
  COVID-19); `SELFEFFI` (`SelfEfficacy`, 1–5 confidence in avoiding
  it); `FAMBEHAV` (`FamBehav`, 1–7 friends/family avoid crowds);
  `DIAGNOSE` (`Diagnose`, professional diagnosis: 1 = yes 42, 2 = no,
  3 = unsure); `INFECT` (`Infect`, believes was infected: 1 = yes 99,
  2 = no 759, 3 = unsure 159); raw-only `Vaccination` (1 = ≥ 1 dose 49,
  2 = no 965). **Education is not in either file** although the paper
  lists it as a covariate; no income, state, or party ID.
- **Identifier.** `RandomID` (raw) = `ID` (LPA), an 8-digit random
  number, unique; join key between the two files.

## Verification (2026-08-24, pandas)

- Re-running the app1.docx cleaning on the raw export: 1,098 rows →
  reject-flag/SIS/timer filters → 1,017 (= the LPA file, matched 1:1 on
  `RandomID` = `ID`) → minus the 3 listed IDs (44142400, 86337727,
  16373208 — exactly the 3 rows with `POSTTRUS` missing) → 1,014
  analysed (511 intervention / 503 control), as in the paper's Table 1.
- Per arm (LPA file, `PRETRUST`/`POSTTRUS`, 1–5):

  | arm | n | n (post) | pre mean (SD) | post mean (SD) | mean change |
  |---|---|---|---|---|---|
  | 0 control | 504 | 503 | 3.853 (0.621) | 3.900 (0.660) | +0.044 |
  | 1 intervention | 513 | 511 | 3.828 (0.595) | 3.900 (0.639) | +0.070 |

- **Raw difference-in-differences = +0.026** on the 1–5 scale
  (Welch SE 0.012, t ≈ 2.2; ≈ +0.66 pp on 0–100; d ≈ 0.04 of pre-test
  SD 0.61). The paper's covariate-adjusted LMM gives 0.03, SE 0.01,
  t(1000) = 2.16, P = .031 — same number. Both arms drift up ~0.04–0.07
  from pre to post (retest/demand), so use the DiD, not the
  intervention-arm change.
- `ClassProb.csv` equals `misinformation_LPA.csv` on every shared column
  after parsing blank-space as missing.

## PII scan

Clean. Column-by-column scan of all three CSVs: no free-text fields (max
string length 18 = Qualtrics timestamps), no e-mail/IP/URL patterns, no
Prolific IDs, names, ZIPs, or lat/long. Only `RandomID` (8-digit random
number) plus Qualtrics `StartDate`/`EndDate`/`RecordedDate` to the second
(22–24 Jan 2021) and page timers. Smallest cells: nonbinary 6,
transgender 4, NHPI 1, AIAN 5 — treat gender 3/4 and race 3/5 as
collapse-or-drop when reporting.

## Caveats

- The treatment is a **static cartoon infographic**, not a text message;
  the mechanism is "scientists update when wrong", i.e. an explainer, not
  a persuasive appeal. Bridging to text-message arms is by analogy only.
- Outcome is a 21-item 1–5 Likert composite (heavily top-coded: means
  ~3.85, SD ~0.6), not a slider; the **DiD of +0.03 is a lower-bound
  calibration point** for explainer-type arms, sitting well inside the
  retest drift of ~+0.05.
- Only 2 arms; no dose or format variation. No education, income,
  state, or party ID (political orientation 1–10 only). Small
  nonbinary/transgender cells.
- Prolific "representative" quota sample (age, sex, race, ethnicity) —
  not probability-based; fielded over a single weekend in January 2021,
  at the height of the US vaccine rollout debate.
- Misinformation and intention items are post-treatment only (no
  pre-test); the paper found no direct effect on either.

## Citation

Agley J, Xiao Y, Thompson EE, Chen X, Golzarri-Arroyo L. Effects of
briefly viewing an infographic about science on trust in science, belief
in COVID-19 misinformation, and COVID-19 preventive behavioral intentions:
a two-arm, parallel-group randomized controlled trial. J Med Internet Res.
2021;23(10):e32425. https://doi.org/10.2196/32425. CC BY 4.0.

Instrument: Nadelson L, Jorcyk C, Yang D, Jarratt Smith M, Matson S,
Cornell K, Husting V. I just don't trust them: the development and
validation of an assessment instrument to measure trust in science and
scientists. Sch Sci Math. 2014;114(2):76–86. https://doi.org/10.1111/ssm.12051
