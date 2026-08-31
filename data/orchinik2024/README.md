# Orchinik et al. 2024 — Consensus Messaging and Perceptions of Climate Scientists

## Version

Full OSF materials for the project "Learning from and about scientists"
(~4.4 MB, all files). Downloaded 2026-08-15 via the OSF API from the
canonical project: https://osf.io/jynqh/

Citation: Orchinik, R., Dubey, R., Gershman, S. J., Powell, D., & Bhui, R.
(2024). Consensus messaging shapes perceptions of climate change and climate
scientists. PNAS Nexus. (OSF project title: "Learning from and about
scientists".)

No license is declared on the OSF project (node license: none). Treat as
all-rights-reserved: internal use only, do not redistribute, cite the paper
and the OSF project when used.

## Contents

- `downloads/data/final_clean.csv` — the cleaned **Bovitz** sample
  (3,478 rows × 68 cols; `drop == FALSE` gives the analysis sample of
  n = 2,545). One row per respondent.
- `downloads/data/final_bovitz_raw.csv` — raw Bovitz Qualtrics export.
- `downloads/data/lucid_sem_clean.csv` — cleaned **Lucid** supplementary
  sample (3,344 rows = 1,672 respondents × 2 within-subject orders).
- `downloads/data/lucid_sem_041224.csv` — raw Lucid export.
- `downloads/data/final_mturk_raw.csv`, `downloads/data/mturk_clean.csv` —
  MTurk pilot sample.
- `downloads/code/bovitz_data_clean.R`, `lucid_data_clean.R`,
  `mturk_data_clean.R` — cleaning scripts; these are the de facto codebook.
  `bovitz_data_clean.R` documents the variable renames and the endpoint
  recodes on the `*_adj` variables (0 → 0.497462, 100 → 99.50254, used to
  keep log-odds transforms finite).
- `downloads/code/analysis.Rmd`, `analysis_supplements.Rmd` — analysis code.
- `downloads/qualtrics/` — the full survey instruments (.qsf + .docx) for
  Bovitz, Lucid, and CloudResearch (MTurk); the .docx files document exact
  item wording and response scales.

Key variables in `final_clean.csv` (verified with pandas):

- **Belief sliders, raw 0–100**: `prior_cc_occur`, `prior_consensus_num`,
  `P_E_yes_given_cc_unbiased`, `P_E_no_given_no_cc_unbiased`, and the
  within-subject conditional beliefs `P_cc_given_cons{50,75,90,97,99}` (plus
  parallel `P_pro/anti_bias_given_cons*` and `P_pro/anti_skill_given_cons*`).
- **Trust items, 4-point categories** (coded 1–4 = "None at all" …
  "A great deal of confidence"): `uni.science.trust`, `priv.science.trust`,
  `gov.trust`, `pol.party.trust`. Note: the derived `uni_sci_trust` /
  `priv_sci_trust` columns are all NA in the published file (the string
  recode in the R script does not match the numeric codes) — use the raw
  1–4 columns.
- **Party + demographics**: `party` (1 = Dem, 2 = Rep, 3/4 = Ind; also the
  labeled `Party`), `politics` (+ social/econ 7-pt ideology), `age`,
  `gender`, `race`, `edu`, `income`, `god`, affective-polarization
  thermometers. A few junk age entries (0.1, 1111) exist — sanity-filter.
- **Sample/quality flags**: `condition` (control/skill/trust), `fails`,
  `flag`, `drop`, `cons_attentive`.

The randomized message experiment in the Bovitz sample (verified 2026-08-17
against `final_clean.csv` and `Bovitz qualtrics.docx`):

- **Arms** (`condition`, between-subjects, shown after the prior elicitation
  and before the conditional-belief outcomes): as-randomized 1,038 control /
  1,037 skill / 1,036 trust (367 further rows have blank `condition` =
  pre-randomization dropouts); analysis sample (`drop == FALSE`, n = 2,545):
  **control 847, skill 837, trust 861**.
  - *skill* = a **history-of-science** passage ("… the study of climate
    change is actually a long-established science. The basic dynamics of
    carbon dioxide (C02) and atmospheric warming were first understood in
    1860 by physicist John Tyndall … CO2 has been measured directly at Mauna
    Loa Observatory since 1958. Famously, NASA scientist James Hansen
    testified to Congress in 1988 …").
  - *trust* = an **institutions-of-science** passage ("Scientists and
    universities take many steps to reduce systemic bias … Scientific
    journals require conflict of interest statements and … investigate the
    funding sources of scientists. Those who receive funding from vested
    interests are often sanctioned by their peers … over 95% of scientists
    think public access to their research is important.").
  - *control* = neutral transition text only.
- **Continuous post-treatment scientist-perception outcomes, all 0–100**
  (each asked at consensus levels 50/75/90/97/99 out of 100 scientists):
  perceived bias — "How likely do you think it is that a random climate
  scientist who expresses that human-caused climate change is occurring
  [/ is NOT occurring] is extremely biased?"
  (`P_pro/anti_bias_given_cons*`); perceived skill — "How likely do you
  think it is that a random and unbiased climate scientist who expresses
  that human-caused climate change is occurring [/ is NOT occurring] is
  capable, meaning they arrived at this conclusion due to skill?"
  (`P_pro/anti_skill_given_cons*`). Pre-treatment 0–100 baselines:
  `prior_sci_biased` ("In your view, what is the likelihood that a randomly
  selected climate scientist will be extremely biased? An extremely biased
  scientist will always express the same opinion about whether human-caused
  climate change is occurring irrespective of what the evidence shows.")
  and the perceived-accuracy items `P_E_yes_given_cc_unbiased` /
  `P_E_no_given_no_cc_unbiased`. The direct 5-point `belief_shift_*` items
  exist only in the two treatment arms (control is NA by design).
- **Moderators in the analysis sample**: `Party` Dem 936 / Rep 836 /
  Ind 773, plus 7-pt `politics(_social/_econ)` ideology and the
  demographics listed above.

Distinguishing the samples: they live in separate files, and the Lucid
conditional-belief sliders ran **−50…+50** in the raw data (shifted +50 to
0–100 in `lucid_sem_clean.csv`), whereas all Bovitz sliders ran natively
**0–100**. Lucid prior items were 0–100 in both.

## Why it is here

The cleanest open view of 0–100 slider endpoint bunching in a quota-matched
US opt-in sample (Bovitz, n = 2,545) with full moderators — party ID,
ideology, demographics, and four 4-point institutional-trust items — making
it a scale-bridging asset for mapping continuous slider responses onto
coarser scales and vice versa. Verified heaping on the raw 0–100 belief
items (9 items pooled, analysis sample, 22,905 responses): 1.8% at 0,
3.2% at 50, 13.7% at 100 (15.5% at either endpoint), 42.5% on multiples
of 5, 32.3% on multiples of 10. The top endpoint dominates: e.g.
`prior_cc_occur` has 22.6% of responses at exactly 100 (full-sample), and
`P_cc_given_cons99` 24.6%.

Caveats: use the **Bovitz sample only** for slider response shape (Lucid
used a different −50…+50 slider); the main DVs are within-subject
*conditional* beliefs (belief given a stated consensus level), not simple
attitude reports; and the trust items are 4-point categories, not sliders,
so they inform moderator structure rather than slider behavior.

Second role (added 2026-08-17, message-experiment sweep for the trust-τ
question, OPEN 38): this is the **only open randomized experiment the sweep
found with message arms and a continuous climate-scientist-perception
outcome** — control vs a history-of-science passage vs an
institutions-of-science passage, with 0–100 perceived-bias and
perceived-skill outcomes (see the experiment block above). That makes it
in-family evidence for the trust-τ question, but at 3 arms it yields only
2 treatment–control contrasts, so it can **narrow, not settle**, the τ
range. Sweep result recorded so nobody re-searches: the 2026-08-17 sweep
came up with a **clean negative for ≥4-arm open alternatives** (no open
randomized message experiment with ≥4 arms and a continuous
climate-scientist-perception outcome was found). Alias warning: the sweep
lead cited as "Rode, Clarke & van der Linden 2024, PNAS Nexus
(PMC11554758), OSF jynqh" resolves to **this** paper — PMC11554758 is
Orchinik, Dubey, Gershman, Powell & Bhui (2024); the author attribution in
the lead was wrong. Verified 2026-08-17 by re-downloading osf.io/jynqh in
full via the OSF API: all 17 files byte-identical (sha256) to `downloads/`
here. Do **not** vendor a separate `rode2024`.
