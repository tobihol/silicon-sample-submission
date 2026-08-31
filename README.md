# team_31 Silicon Sample Benchmark: code snapshot

Code repository for the two Tier-1 entries of **team_31** in the
[Silicon Sample Benchmark](https://janpfander.github.io/llm_predictions_megastudy/) (2026),
referenced as `code_repository` (registration item K.1) by both entries' Zenodo records.

## Methods

Both entries share one setup: **dataset acquisition → prime-agent loop → derivation of
individual-level rows**. They are analysis-first: they predict the target study's published
analysis table (16 interventions × 13 outcomes, control levels, distributions) rather than
simulating respondents, and synthesize the individual-level rows backwards so the benchmark's
own analysis code reproduces the table.

The loop runs on [Prime Agent](https://github.com/PrimeIntellect-ai/prime-agent)
([paper](https://arxiv.org/abs/2608.23552)), a self-improving harness built on two ideas:
[Recursive Language Models](https://arxiv.org/abs/2512.24601) (Zhang, Kraska and Khattab) and
the [Continual Harness](https://arxiv.org/abs/2605.09998) (Karten et al.). Both entries run on
`claude-opus-5`.

The method of each entry is the **start state of its loop**, and that start state is what this
repository holds. What the loop produced (the fitted model, the target card, the campaign
records) is the loop's output, deposited in each entry's own record under `run_record/`. The
two entries differ only in how the loop is handled:

| directory | entry | how the loop is handled |
|---|---|---|
| [`llm-as-scientist-v1/`](llm-as-scientist-v1/) | [secondary-1](https://github.com/tobihol/silicon-sample-entry-llm-as-scientist-v1) | **Prescribed strategy, self-administered testing.** The start state fixes the strategy and the materials: predict the study analysis-first, synthesize the rows backwards, improve by practicing on tasks built from published data, and build the entry from nothing but that data plus plain model completions (fixed prompts, no tools, no agent runtime, thinking off). The deposited entry is therefore independent of the building agent's own reasoning: it reproduces from code, data, and a handful of cached completions. Testing was self-administered: practice ground truth sat in the loop's own filesystem, held out only by its own discipline, with no external rules. |
| [`llm-as-scientist-v2/`](llm-as-scientist-v2/) | [**primary**](https://github.com/tobihol/silicon-sample-entry-llm-as-scientist-v2) | **Free strategy, externally administered testing.** No restriction on how the agent makes predictions: it is free to use scripts, simulator calls, or anything else. The restrictions sit on information instead: there are held-out data that are excluded from its container, feedback comes only through an oracle (only 2 submissions per study allowed). Its outcome was to write and fit an explicit structural model on the train split. This mirrors [Prime Agent's ARC-AGI-3 evaluation](https://arxiv.org/abs/2608.23552): unseen games with hidden rules, learned by experimenting under an action budget. Here the game is a sealed study, and the scored moves are rationed. |

The internal arm names `idea_01` (= v1) and `idea_03` (= v2) are used in paths throughout
the registration forms, scripts, and documentation. The symlinks `idea_01` and `idea_03`
in this repository keep every such path valid.

## What this repository holds

The **environment and start state** of each experiment, meaning what you would need to run
it again. The *outcomes* (predictions, distilled method code, campaign records) are in each
entry's own Zenodo record under `run_record/`. The *trajectory* (complete session transcripts)
is the primary entry's restricted-access log archive (registration item K.2).

## Layout

| path | what |
|---|---|
| `llm-as-scientist-v2/` | primary entry's start state: frozen definitions (`frozen.sha256`, `run/.prime/agent/APPEND_SYSTEM.md`), launch budgets, the first session brief (`run/TASK_01.md`), starting material (`run/SCAFFOLD.md`), the session driver (`run_session.sh`: preflight, oracle, session, post-run audits). The agent's work products (model code, anchors, reports) are in the entry deposit's `run_record/`, and mounted inputs are rebuilt by `utils/heldout/setup_idea03.sh` |
| `llm-as-scientist-v1/` | secondary-1 entry's start state: frozen definitions (`frozen.sha256`, `run/.prime/agent/APPEND_SYSTEM.md`), the first session brief (`run/TASK_01.md`), the session driver (`run_session.sh`). The pipeline and its inputs are in the entry deposit's `run_record/pipeline/` |
| `utils/heldout/` | the validation environment: held-out carving, scoring oracle, leave-one-study-out gate, leak audits |
| `utils/prime/` | container + launcher for the agent sessions, evaluation forks, promotion ledger |
| `data/` | per-study READMEs with licences and `fetch.sh` scripts (raw data are fetched, never committed) |

## Entries

The deposited entries (predictions, filled registration forms, method records) are separate
repositories, each its own Zenodo record (DOIs in the benchmark deposit):
[silicon-sample-entry-llm-as-scientist-v2](https://github.com/tobihol/silicon-sample-entry-llm-as-scientist-v2) (primary) and
[silicon-sample-entry-llm-as-scientist-v1](https://github.com/tobihol/silicon-sample-entry-llm-as-scientist-v1) (secondary-1). Registered team: Tobias Holtdirk,
Bolei Ma (LMU Munich, SODA Lab). Contributor: Haiwen Huang. Contact: tobias.holtdirk@lmu.de.
