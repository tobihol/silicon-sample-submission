# Schmid & Betsch 2019 (+ Schmid & Werner 2023) — Rebutting science denialism: advocate credibility in public discussions

## Version

Two OSF projects by the same lab, downloaded 2026-08-17 via the OSF API
(no account required), mirrored under `downloads/<node-id>/` with each
project's folder structure:

1. OSF project "Effective strategies for rebutting science denialism in
   public discussions" (https://osf.io/xx2kt/), last modified on OSF
   2019-06-25. Paper: Schmid, P., & Betsch, C. (2019). Effective
   strategies for rebutting science denialism in public discussions.
   Nature Human Behaviour, 3, 931–939.
   https://doi.org/10.1038/s41562-019-0632-4
   License: CC-BY Attribution 4.0 International (set on the OSF node).

2. OSF project "DATA: Hostility has a trivial effect on persuasiveness
   of rebutting science denialism on social media"
   (https://osf.io/hg2y8/), last modified on OSF 2023-12-05. Paper:
   Schmid, P., & Werner, B. (2023). Hostility has a trivial effect on
   persuasiveness of rebutting science denialism on social media.
   Communications Psychology, 1, 39.
   https://doi.org/10.1038/s44271-023-00041-w
   License: no license — cite only, never re-host.

Subset vendored: all experiment data files (.sav), stimuli (English and
German), AsPredicted preregistrations, the hg2y8 merged analysis dataset
and analysis script, and the messages PDF. Skipped: SPSS mediation
outputs, RevMan internal-meta-analysis files, per-figure xlsx exports,
forest-plot PDFs.

## Contents

### `downloads/xx2kt/` — Schmid & Betsch 2019 (NHB), Experiments 1–6

Per experiment: `Experiment N/Data/Experiment N.sav` (microdata),
`Experiment N/Stimuli GER|ENG/` (the discussion stimuli: mp3 audio in
Exp 1, screenshot images elsewhere), and
`AsPredicted_Experiment_N.pdf` where present (Exps 2–5 only; Exps 1 and
6 have no prereg file on the node).

All six experiments share the same 4 arms (SPSS value labels on
`Condition`, verified in every file): 1 = Advocate absent, 2 = Technique
rebuttal, 3 = Topic rebuttal, 4 = Combination.

| Exp | n (rows) | vars | Language | Topic |
|-----|----------|------|----------|-------|
| 1 | 125 | 106 | German | vaccination (audio stimuli) |
| 2 | 206 | 145 | German | vaccination |
| 3 | 261 | 123 | German | vaccination |
| 4 | 345 | 156 | **English** | vaccination |
| 5 | 217 | 247 | German | climate change |
| 6 | 1,137 | 126 | **English** | vaccination |

Row/var counts and arm labels verified by reading each .sav. Exp 4 is
balanced 69 per arm; Exp 6 has an oversampled Combination arm
(246/224/244/423). Exps 4 and 6 carry political-orientation variables
(`POMP_PoliticalLIBERALKONS` "political ideology",
`POMP_PoliticalREPUBDEMO` "political identity"); Exp 6 was recruited to
include political conservatives. The vaccination scenario uses a
fictitious disease ("dysomeria"), so attitudes are not contaminated by
prior real-vaccine beliefs.

Credibility DVs (verified present in Exps 4 and 6): 12-item
McCroskey-style source-credibility semantic differential for the science
advocate — `Competence_Image_Source_Scale_Pro1`–`6`,
`Character_Image_Source_Scale_Pro7`–`9`,
`Sociability_Image_Source_Scale_Pro10`–`12` — with composites
`POMP_COMPETENCE_MEAN_PRO`, `POMP_CHARACTER_MEAN_PRO`,
`POMP_SOCIABILITY_MEAN_PRO`. Denier equivalents exist pre and post
(`..._Denier1a`–`12a`, `..._Denier1b`–`12b`;
`POMP_COMPETENCE_MEAN_DEN` etc.). Primary DVs are pre/post attitude
(`POMP_PRE_ATT_MEAN`, `POMP_POST_ATT_MEAN`, `POMP_DIFF_ATT`) and
behavioral intentions (`POMP_PRE_INT`, `POMP_POST_INT`,
`POMP_DIFF_INT`).

### `downloads/hg2y8/` — Schmid & Werner 2023 (Communications Psychology), hostility follow-up

Four experiments, all-English stimuli (no country variable in the data),
vaccination against the same fictitious "dysomeria", discussions framed
as social-media threads. Per experiment: `Experiment N/Experiment N.sav`.
Plus `Merged dataset and RScript for primary analyses/
DATA_MERGE_ANALYSIS.sav` (all four experiments stacked, 3,226 rows × 61
vars, verified) and `AnalysisScript.R` (the authors' primary analyses;
de-facto codebook for factor codings), and `Additional Material/Messages
delivered by deniers and advocates for all conditions and experiments.pdf`
(full message texts — the node has no stimulus images or prereg files).

Verified counts and design (crosstab of `FACTOR_DENIER` ×
`FACTOR_ADVOCATE` in the merged file; codings from `AnalysisScript.R`:
denier 0 = hostile, 1 = neutral; advocate 0 = hostile, 1 = neutral,
2 = absent):

| Exp | n (rows) | vars | Arms | Design |
|-----|----------|------|------|--------|
| 1 | 521 | 43 | 4 | denier hostile/neutral × advocate hostile/neutral |
| 2 | 310 | 48 | 4 | denier hostile/neutral × advocate hostile/absent |
| 3 | 1,200 | 63 | 6 | denier hostile/neutral × advocate hostile/neutral/absent |
| 4 | 1,195 | 63 | 6 | denier hostile/neutral × advocate hostile/neutral/absent |

DVs include perceived competence of advocate and denier
(`POMP_COMPETENCE_ADVOCATE`, `POMP_COMPETENCE_DENIER`), plus pre/post
attitude and intention (`PRE_POMP_Attitude`, `POST_POMP_Attitude`,
`PRE_POMP_Intention`, `POST_POMP_Intention`). Caveat: unlike xx2kt's
12-item scale, competence here is a single bipolar item ("not at all
competent – very competent"; multi-rater variants like
`COMPETENCE_DENIER_1/_2` appear in Exps 3–4).

## Why it is here

Randomized rebuttal-message arms with a McCroskey-style
advocate-credibility outcome: the competence/character semantic
differentials for the science advocate are the nearest open analog to
the competence/integrity dimensions of trust in scientists, measured
under randomized message interventions. English samples exist (Exp 4,
and the large conservative-inclusive Exp 6, both with political ideology
and identity variables), and the hg2y8 follow-up adds four more
all-English experiments with an advocate-competence DV under
hostile-vs-neutral tone manipulations.

Caveat: the outcome is the speaker credibility of one debating advocate,
not generalized trust in scientists — use for bridging/priors on
credibility-shaped outcomes, not as a direct trust-in-scientists
measure. The German experiments (xx2kt Exps 1–3, 5) are included for
completeness but are flagged: German-language stimuli and samples, so
they need explicit justification before use in any English-sample
simulation.
