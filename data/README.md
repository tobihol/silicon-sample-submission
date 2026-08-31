# data/ — public survey datasets, one folder per dataset

Training / profile-source data for all ideas. **Public data only** — everything
here is openly downloadable for research; the licence column says what may be
redistributed (several sources — Pew, CCAM, ANES, Attari — permit research use
but not redistribution, so raw files are fetched, never committed or deposited).
(The gssim projects' restricted datasets — GLES, PSID, NSDUH, … — stay out of
this repo; their raw data cannot leave the cluster.)

Inside the container these folders are mounted **read-only** at
`/workspace/datasets/<name>` (see `utils/container/`).

Each dataset folder contains:

- `README.md` — provenance: version, DOI/URL, download date, citation
- `downloads/` — the raw data files plus documentation (codebook, questionnaire)
- optionally a `dataset_<name>.json` manifest (carried over from gssim)

| dataset | what | size | source |
|---|---|---|---|
| `acs` | American Community Survey 2018 1-Year PUMS, person + housing files (housing adds household income `HINCP`, joined via `SERIALNO`). Person file copied from `gssim_prototype`; synthetic copies not carried over. | 3.0G | U.S. Census Bureau, public |
| `agley2021` | Agley et al. 2021 (JMIR): preregistered 2-arm Prolific US-quota RCT, N=1,017 — 60-s "how science works" infographic vs control; 21-item Trust in Science Inventory (1–5) **pre AND post**, DiD +0.03 (SE 0.01); 7 COVID-misinformation + 7 intention items; stimuli JPGs included. No education/party. | 3.3M | JMIR appendices / Europe PMC, CC BY 4.0 |
| `altenmueller2024` | Altenmüller, Wingen & Schulte 2024: randomized scientist-identity vignettes (liberal vs conservative institute; economists vs sociologists) → METI trust in scientists (7-pt), respondent ideology/party moderator; controlled N=2,859 (US MTurk + 1 German sample) + 20-discipline stereotype/trust sliders. | 3M | OSF, CC BY 4.0 |
| `anes` | ANES Time Series 2020 (8,280/7,449) + 2024 (5,521/4,964), probability samples of US citizens 18+: 2020 `V202173` 0–100 scientists thermometer (n=7,367; 98.8% on multiples of 5, 30% at 100), 2024 `V242420` 4-pt CSES trust in scientists; all six moderators + weights both years. No experiment; 2024 has no thermometer. | 85M | electionstudies.org, ANES terms of use (research, cite, no re-identification; no redistribution licence) — reproduce via `fetch.sh` |
| `attari2016` | Attari, Krantz & Weber 2016/2019 (Climatic Change): 4 MTurk vignette experiments (N=10,361; 18+12+6 arms) on a climate researcher's carbon footprint → 6-item **researcher-credibility composite** (−1..+1), conservation intentions, 2019 policy support + policy-trust item; ideology 1–7, no race, no control arm, no pre/post. | 6.0M | szattari.com, no license, "educational use only" — raw + respondent-level derived disk-only; aggregates with attribution |
| `bago2025` | Bago, Muller & Bonnefon 2025 (Nat. Clim. Chang.): LLM-personalized climate headlines, US Prolific n=1,999, 2 arms (personal vs original), **0–100 pre/post belief sliders** (happening/cause/risk) + headline upvote/bookmark behavior; effects strongest among sceptics (HTE-curve asset). Engagement treatment, not a persuasive appeal; treat belief change as ITT; no income. | 18M | GitHub / Zenodo, CC BY 4.0 |
| `beall2017` | Beall et al. 2017 (PLOS ONE): 4 topics (flu, marijuana, severe weather, climate) × 3 (info-only / non-controversial / controversial solution) op-ed by a fictitious scientist → 9-item credibility (1–8, α .91); N=2,453 US Qualtrics quota, post-only; age/gender/education/race/Hispanic, ideology via the corrected v2 file; no party/income. | 4.3M | Zenodo 495653 + 1407096, PLOS S1; CC BY 4.0 |
| `bbprime2025` | BB-PRIME Phase II climate intervention tournament (Sinclair et al. 2025): 18 arms, N≈7,600, individual-level **0–100 message-sharing** + petition outcomes, moderators; joins on `SID`. | 321M | OSF, no license — cite only |
| `ccam` | Climate Change in the American Mind, cumulative microdata 2008–2024 (31 waves, 35,309 rows): climate beliefs/worry/policy with demographics and party. **No-redistribution terms** — never include the raw file in a public deposit. | 6M | Yale YPCCC + Mason 4C via OSF |
| `ces` | Cooperative Election Study: 2024 Common Content (60,000 × 694) + cumulative 2006–2025 (718,955 × 109). Party ID, education, income at large n. | 0.3G | Harvard Dataverse, CC0 |
| `dablander2025` | Dablander et al. 2025 (RSOS registered report): 6-arm 2×3 scientist-protest vignette experiment, US Prolific n=2,856, **scientist-credibility outcomes** (source + general, 1–5) + policy support + **0–100 behavioral donation**, all six target moderators. Registered-report nulls = calibration prior for small trust effects. Verbatim vignettes in the CC-BY ESM. | 4M | OSF data no license — cite only; ESM CC BY 4.0 |
| `gatewaybelief` | Gateway (mis)Belief pooled data (van der Linden 2017 / Maertens 2020, 2025): 0–100 consensus slider **and** 1–7 Likert climate items in the same respondents, pre/post a consensus message — the empirical Likert→slider bridge. No codebook; the authors' R scripts document the variables. | 3.5M | OSF, no license — cite only |
| `geiger2026` | Geiger et al. 2026 (JEVP) reanalysis deposit re-releasing (a) van der Linden et al. 2019 US consensus RCT — n=6,301, 2 arms, pre/post belief/worry/policy (1–7) + 0–100 consensus, party — and (b) Većkalov et al. 2024 27-country subset with **1–7 trust-in-climate-scientists** under 3-arm message randomization (US ~120/arm). NB 40% of vdL-treated report exactly 97 post-consensus; cite Geiger AND the originals. | 2.0M | OSF, no license — cite only |
| `gligoric2025` | Gligorić et al. 2025: trust in 35 scientist occupations (7-pt) × ideology, US N=7,800, + 5 randomized trust-raising messages that all failed (conservatives-only randomization). | 8.3M | OSF, no license — cite only |
| `goldwert2026` | Climate Advocacy Megastudy (Goldwert et al. 2026): 31,324 × 113, 18 arms, 0–100 slider DVs + real petition/newsletter/donation outcomes, `belief_1`/`policy_1` confirmed 0–100 (~24% missing). No trust items; video/writing interventions — ranking, not magnitudes. | 25M | OSF, no license — cite only |
| `gss` | General Social Survey 1972–2024 cumulative file, release 7224 R3a, with codebook. | 0.6G | NORC, public |
| `hackenburg2025` | Hackenburg et al. 2025 (PNAS) LLM-persuasion scaling: 25,982 US Prolific respondents, **730 verbatim message arms** (720 LLM-generated across 24 models + 10 human-written) on 10 policy issues, 0–100 slider DVs, party + ideology. LLM-authored stimuli: use for arm-count power and model/prompt selection, not human-message realism. | 71M | GitHub, MIT |
| `hewitt2026` | Hewitt et al. 2026 (Nature) Archive 1: raw responses from 70 TESS/Coppock probability-sample survey experiments (71 in file), 134 outcomes, 482 arm contrasts, ~121k participants, original scales (mostly 1–7/1–5) + gender/race/age/educ/party/ideology. No climate/trust outcome; LLM outputs and the 15-megastudy secondary archive deleted (red-line check passed). Train/calibration only (memorised). RDS needs R. | 1.1M | Code Ocean capsule 9843791 v1.0 via git clone, data CC0 1.0 / code MIT |
| `kerwer2025` | Kerwer et al. 2025 (ZfP): 18-arm between-subject text RCT (plain-language summary vs abstract × #effects × COI / publication-bias / relevance statements), German quota N=2,451 (2,256 completers), **14-item METI trust** (1–7) + credibility (1–8), two summaries per person; arm means span 0.4 — near-null dispersion prior. Coarse gender/age/education decodable from the quota cell. | 2.3M | PsychArchives, CC BY-SA 4.0 — share-alike, keep separate |
| `kim2024` | Kim & Liu 2024 (Dataverse): 3-arm US text-message experiment (control/consensus/causal, n=3,007 MTurk) with **trust-in-climate-scientists measured pre AND post** (4-pt, q11/q40) + GND/Paris/federal policy + 7-pt party. Treated arms +0.08 trust vs +0.02 control — the first US message→trust ATE anchor. Verbatim stimuli NOT in deposit (paper appendix only). | 2M | Harvard Dataverse, CC0 |
| `koetke2024` | Koetke et al. 2024 (NHB) intellectual-humility experiments: 5 US studies, N=2,034, randomized vignette/strategy arms (Study 5: 4 arms incl. two "limits" framings) → **METI trust-in-scientists** (14 bipolar items: competence/integrity/benevolence), party + ideology in every study. First vendored randomized trust-outcome source; Study 5 shows a trust-vs-belief dissociation. | 6.6M | OSF, no license — cite only |
| `orchinik2024` | Orchinik et al. 2024 consensus messaging: quota-matched US samples with native 0–100 belief sliders — measured heaping: 42.5% on multiples of 5, 15.5% at endpoints. Use the Bovitz sample (n=2,545) only for slider shape. Also the only open randomized message experiment with a continuous (0–100) climate-scientist-perception outcome (3 arms: control / history-of-science / institutions-of-science) — in-family evidence for trust-τ (OPEN 38). NB: the "Rode, Clarke & van der Linden 2024" sweep lead (PMC11554758, OSF jynqh) is this same dataset under a wrong author attribution — do not re-vendor. | 4.6M | OSF, no license — cite only |
| `pew_atp` | Pew American Trends Panel waves 42 ("Trust in Science", 2019, incl. multi-item environmental-scientist battery), 100 (2021, Black/Hispanic oversamples), 114 (2022): 4-pt confidence in scientists **with party and race** — the race×trust / party×trust anchor. **Pew EULA: no redistribution** — reproduce via `fetch.sh` (pinned URLs+sha256). | 11M | TheARDA/OSF mirror, open |
| `sce` | FRBNY Survey of Consumer Expectations public microdata 2013–2025 (~186k rows): 0–100 percent-chance items with demographics for the heaping model (75% on multiples of 5, 17% at 50; heaping falls with education). No climate content — pure response-format asset. | 195M | FRBNY, open w/ attribution |
| `schmidbetsch2019` | Schmid & Betsch 2019 (NHB) + Schmid & Werner 2023 rebuttal experiments: 10 experiments, shared 4–6 arm designs (advocate absent / technique / topic / combination; hostility variants), pre/post attitudes + **12-item advocate-credibility semantic differential** (competence/character/sociability). English Exps 4 & 6 (n=345/1,137, political ideology incl. conservatives); fictitious-disease vaccination + climate topics. | 54M | OSF, CC BY 4.0 (2019) / no license (2023) — cite only |
| `spampatti2023` | Spampatti et al. 2023 climate-disinformation inoculation: 8 arms (2 controls + 6 verbatim text strategies, in the QSF), 0–100 affect slider (baseline + 20 post-statement measures), US raw n=834 (~100/arm). No US party ID (1–10 left–right only). | 23M | OSF, CC BY 4.0 |
| `tappin2023` | Tappin, Berinsky & Rand 2023 persuasion experiment: 5,071 US partisans / 25,181 obs, 48 human-written ~150-word message arms (24 issues × in-favor/against, verbatim texts in the SI), 7-pt agreement outcome, crossed with party-leader cues (use no-cue cells as clean arms). | 350M | OSF, CC BY 4.0 |
| `tisp` | TISP Many Labs (Cologna et al. 2025): 69,534 respondents, 68 countries (US n=2,559), **the exact 12-item four-dimension trust-in-scientists scale the target study uses**, with weights. | 0.2G | OSF, CC BY 4.0 |
| `vlasceanu2024` | Global climate intervention tournament (Vlasceanu et al. 2024): 59,440 respondents, 63 countries (US n=8,253), 11 interventions + control, belief/policy/sharing/WEPT outcomes; paper's analysis file + full ICPC item-level microdata + codebook. | 73M | Zenodo CC BY 4.0 / OSF CC0 |
| `wellcome` | Wellcome Global Monitor 2018 + 2020 (Gallup World Poll, US RDD phone, 15+; n=1,006 / 1,001): 4-pt trust in scientists/science, competence, benevolence, **2018 funding-transparency item Q14B**; age/gender/education/income quintile, weights; no party, no race. Raw world files via `fetch.sh`, US csvs via `extract_us.py`. | 60M | Wellcome CMS, CC BY 4.0 (site-wide terms, assumed) |
| `voelkel2024` | Strengthening Democracy Challenge megastudy (Voelkel et al. 2024): 35,252 rows, 25 interventions + 2 controls, democratic-attitudes outcomes; anonymized + recoded data, questionnaire. | 36M | OSF, no explicit license — research-use, cite only (see its README) |
| `voelkel2026` | Climate-messages megastudy (Voelkel, Ashokkumar et al. 2026): 13,821 rows, 13 arms (10 short messages + 3 placebo controls), **all outcomes 0–100 sliders**, all six scored moderators — the target study's closest design twin. No trust outcomes; pre/post design (use control-arm PRE for baselines). | 22M | OSF, no license — cite only |

## Why these

The benchmark's registration form (item D.1) names **GSS / ANES / Census** as
example sources of demographic profiles. ACS *is* the Census microdata product;
GSS additionally carries long-running items adjacent to the benchmark's outcomes
(confidence in the scientific community, environmental spending, institutional
trust).

The rest map onto the playbook's three data assets (`docs/playbook.html` §6.1):

- **D1 profile pool** — ACS for census structure; **CES** adds party ID ×
  education × income at large n (ACS carries no party).
- **D2 baseline corpus** — **TISP** (the target study's own trust scale),
  **CCAM** (U.S. climate-attitude time series), GSS.
- **D3 effect-proxy corpus** — **Vlasceanu 2024** and **Voelkel 2024**, the two
  open multi-intervention experiments closest in design to the target study:
  run them through our own pipeline to measure how much to trust our
  effect-level predictions. Extended by the 2026-08-15 scouting sweep
  (`docs/dataset-scouting.md`): **voelkel2026** (the design twin),
  **goldwert2026** (real advocacy-behavior outcomes), **bbprime2025**
  (sharing outcomes), and **gligoric2025** (the trust-ATE null prior).
- **Scale bridging / response format** (from the same sweep) —
  **gatewaybelief** (within-person Likert↔slider joint distribution),
  **orchinik2024** (slider endpoint/heaping shape in a quota panel), and
  **sce** (large-n 0–100 heaping model with demographic gradients).

## Not vendored

- **ANES** — vendored 2026-08-24 (`anes/`, 2020 + 2024 Time Series; downloads no
  longer require a login, see its `fetch.sh`).
- **Pew** (direct) — pewresearch.org needs a registered account, but the ATP waves we
  use are openly mirrored by TheARDA/OSF; see `pew_atp/`.
- **Gallup** — proprietary; topline numbers only via publications.
