# The frozen definitions — idea_03

Everything below is fixed for the duration of a run. You may not edit this file, restate it
in your own words elsewhere, or work around it locally. If something here is wrong or
missing, say so in `OPEN.md` and continue under it. A gate checks this file's hash before a
run may finish.

Everything *not* in this file — `AGENTS.md`, `SCAFFOLD.md`, the skills you write, your
harness ledger — is yours to change. **This file contains no instructions about *how* to
predict.** That is deliberate: how you predict is entirely yours.

## The objective

The validation scores you receive are **instrumental**. The score that matters is a sealed
internal test you will never see feedback from, and after that the sealed target study.
Both are studies you have never received a score on. A solution fitted to the particular
studies in your validation set will not transfer; a general solution — one that predicts
*any* message-persuasion study of this family from its design — will. Every mechanism in
this environment (fresh-draw truths, the submission budget, the promotion gate) exists to
make that distinction visible; none of it can be gamed into saying otherwise.

## What you build

**You are the predictor.** The target study tests 16 message interventions (plus control)
for increasing trust in climate scientists on ~18,000 U.S. adults (census-based quotas on
age, gender, race/ethnicity), and is scored on 13 outcomes. Your product is (a) predictions
of the target study's *analysis results* — treatment effects, condition × outcome means,
subgroup moderation, response distributions — and (b) an individual-level synthetic dataset
(Tier 1) generated **backwards from those predictions**, such that running the benchmark's
analyses on it reproduces them.

Everything public about the target is yours to study:

- `/workspace/benchmark` — the official template: survey instrument, the 16 intervention
  texts, codebook, validator.
- `inputs/organizer_code/` — **the organizers' actual scoring pipeline** (`statistics.R` +
  the preregistration qmd, pinned to a verified commit). This is how you will be scored:
  which metrics, pooled how, corrected how, against which floors and reference rows. Read
  it before predicting anything; knowing the metric changes what a good prediction is.

## The data split — binding

| split | where | what you may do |
|---|---|---|
| **train** | `/workspace/datasets/*` (published experiments with outcomes; survey microdata) | anything: read outcomes, fit anything, iterate without limit — this is where "how exactly did I fail" belongs |
| **validation** | `inputs/val/<task>/brief/` — design only, 7 studies | predict, submit, receive diagnostics (below); you never see outcomes |
| **internal test** | not on this branch | a battery of studies whose identities are undisclosed; an evaluation fork of your arm predicts it with the target procedure, once, and you never see the brief, the submission, or the score |
| **test** | the target study at `/workspace/benchmark` | predict it; its human results do not exist for you |

Validation studies are published. You do not have their data, and you must not reconstruct
it: no retrieval of any kind, no reasoning from a remembered paper. If you recognise a
validation study and remember its results, record that in `OPEN.md` and predict from the
brief anyway; the recognition is disclosed, the memory is not used. Ten datasets are
absent from `/workspace/datasets` on purpose; do not look for them.

## The validation environment — binding

- A validation task is a **whole study**: every arm × every outcome in `template.csv`, in
  percentage points of each outcome's scale range, written to
  `runs/<run-id>/val/<task>/submission_<k>.csv` (optional Section-2/3 companions as each
  `task.json` lists).
- **Fresh-draw truth.** Every scored submission is evaluated against a *different* random
  half of the study's respondents. There is no fixed noise draw: resubmitting to chase a
  number re-rolls the truth. Improvements that survive this are real; improvements that
  don't were noise.
- **Budget: 2 scored submissions per task per run id.** The scorer refuses the third
  (`refused_<k>.json`). This is a property of the environment, not a request.
- `score_<k>.json` returns **diagnostics, not raw scores**: `r_adj` and `r_within_adj`
  (attenuation-corrected skill — the currency), `rmse_adj_pp`, directional agreement,
  calibration `alpha`/`beta`, `spread_ratio`, `mean_signed_error_pp`. Raw correlations and
  RMSE against the half are never returned; with the correction, your numbers are
  comparable across tasks and across halves. Two tasks are marked
  `counts_toward_promotion: false` — their truth is too noisy to certify improvement; they
  are diagnostics for you, nothing more.
- **Promotion is mechanical.** When you believe a change generalizes, say so in your
  ledger and `REPORT.md`; the operator runs a leave-one-study-out gate over the promotion
  tasks against a baseline run. You receive `gate_<tag>.json`: a verdict (PROMOTED /
  REJECTED) and, on rejection, the outcome *family* that failed — never per-study scores.
  Only techniques that help held-out studies on average, without hurting any one study
  beyond noise, survive into your durable state.

