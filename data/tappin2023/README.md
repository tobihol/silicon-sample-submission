# Tappin, Berinsky & Rand 2023 — Partisans' receptivity to persuasive messaging is undiminished by countervailing party leader cues

## Version

OSF parent project "Partisans' Receptivity to Persuasive Messaging is
Undiminished by Countervailing Party Leader Cues" (https://osf.io/v3s72/),
license CC-BY Attribution 4.0 International (verified on the node via the OSF
API). Four child components, all downloaded 2026-08-17 via the OSF API (no
account required):

- Data and code (https://osf.io/czwmp/): `replication_materials.zip`, 173 MB,
  https://osf.io/download/tfx2v/ — MD5 verified against OSF
  (`bff16373e9a3567127b3abad70e7363b`)
- Survey instrument (https://osf.io/w9fcd/): `survey_instrument.pdf`,
  https://osf.io/download/qh9wx/
- Supplementary information (https://osf.io/yqfm2/):
  `supplementary_information.pdf`, https://osf.io/download/uqdtw/
- Pre-analysis plan (https://osf.io/vdb7j/): `PAP_cues_info_2021-09-01.pdf`,
  https://osf.io/download/hpdct/

Paper citation: Tappin, B. M., Berinsky, A. J., & Rand, D. G. (2023).
Partisans' receptivity to persuasive messaging is undiminished by
countervailing party leader cues. Nature Human Behaviour, 7, 568–582.
https://doi.org/10.1038/s41562-023-01551-7

Design: Lucid, September 2021, quota-matched US adult partisans (incl.
leaners). Each respondent judged 5 of 24 US policy issues (7-point agreement).
Per issue, a 2×2 within-subject randomization crossed a persuasive message
(`info`) with a party-leader cue (`cue`); cue style (`cue_type`, one- vs
two-sided) was between-subjects. 48 unique ~150-word messages (2 per issue,
one in favor / one against); each respondent was always shown the message
countervailing their own party leader's position.

License: CC-BY 4.0 (whole OSF project).

## Contents

Raw files under `downloads/`; the zip is unzipped in place to
`downloads/replication_materials/`:

- `downloads/replication_materials/data/data_RM.rds` — the participant-level
  data, 126,264 rows × 46 columns: long format, 5,261 respondents × all 24
  issues, with `item_seen` flagging the 5 issues each respondent actually saw
  (25,284 seen rows; 25,181 non-missing outcomes from 5,071 completes —
  matches the paper's reported numbers exactly)
- `downloads/replication_materials/data/codebook.xlsx` — codebook for all 46
  variables
- `downloads/replication_materials/*.R`, `model_fitting/`, `fits/`,
  `appendix/`, `figures/` — the authors' full brms/Stan replication pipeline
  including pre-fitted models
- `downloads/survey_instrument.pdf` — Qualtrics export; documents the
  loop-and-merge display logic (Democrats are shown the message/cue field for
  Biden, Republicans the one for Trump)
- `downloads/supplementary_information.pdf` — Supplementary Table 1 (§1.2,
  from p. 4) contains all 48 verbatim persuasive messages ("Message Treatment
  In Favor" / "Message Treatment Against" per issue) plus both leaders'
  positions per issue. The verbatim message texts appear ONLY here, not in the
  replication zip.
- `downloads/PAP_cues_info_2021-09-01.pdf` — pre-analysis plan (2021-09-01)

Key variables (verified against the data and codebook):

- Outcome: `likertAgree`, 1–7 (1 = strongly disagree … 7 = strongly agree)
  with the policy; `likertAgree_recoded` re-signs it toward the in-party
  leader's position.
- Issue/message identifiers: `item` (1–24), `item_label`, `item_text`. There
  is NO explicit 48-level message ID: which of the two messages a respondent
  saw is deterministic — the one arguing against their in-party leader's
  stance — and is recovered as `item` × direction, where direction = opposite
  of `biden` (for Democrats) or `trump` (for Republicans) (`agrees`/
  `disagrees`; the two leaders oppose each other on all 24 issues). This
  yields exactly 48 arms.
- Treatment: `info` (message shown 0/1), `cue` (leader cue shown 0/1),
  `condition` (Control / Cue-only / Info-only / Both), `cue_type` (one_sided /
  two_sided, between-subjects).
- Party & covariates: `party7` (6 levels, partisans incl. leaners; no pure
  independents in sample), `republican`, `strong_partisan`, `party_strength`,
  `age_survey`, `female`/`gender_survey`, `education_survey`/`ba_degree`,
  `PK_sum` (political knowledge 0–4), `vote_party`, `ideo7`.

Per-arm cell sizes over the 48 derived arms (non-missing outcomes):
Info-only (message, no cue) 6,233 obs, n per arm 94–171 (median 128);
Control (no message, no cue) 6,444 obs, matched cells 92–167.

## Why it is here

48 real, human-written ~150-word persuasive-message arms with verbatim texts
(SI Table 1), each with a per-arm 7-point Likert outcome and a party
moderator, under a clean CC-BY 4.0 license — this is the harness's requested
~30+-arm practice task for shrinking arm-clustered CIs (REPORT §7): enough
arms to estimate the between-arm variance component that dominates our CI
width, an order of magnitude more than the 11–25-arm tournaments already in
D3. One handling requirement: the cue-condition crossing must be dealt with —
only the no-cue cells (`condition == "Info-only"` vs `"Control"`) are the
clean message arms; the `Both` and `Cue-only` cells confound the message
effect with party-leader cues (that interaction is the paper's own research
question, and a usable secondary check).
