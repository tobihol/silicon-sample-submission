# Koetke, Schumann, Porter & Yeomans 2024 — Seeing scientists as intellectually humble and trust in scientists and their research

## Version

OSF project "The effect of seeing scientists as intellectually humble on
trust in scientists and their research" (https://osf.io/d3xua/), osfstorage
contents as of 2026-08-17 (project last modified on OSF 2024-12-06).
Downloaded 2026-08-17 via the OSF API (no account required). The five
per-study `StudyXJASP_OSF.jasp` files (17–54 MB JASP workbooks duplicating
the R analyses) were skipped; everything else was mirrored. Preregistrations
are also linked as OSF registrations (nwbc2, 26fjk, m4xzv, yjdf2, mb5sx) —
the PDFs under `downloads/` are the same documents.

Paper citation: Koetke, J., Schumann, K., Porter, T., & Yeomans, M. (2024).
The effect of seeing scientists as intellectually humble on trust in
scientists and their research. Nature Human Behaviour, 9, 331–344.
https://doi.org/10.1038/s41562-024-02060-x (published online 2024-11-18).

License: none specified on the OSF project (`node_license` is empty and no
license relationship is attached) — no license; cite only, never re-host.
Publicly posted for a published paper; kept here privately for research use
only, not redistributed.

## Contents

All from OSF osfstorage, mirrored under `downloads/` with the project's
folder structure. Each `Study X/` folder holds `StudyXCleanData.csv`,
`IHS Study X Code for OSF.R` (the de-facto codebook: recodes, reverse
coding, composite construction), a preregistration PDF, and the Qualtrics
survey exported to .docx (verbatim items; in Studies 2–4 the vignette
stimuli are embedded screenshots of mock news articles inside the .docx,
not text — Study 5's stimuli are plain text).

- `downloads/Study 1/Study1CleanData.csv` — 298 × 118. Correlational
  (Prolific; no manipulation). Perceived intellectual humility of
  scientists in general (22 items) and METI trust toward "an average
  scientist", plus attitudes on climate change, vaccination, and GM foods,
  conspiracy mentality, science knowledge, CRT, and participants' own IH.
- `downloads/Study 2/Study2CleanData.csv` — 317 × 93. Randomized vignette:
  `Condition` = High IH (n=115) / Low IH (n=103) / Neutral (n=99). Mock
  Michigan News article about "Dr. Susan Moore" developing an anti-viral
  for long COVID; High/Low versions vary colleague and student quotes about
  her intellectual (im)humility. Outcomes: METI, support for the anti-viral
  research (5 items), vaccination attitudes; plus Big-5 and likability
  ratings of the scientist.
- `downloads/Study 3/Study3CleanData.csv` — 369 × 74. 3 (`IHCondition`:
  High IH 146 / Low IH 113 / Neutral 110) × 2 (`GenderCondition`: female
  184 / male 185 scientist) between subjects. Topic: Dr. Wilson's research
  on talking with opposing-party members. Outcomes: METI, Support for
  Research (5 items), recommendation-following behavioral intention
  (2 items: interest in receiving information / learning more about the
  suggestions), stereotype-content competence/warmth.
- `downloads/Study 4/Study4CleanData.csv` — 371 × 73. 2 (`IHCondition`:
  High 198 / Low 173) × 3 (`RaceCondition`: White 133 / Black 116 /
  Latinx 122 scientist) between subjects. Topic: plant-rich diets and
  climate change. Outcomes: METI, SupportforResearch (4 items), and
  information-seeking behavior: `Switch` (1=yes/2=no to receiving
  plant-rich-diet information after the survey) plus `Days` (meat days per
  week) and stereotype content.
- `downloads/Study 5/Study5CleanData.csv` — 679 × 87. CloudResearch
  Connect. Four randomized IH-communication strategies as separate arms
  (`IHCondition`): Control (164), Personal Humility (163), Limits of
  Methods (174), Limits of Results (178) — verbatim interview excerpts from
  "Dr. Sandra Wilson" about a social-media-break experiment; arms differ
  only in the final answer (crediting evolving thinking and her team vs.
  flagging methodological limits vs. flagging discrepant results and limits
  on generalizability). Outcomes: METI, Belief in Research (4 items,
  2 reverse-coded), `Behavior Follow` (1=yes/2=no/3=unsure, interest in
  social-media-break tips), stereotype content, and `S1_1..S6_3` — six
  candidate humility expressions each rated on conveying IH / increasing
  trust in the scientist / increasing trust in her results.

Key variables shared across studies (verified against the data, surveys,
and R code):

- Trust: METI (Muenster Epistemic Trustworthiness Inventory), 14 bipolar
  7-point semantic differentials rating the (average) scientist.
  Competence/expertise (METI_1–6): competent–incompetent (reverse-scored in
  the R code; all other items run negative→positive),
  unintelligent–intelligent, poorly educated–well educated,
  unprofessional–professional, inexperienced–experienced,
  unqualified–qualified. Integrity (METI_7–10): insincere–sincere,
  dishonest–honest, unjust–just, unfair–fair. Benevolence (METI_11–14):
  immoral–moral, unethical–ethical, irresponsible–responsible,
  inconsiderate–considerate. Scored as `METI_AVG` (14-item mean) and as the
  three subscale means.
- Perceived IH of the scientist: 22-item state-IH scale (`IH_1..IH_22`,
  1–5) — the manipulation check and Study 1's key predictor.
- Politics: `PO Bin` party ID (1 Democrat / 2 Republican / 3
  Other-third-party), `PO_1`/`PO_2` economic and social ideology (7-point,
  strong liberal → strong conservative), political conviction and
  moralization items. Present in all five studies.
- Demographics: `Race`, `Age`, `Gender`, `Edu`, `Religion`, `Religiosity`
  in all studies (Studies 1–4 also `Transgender`).

Total N = 2,034 across the five clean data files (298+317+369+371+679).

## Why it is here

The repo's first vendored randomized-experiment source where
message/vignette arms move a trust-in-scientists scale that structurally
matches the competence/integrity/benevolence core of the target study's
4-dimension trust battery (the METI has no separate openness subscale,
though the 22-item perceived-IH measure is openness-adjacent). Closes
practice finding 33's trust-cell gap: all 1,489 scored practice cells are
non-trust. Study 5 is especially valuable for its heterogeneous,
partly backfiring ATEs: relative to control, both "Limits" arms modestly
raise METI trust in the scientist (6.05 → 6.15/6.28 raw means) while
lowering belief in her research (5.39 → 5.02/4.89), whereas Personal
Humility raises trust without that cost — a dissociation between trust in
the person and trust in the findings that any credible simulation should
reproduce. Studies 2–4 add clean 2–3-arm vignette ATEs on the same scale
with party/ideology covariates for subgroup checks, and Study 1 provides a
correlational anchor for trust in scientists in general.
