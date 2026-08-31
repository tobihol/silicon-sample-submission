# Kim & Liu 2024 — Persuading climate skeptics: causal evidence vs. consensus messaging

## Version

Harvard Dataverse "Replication Data for: Persuading Climate Skeptics with
Facts: Effects of Causal Evidence vs. Consensus Messaging"
(doi:10.7910/DVN/ABEHSN), dataset version 1.0, published 2024-02-12.
Downloaded 2026-08-19 via the Dataverse API
(https://dataverse.harvard.edu/api/access/datafile/{id}; no account
required). All file md5 checksums verified against the Dataverse file
metadata.

Authors: Jin Woo Kim (Kookmin University) & Ruijun Liu (University of
Pennsylvania). The survey was fielded by the University of Pennsylvania
(per the consent text in the instrument).

License: CC0 1.0 (declared on the Dataverse record).

## Contents

All files of the deposit, mirrored flat under `downloads/`:

- `downloads/s.sav` (id 8220856) — experiment microdata as exported from
  Qualtrics, 3,007 rows × 107 columns, with variable and value labels.
- `downloads/RP Replication.R` (id 8220853) — the authors' R script that
  reproduces all results in the paper and appendices; serves as the
  de-facto codebook (condition derivation, recodes, index construction).
- `downloads/PR.Rmd` (id 8220852) — RMarkdown version of the same script.
- `downloads/PR.html` (id 8220857) — knit log of the Rmd (code + console
  output + plots).
- `downloads/README.rtf` / `downloads/README.pdf` (ids 8220854, 8220855) —
  the deposit's two-paragraph file manifest (no codebook content).

Key variables (verified against `s.sav` and the R script):

- Design: US MTurk sample (`workerId`/`hitId`/`assignmentId` present),
  three-arm between-subjects randomization. Arm is not a single column; it
  is derived from Qualtrics block-randomizer indicators
  `FL_{117,119,134,139,144,149,129,124}_DO_{control,consensus,causal}`
  (a respondent's arm is the one whose indicator is 1 in any of the eight
  blocks), exactly as in `RP Replication.R` lines 29–33. Verified counts:
  control n = 1,008; consensus n = 994; causal n = 1,005 (total 3,007;
  arms are mutually exclusive and exhaustive).
- Treatments: static persuasive text messages — a "97% consensus" message
  vs. a longer causal-mechanism explanation of why scientists concluded
  humans cause climate change, vs. a control text (about cryptocurrency,
  per the manipulation check). **The verbatim message texts are NOT in the
  deposit**: they appear nowhere in the .sav labels, the R/Rmd scripts,
  the HTML log, or the two READMEs. The closest in-deposit description is
  the manipulation-check item `q48` and its value labels ("It explained
  that there is a 97% consensus among climate scientists" / "It explained
  why scientists have concluded that human activities are causing climate
  change" / "It discussed cryptocurrency."). Full stimuli would have to
  come from the paper's appendix.
- Trust in climate scientists, measured PRE (`q11`, pre-treatment) and
  POST (`q40`, post-treatment): "How much, if at all, do you trust climate
  scientists to give full and accurate information about global climate
  change?", single item, 4-point (1 = A lot … 4 = Not at all / None at
  all). n non-missing 3,006 each; pre–post r ≈ 0.90.
- Climate belief: `q7` (pre) / `q31` (post) attribution of warming (human
  vs. natural, 3-point) plus follow-ups `q8/q9/q32/q33`, `q36–q39`
  (contribution/evidence ratings), and `q41_7` perceived scientific
  consensus (0–100 slider).
- Policy support (all post): `q42` federal government should do more
  (5-point), `q43` Green New Deal support (7-point; raw Qualtrics codes
  6–12, not 1–7), `q44` Biden recommitting to the Paris Agreement
  (7-point; raw codes 4–10), `q45` priority for Biden/Congress (4-point).
- Party ID: `q5`, 7-point from Strong Republican (1) to Strong Democrat
  (7); n = 3,004 (1,520 Republicans/leaners at 1–3).
- Also: Biden/Trump approval (`q3`/`q4`), political interest (`q6`),
  demographics (`q12` gender, `q13` age, `q14` education, `q15/q16`
  religion), 6-item CRT (`q17–q22`), news-source choice (`q24_*`), and
  manipulation checks `q46–q48`.

## Why it is here

The only open US dataset found (2026-08-19 workflow sweep) where
randomized *static text messages* move a trust-in-climate-scientists item
measured both PRE and POST treatment, with party ID on file — the closest
effect-proxy to the target's treatment class. Directionally, treated arms
gain ~0.08 on the reverse-coded 4-point trust item pre-to-post vs. ~0.02
in control. Caveats: MTurk convenience sample (not probability-based);
trust is a single 4-point item, not a slider, so scale bridging to the
target instrument is coarse; no race or income variables, so those
moderators cannot be checked here.
