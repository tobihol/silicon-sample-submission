# Geiger et al. 2026 — Beyond memory and experimenter demand (consensus-message reanalysis deposit)

## Version

OSF project "Beyond Memory and Experimenter Demand: Scientific Consensus
Messages Correct Misperceptions" (https://osf.io/s8zgh/), full osfstorage
contents (5 files) as of 2026-08-19 (project last modified on OSF
2026-04-22). Downloaded 2026-08-19 via the OSF API (no account required).

Paper citation: Geiger, S. J., Većkalov, B., Bartoš, F., Ruggeri, K., &
van der Linden, S. (2026). Beyond memory and experimenter demand:
Scientific consensus messages correct misperceptions. Journal of
Environmental Psychology. https://doi.org/10.1016/j.jenvp.2026.103038

This is a **reanalysis deposit, not the original data releases** — it
re-releases two earlier experiments' microdata. Always cite the original
authors alongside Geiger et al.:

- CSV: van der Linden, S., Leiserowitz, A., & Maibach, E. (2019). The
  gateway belief model: A large-scale replication. Journal of
  Environmental Psychology, 62, 49–58.
  https://doi.org/10.1016/j.jenvp.2019.01.009
- RDS: Većkalov, B., Geiger, S. J., Bartoš, F., et al. (2024). A
  27-country test of communicating the scientific consensus on climate
  change. Nature Human Behaviour.
  https://doi.org/10.1038/s41562-024-01928-2

License: none specified on the OSF project (no license attached) — cite
only, never re-host. Kept here privately for research use only, not
redistributed.

## Contents

All five osfstorage files, flat under `downloads/`:

- `downloads/data - van der Linden.csv` (osf.io/download/7wt3x) — the van
  der Linden et al. 2019 US consensus-message RCT, **6,301 rows × 69
  columns**, all `complete == 1`. Verified structure:
  - Two arms: `group` control (n = 3,151) vs treatment (n = 3,150);
    `condition` is the same split coded 0/1. `new_cond` further splits the
    treatment arm by whether post consensus is exactly 97 (`treat_97`,
    n = 1,273 — 40% of the treated!) vs not (`treat_NO97`, n = 1,877) —
    the memory/demand artifact the reply paper is about.
  - Pre/post outcomes, no missings: `belief_pre/post`, `worry_pre/post`,
    `policy_pre/post` (all 1–7 composites with decimals) and
    `consensus_pre/post` (0–100). `diff_*` columns are post − pre.
  - Party: `party3` with 1 = Republican (1,491), 2 = Independent (1,626),
    3 = Democrat (2,076), NA (1,108) — coding recovered from `reply.R`
    lines 437–441; also `ideology` (values 1/3/4) and raw `q*` items.
- `downloads/analysis_dataset.RDS` (osf.io/download/y46hw; read with
  `pyreadr`, single unnamed data frame) — the Većkalov et al. 2024
  27-country experiment, **10,527 rows × 23 columns**, 27 `country_id`
  values. Verified structure:
  - Three arms: `condition` control (3,512) / classic (3,488) / updated
    (3,527) consensus messages.
  - **USA cells: n = 362 — control 125 / classic 119 / updated 118.**
  - `scientist_trust`: 1–7, no missings (US mean 5.88) — trust in climate
    scientists under message randomization.
  - Also `consensus_perception(.pre)` 0–100, `belief_climate_change` /
    `belief_human_causation` / `belief_crisis` (1–7), `climate_worry`,
    `climate_action_support`, `political_orientation` (0–10), age, gender
    (0/1/2), education, `paid` (True for only 322 rows), `pretest`
    order flag.
- `downloads/reply.R` (osf.io/download/z9k5t) — the authors' full
  reanalysis script; the de-facto codebook for both files (effect-size
  functions, arm definitions, party recodes, figure code).
- `downloads/functions.R` and `downloads/functions-nonhierarchical.R`
  (osf.io/download/6bfnt and the fifth osfstorage file) — model helper
  functions used by `reply.R`.

## Why it is here

The vdL 2019 file is the **largest single US consensus-message RCT in our
set** — n = 6,301 with ~3,150 per arm dwarfs the per-arm precision of the
vendored `gatewaybelief` pool, with pre/post belief, worry, and policy
support plus party splits, so it anchors consensus-message ATE priors and
party-moderated effects. The RDS adds a second randomized **trust-in-
climate-scientists (1–7)** outcome column under 3-arm message
randomization (US cells ~120/arm) — in-family evidence for trust-τ
alongside `orchinik2024` and the `gligoric2025` null. Caveats: this is a
reanalysis deposit — cite Geiger et al. AND the original authors; and 40%
of vdL-treated respondents report exactly 97 post-consensus (message
parroting), so use `new_cond` / the reply's robustness splits before
taking consensus ATEs at face value.
