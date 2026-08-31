# Gateway (mis)Belief Model — pooled study data

## Version

OSF project "The Gateway (mis)Belief Model", https://osf.io/ewjgt/ (osfstorage,
single component, no separate releases). Downloaded 2026-08-15 via the OSF API;
local filenames match the OSF filenames exactly.

The project pools data from three studies:

- van der Linden, Sander; Leiserowitz, Anthony; Rosenthal, Seth; and Maibach,
  Edward. "Inoculating the Public against Misinformation about Climate Change."
  Global Challenges 1, no. 2 (2017): 1600008. ("Experiment 2" here.)
- Maertens, Rakoen; Anseel, Frederik; and van der Linden, Sander. "Combatting
  Climate Change Misinformation: Evidence for Longevity of Inoculation and
  Consensus Messaging Effects." Journal of Environmental Psychology 70 (2020):
  101455. ("Experiment 1" here.)
- Logemann, Hyunji; Rode, Jacob; Maertens, Rakoen; and van der Linden, Sander.
  "The Gateway (mis)Belief Model: How Misinformation Impacts Perceptions of
  Scientific Consensus and Attitudes towards Climate Change." British Journal
  of Psychology (2025), doi:10.1111/bjop.70022. (Pooled/internal meta-analysis
  paper; "Supplemental study" here.)

License: none stated on the OSF project (the node has no license field set and
no LICENSE/README file). Publicly shared research data; keep vendored for
internal analysis only, do not redistribute.

## Contents

- `downloads/Experiment 1 data Maertens et al 2020.csv` — 479 × 58; three-arm-
  plus-control between-subjects experiment (`Condition`: Control / Consensus /
  Inoculation / Balanced; `Consensus` dummy = 1 for all message arms), climate
  outcomes at T1 (pre), T2 (post-message), T3 (post-misinfo follow-up)
- `downloads/Experiment 2 data van der Linden et al 2017.csv` — 2,197 × 33;
  Qualtrics export, condition in `FL_32_DO` (Control, CounterOnly,
  PieChartOnly, Pie-Counter, Pie+Inoc-Counter, Pie+Indepthinoc-Counter; "Pie" =
  97 %-consensus pie-chart message), outcomes pre (Q3–Q11) and post (Q31–Q47)
- `downloads/Supplemental study data Maertens et al 2025.csv` — 1,825 × 384;
  longitudinal inoculation study, `Group` (Control / Inoc / InocInoc) ×
  `Measurement` (T1/T2/T3 delay), outcomes at `.Pre` and `.T1/.T2/.T3`
- `downloads/Experiment 1 analysis.R`, `Experiment 2 analysis.R`,
  `Supplemental Study analysis.R`, `Internal meta analysis GmBM.R`,
  `Figures 6 and 7.R` — the authors' analysis scripts; the project has no
  codebook, so these are the only variable documentation (Experiment 2
  analysis.R maps the Q-numbered columns: Q8_1/Q36_1 = perceived scientific
  consensus, Q10_1/Q38_1 = worry, Q11_1/Q39_1 = support for action, and gives
  the belief/human-causation recodes and demographic codings)

## Why it is here

The only open source we have with an empirical within-person joint distribution
of 0–100 slider responses and 1–7 Likert responses on climate constructs — the
Likert→slider bridge the pipeline otherwise has to assume. In all three
datasets the same respondents answer perceived scientific consensus as a 0–100
slider (verified range 0–100, ~60–100 distinct values) and belief in climate
change, human causation, worry, and support for action on 1–7 scales (integer
Likert in Experiments 1–2; continuous 1–7 sliders in the supplemental study;
Experiment 2's belief and human-causation items are 5-point recodes instead),
both before and after a randomized consensus/inoculation message (e.g. pre-PSC
× pre-worry r ≈ 0.47 on N = 2,173 in Experiment 2). Because the message
manipulation is randomized (`Condition` / `FL_32_DO` / `Group`), the data
double as an effect-size proxy for a scientific-consensus-message arm.
