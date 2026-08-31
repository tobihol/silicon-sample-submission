You are building the harness for this idea. The frozen definitions are already in your
system prompt — the scoring tables and the blinding rules are binding and you do not need to
load them from anywhere. Read `AGENTS.md` for the layout.

## What exists

The frozen definitions, the benchmark materials, the training data — and nothing else. No
loop has been designed; you are designing it, on this harness's own facilities.

- `/workspace/benchmark` — the official submission template, read-only: the survey
  instrument (`survey/survey.json`, `survey/questionnaire.txt` with all 16 intervention
  texts), the variable dictionary (`codebook.csv`), the condition map
  (`survey/condition_codenames.csv`), the per-tier file formats (`predictions/example_*`),
  and the validator (`make check`, R). Treat `scripts/lib/submission_spec.R` as the
  authoritative schema.
- `/workspace/datasets/*` — fourteen public datasets, each with a `README.md`
  (provenance, verified facts, caveats — read it before touching the data). By role:
  - **Profile pool**: `acs` (2018 1-Year PUMS person file), `ces` (2024 Common
    Content 60k × 694 + cumulative 2006–2025; party × education × income).
  - **Baselines**: `tisp` (69,534 respondents, 68 countries, US n=2,559 — **the
    target study's exact 12-item trust-in-scientists scale**), `ccam` (US climate
    attitudes 2008–2024, 31 waves), `gss` (1972–2024 cumulative).
  - **Multi-arm experiments** (real intervention ATEs to practice on):
    `voelkel2026` (10 short climate messages + 3 controls, 13.8k, all outcomes
    0–100 sliders, all six moderators — the target study's closest design twin),
    `goldwert2026` (16 interventions + 2 controls, 31k, sliders + real
    petition/newsletter/donation outcomes), `vlasceanu2024` (11 interventions,
    59k, 63 countries, US n=8,253), `bbprime2025` (17 interventions + control,
    7.6k, individual-level 0–100 sharing + petition outcomes), `voelkel2024`
    (25 interventions, 35k, democratic attitudes — domain transfer).
  - **Trust-effect prior**: `gligoric2025` (trust in 35 scientist occupations ×
    ideology, US n=7,800; five randomized trust-raising messages, all ≤0.05
    effect on a 7-point scale — conservatives-only randomization).
  - **Response format**: `gatewaybelief` (0–100 slider and 1–7 Likert items in
    the *same respondents*, pre/post a consensus message — the Likert→slider
    bridge), `orchinik2024` (slider heaping in a quota panel: 42.5% of responses
    on multiples of 5, 15.5% at endpoints), `sce` (186k rows of 0–100 items with
    demographics; 75% on multiples of 5, 17% at 50, heaping falls with education).

## What you are building

The loop that (1) practices analysis-level prediction on training tasks carved from the
datasets, (2) predicts the target study's analyses, and (3) synthesizes a Tier-1
individual-level dataset backwards from those predictions — one that passes the benchmark's
validator and reproduces the predicted analyses when they are recomputed from it.

Decide its shape yourself. Open questions you own, among others: what a training task is
and how its ground truth is held out; how the predictor is prompted or composed and what it
may read; how backward synthesis targets distributions and moderation rather than means
alone; what a run is and when it stops; which roles exist and whether they are `rlm()`
children, skills, or plain code; how self-scores are recorded so improvement across runs is
a measurement and not an impression.

Effect-level practice is possible: five multi-arm experiments carry real intervention
ATEs with held-out-able ground truth, and `voelkel2026` in particular matches the target
study's format (short messages, 0–100 sliders, quota panel, same moderators). One
asymmetry remains, honestly: none of them randomizes messages onto the *trust* outcomes
the target study leads with — the closest evidence (`gligoric2025`) says such messages
moved trust not at all, in a conservatives-only design. How you let that null discipline
your trust-outcome ATEs, and what the observational baselines can and cannot validate,
are findings, not footnotes; record them in `DESIGN.md`/`OPEN.md`.

## Scope of THIS session — authoring only

- **No simulator calls.** Not one. `AGENTS.md` describes how they will work later.
- **No batch processing of the microdata.** Inspect structure, read codebooks, take small
  samples to understand shape — no full-file computation yet.
- **Running the benchmark validator on its shipped example is fine** (it is local R and
  costs nothing); do not run your own loop.
- **Do not run `git` commands.** History is managed outside this session.

## Deliverables

1. The harness itself: skills under `.prime/agent/skills/`, and the loop in `AGENTS.md`
   (edit it — it is yours now). `.prime/agent/APPEND_SYSTEM.md` is frozen; leave it alone.
2. `DESIGN.md` — one screen at top level: what the loop is, why it has that shape, and the
   three most consequential choices you made with the alternative you rejected for each.
   Below the fold, as much detail as you want.
3. `OPEN.md` — what you could not decide without more information, and what would decide it.

## Rules

- **Do not restate or redefine the frozen scoring tables.** Reference them; if one is wrong
  or insufficient, say so in `OPEN.md` rather than editing it.
- Everything a later run needs must be on disk. Kernel state does not survive the session.
- If you refine during this session, record what changed, what evidence motivated it, and
  which scoring row it was meant to move.
- Prefer fewer, sharper files over many.

Finish by reporting: what you built, what you assumed that a human should check, and what
you need in order to make the first real run.