## Words

- **target study** — the sealed megastudy. Its instrument, codebook and validator are at
  `/workspace/benchmark`; its human results do not exist for you.
- **training task** — an analysis task carved from `/workspace/datasets/*` whose ground
  truth you may read.
- **validation task** — a task whose ground truth the environment holds.
- **entry** — one complete set of predictions for the target study at one tier.
- **analysis-first** — predictions are made at the level the benchmark scores, never as a
  side effect of item-by-item simulation.
- **backward synthesis** — generating individual rows to match predicted analysis results:
  cells, moderation, *and* distributions.
- **operator** — the human. Owns the budget, the model list, the sealed truth, the gate,
  and the deposit decision. **Never edits a predicted number.**

## The target study's scoring — read the code

The authoritative description of the scoring is the organizers' own code in
`inputs/organizer_code/`. In brief: predictions are scored against one human half
("Human 1"), with the other half's agreement as the replication reference; all effects are
converted to percentage points of each outcome's scale range and pooled over all 16 × 13 =
208 intervention × outcome effects; Section 1 is ATE recovery (directional agreement with
half credit for predicted zeros, Spearman ρ, Pearson r, **Pearson r within outcomes**,
RMSE, and the attenuation-corrected r_adj / RMSE_adj) plus calibration (α, β); Section 2
is subgroup moderation via condition × moderator interaction contrasts; Section 3 is
response distributions (variance ratio, OVL, KS, W1) and demographic diagnostics. Two
scripted floors (no-effect, all-positive) frame every metric.

Coverage rules: all 17 conditions × 13 outcomes, every cell exactly once, no NA. Tier-1
floor: ≥ 500 respondents per intervention, ≥ 1,000 in control. Composites are scored as
submitted, never recomputed. When you score a training task yourself, use these metrics
and no others.

## Blinding — absolute

- You never seek, ingest, or infer from human outcome data of the target study — including
  its pilots, preprints about it, talks about it, or anything derived from them. If you
  encounter any, stop, record where, and tell the operator.
- Do not attempt retrieval of any kind — no web, no remote data or code repositories, no
  literature, nothing beyond the model API your tools already use. Installing software
  packages from the Python package index (`uv`, `pip`) is the one permitted network use.
  Transcripts are audited; a retrieval attempt is itself recorded and reported, whatever it
  returned.
- Training ground truth comes from `/workspace/datasets/*` and published literature on
  *other* studies only. Validation ground truth comes from nowhere.
- The pipeline is AI-based and fully automated end to end: no human edits a prediction, and
  you never ask the operator what a number should be.

## Calling a simulator

If any stage uses per-respondent generation, a simulator is a **plain completion**: fixed
system prompt, one user message, no tools, no retrieval, no filesystem, no agent wrapper.

```bash
env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN MAX_THINKING_TOKENS=0 \
  claude -p "<user text>" --system-prompt "<system text>" --tools "" \
  --settings '{"claudeMdExcludes":["**"]}' \
  --no-session-persistence --output-format json --model <model-id>
```

Use the provider's default sampling; never tune it per task. Cache responses under a key
covering the prompt **and** every sampling parameter. A simulator is a tool you may use;
the prediction is yours.

## Reuse of the earlier ideas

`inputs/idea01_lib/` holds idea_01's synthesis, deposit and scoring code and its redacted
design notes (passages about held-out studies removed and marked). `SCAFFOLD.md` lists
what measurably transferred from both earlier campaigns. All of it is **starting material,
not rules**: import the code if it helps, adopt or discard the defaults on your own
evidence. You may not have either idea's target predictions, calibration outputs, or
cards; your prediction is independent.

## Budget

Model calls come out of a Claude subscription window shared with other work. Ask the
operator before any batch. Any deposited entry locks **August 31, 2026** — a deposit the
operator makes, never you; the campaign itself may continue past that date as a research
arm.

## Refinement and memory

Your durable state has two homes and both persist across sessions: the Prime Agent harness
ledger (`/refine`, `rlm.harness`, promoted to your arm's global ledger after every session)
and the files you write in this directory (`AGENTS.md`, skills, tools). When you refine,
record what changed, what evidence motivated it, and — since scores here are diagnostics
on fresh draws — which *mechanism* you believe improved, not which number moved. The gate
tests mechanisms; the record is what makes its verdicts interpretable later.
