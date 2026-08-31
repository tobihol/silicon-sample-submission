# utils/ — shared infrastructure for all ideas

Operator-side structural tooling. **Agent-agnostic at the top, one runtime per
subfolder**: an idea picks whatever agent harness fits it (Prime Agent, Claude
Code, …); what all ideas share is the *contract* below, not the agent. None of
this is mounted into a session.

## The idea contract (agent-agnostic)

Each `idea_NN/` in the repo root is one self-contained approach:

    idea_NN/
      README.md          what the idea is — and WHICH RUNTIME it uses
      frozen.sha256      operator signature over the idea's frozen definitions
      run/               EVERYTHING THE CONTAINER SEES as its working directory:
                         the frozen definitions, the agent-owned files, task
                         files, and runs/<run-id>/ products

Invariants, whatever the agent:

- **The mount set is the boundary.** A session sees its idea's `run/`
  (read-write), `data/` at `/workspace/datasets` (read-only), the official
  submission template at `/workspace/benchmark` (read-only), and the uv project
  files — nothing else. It is also the blinding boundary: no mount carries
  human outcome data of the target study.
- **Frozen definitions are witnessed, not unwritable.** Every runtime has some
  file that is always in the agent's context (Prime Agent:
  `run/.prime/agent/APPEND_SYSTEM.md`; Claude Code: `run/CLAUDE.md`). That file
  carries the binding definitions, and `sign-frozen.sh` signs it into
  `<idea>/frozen.sha256` — which lives outside the mount set, so an in-container
  edit cannot forge it. Launchers refuse to start on a signature mismatch and
  shout if the hash moved during a run.
- **State is mounted, resettable, diffable.** Per-idea, per-arm agent state
  lives under `.container-state/arms/<idea>/<arm>/`; launchers snapshot the
  mutable surface before and after every run into
  `.container-state/snapshots/<run-id>/`. What a harness learned is a diff, not
  an anecdote.
- **Credentials never enter an image or the repo.** OAuth tokens live in
  `.container-state/` (gitignored) and are bind-mounted or passed by env file.
  `ANTHROPIC_API_KEY` is never forwarded — an ambient key silently outranks a
  subscription login and bills the metered API.

Shared tooling at this level:

| | |
|---|---|
| `sign-frozen.sh <idea> [file]` | sign an idea's frozen definitions (auto-detects the runtime's frozen file; pass the idea-relative path to override) |

## Runtimes

### `prime/` — Prime Agent (used by `idea_01`)

Self-refining harness: the agent edits durable harness state (`/refine`,
`AGENTS.md`, skills) from its own trajectory; arms make the accumulation
resettable. Adapted from `gssim_prime`.

| | |
|---|---|
| `prime/Dockerfile` | Prime Agent (pinned version + SHA-256), Claude Code CLI as plain-completion simulator interface, uv kernel venv baked at `/opt/kernel/venv`, R with the benchmark validator's packages |
| `prime/run.sh` | the launcher: mount set per the contract, frozen check, arm state at `~/.prime/agent`, before/after snapshots |

```bash
docker build -t ssb-prime:latest utils/prime/
SSB_IDEA=idea_01 SSB_ARM=fresh ./utils/prime/run.sh     # then /login
```

Two logins, because two programs need credentials (details in `prime/run.sh`
header): Prime Agent via `/login` once (lands in `.container-state/auth.json`,
shared across arms), and the Claude CLI simulator via a bare
`CLAUDE_CODE_OAUTH_TOKEN=…` line in `.container-state/container.env`.

| variable | meaning |
|---|---|
| `SSB_IDEA` | required — which idea's `run/` to mount |
| `SSB_ARM` | experimental condition; new name = fresh harness state, reuse = carried |
| `SSB_DATASET` | optional — mount only `data/<name>` instead of all of `data/` |
| `SSB_MODEL`, `SSB_THINKING` | model + reasoning pins (default `claude-opus-5`, `high`) |
| `SSB_AUTOREFINE` | `on` (default) or `off` — pins Prime Agent's auto-refine per arm via its `settings.json` (upstream default is on, so the regime is recorded, not inherited) |
| `SSB_AUTONOMOUS_MAX_CONTINUATIONS` etc. | budgets pinned when the caller passes `--autonomous` (upstream defaults are 3 continuations / 12 turns / 80k tokens / 30 min — far too small for idea sessions). Defaults: 10 / 300 / 8M / 3h; also `_MAX_TURNS`, `_MAX_TOKENS`, `_TIMEOUT_MS` |
| `SSB_GATE` | completion gate for `--autonomous` runs (ARC-3-style: the session may not finish until it passes; failure output is fed back). Default: operator-owned `utils/prime/gates/session_gate.py`, mounted read-only at `/workspace/gates`. `off` disables; any other value replaces the gate command |
| `SSB_GOAL`, `SSB_GOAL_TOKENS` | optional persistent goal (`--goal`): re-prompted across continuations until the agent calls `goal.complete()`, optionally with its own token budget |
| `SSB_DETACH=1` | run detached (no post-run snapshot — take it yourself) |
| `SSB_STATE` | state dir, default `.container-state/` |
| `SSB_DATASET_EXCLUDE` | comma list of `data/<name>` directories NOT to mount (idea_02's held-out studies). Every other dataset is mounted individually; text files in the mount set that name an excluded study are overlaid with redacted copies |
| `SSB_RUN_DIR`, `SSB_PRIME_DIR` | mount another directory as `/workspace/run` / use another arm-state directory — evaluation forks (`prime/fork_eval.sh`) |
| `SSB_EXTRA_MOUNTS` | `;`-separated extra `host:container[:ro]` bind mounts |
| `SSB_LEDGER_PROMOTE=1` | after the run, `prime/promote_ledger.py` merges the session's *local* Prime harness ledger (auto-refine writes only there) into the arm's *global* ledger, so it persists into the next session — Prime itself never does this |

### `heldout/` — the held-out environment for idea_02 (host side, never mounted)

Held-out truths live **beside their raw data** in `data/<study>/carved/` (gitignored like
`downloads/`); an idea declares which dataset directories its container may not see in
`<idea>/launch.env` (`SSB_DATASET_EXCLUDE`), and the launcher mounts every other dataset.
Scorer state — log, internal-test scores, audits — lives in `idea_02/eval/`, outside `run/`.

| | |
|---|---|
| `heldout/carve_val.py` | carve validation + internal-test tasks from idea_01's adapters: truth to `data/<study>/carved/`, design-only briefs to `idea_02/run/inputs/val/` (internal test: `data/bbprime2025/carved/brief/`) |
| `heldout/score_daemon.py` | the environment's scorer: watches submissions, writes task-level `score_<k>.json`, cap 5 per task per session, hashed log in `idea_02/eval/`; `--itest` for forks |
| `heldout/build_idea01_lib.py` | build `idea_02/run/inputs/idea01_lib/` — idea_01's code/notes with every held-out passage removed, scanner-verified |
| `heldout/sibling_leak_scan.py` | name/alias scan for the held-out studies (exit 1 on any hit) — the gate for mounts and forks |
| `heldout/leak_audit_run.py` | value-echo audit of every transcript and run-tree file against every carved truth (idea_01's probe), record under `idea_02/eval/audits/` |
| `prime/fork_eval.sh <arm> <n>` | the internal-test fork: copy arm state + run tree, add the bbprime brief, one session with auto-refine off, sealed score, read-only archive |
| `heldout/carve_arm_holdout.py` | **idea_04**: arm-level holdout inside train megastudies — folds (val/sealed), truths to `data/<study>/carved_arms/<fold>/`, briefs with an `instrument` block, and MASKED dataset copies under `.container-state/masked/idea_04/` (mounted via `SSB_DATASET_REPLACE`); `--measure` prints every candidate study's within-outcome reliability |
| `heldout/score_oracle4.py` | idea_04's oracle: full-sample truth + fresh per-cell noise per scored call, cap 2, diagnostics only, moderator-contrast diagnostic, `--itest` battery (anchor + sealed arm folds) |
| `heldout/cell_gate.py` | idea_04's gate: pooled r-within over all promotion cells, cluster bootstrap over arms, PROMOTED / REJECTED / UNDERPOWERED + 90% band + β bucket (cells standardised per task; `--baseline-k` / `--baseline-only` for single-run ablations) |
| `heldout/paired_h2h.py` | paired per-cell head-to-head on bokemper2022 for idea_01/02/03 cell files (mean abs-error diff, cell + arm-cluster bootstrap, sign test) — `docs/heldout-h2h-2026-08-26.md` addendum |
| `heldout/itest_summary4.py` | opens idea_04's sealed internal-test scores **after the campaign ends**, prints them against the pre-registered bars, paired fork-2 − fork-1 bootstrap on the anchor |
| `heldout/brief_instrument.py`, `heldout/build_idea03_lib.py`, `heldout/setup_idea04.sh` | idea_04 setup: instrument tables for the study-level briefs; idea_03's redacted design record/tools/anchors; the one-shot setup |
| `prime/fork_eval4.sh <arm> <n>` | idea_04's internal-test fork: anchor study + every sealed arm fold, scored by `score_oracle4.py --itest` |

After every session, regenerate the operator-side ledger: `uv run
utils/track_progress.py` — now also `--idea idea_03` (reads the escrow bundle's Prime transcripts) and `--idea idea_04`, writing `docs/progress-ledger-idea0{3,4}.md` with adjusted metrics and per-call sub-agent usage — (one row per session: exact harness tokens/$ from the
session logs, billed simulator tokens, practice metrics) -> `docs/progress-ledger.md`.

**Daemon startup hangs** (container up, JSON log empty, prime-agent processes at
~0 CPU): two causes seen 2026-08-19/20, both pre-loop so the autonomous timeout never
arms. (1) Stale `session-leases/`/`daemon-workers/` after a force-stop — run.sh now
auto-quarantines these before every launch. (2) A large accumulated
`session-artifacts/` tree (1.1G) deadlocked the daemon at "listening"; fix by moving
`session-artifacts/` aside (it only serves resumption of OLD sessions, which one-shot
runs never do; note snapshots read harness_state from it, so quarantine — don't
delete). ALWAYS health-check a launch: ≥1 `turn_start` in the JSON log within 5
minutes, else stop + quarantine + relaunch.

The launcher also refuses to run (and `sign-frozen.sh` refuses to sign) if a
`SYSTEM.md` exists beside the frozen `APPEND_SYSTEM.md`, or if the arm state
carries its own `SYSTEM.md`/`APPEND_SYSTEM.md`: those files replace or extend
the system prompt *around* the signature, so their absence is part of the
frozen contract (checked before and after every run).

### Adding a runtime (e.g. Claude Code)

`gssim_prototype` is the reference for a Claude Code runtime: `run/CLAUDE.md`
as the frozen orchestrator instructions, subagents under `run/.claude/agents/`,
sessions launched headless with
`claude -p "$(cat <kickoff>)" --model … --dangerously-skip-permissions` inside
the same kind of container. To add it: create `utils/claude-code/` with a
Dockerfile and a `run.sh` honoring the contract above (same mount set, same
frozen check against `<idea>/frozen.sha256`, same snapshot layout), and declare
the runtime in the idea's README. Nothing in `data/`, the template mount, or
`sign-frozen.sh` needs to change.
