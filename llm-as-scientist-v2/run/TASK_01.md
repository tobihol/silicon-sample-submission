# TASK_01 — read the scoring, take the first honest shot

You are starting `idea_03`. Read `.prime/agent/APPEND_SYSTEM.md` first; it is frozen and
signed, and unlike your predecessors' it contains **no instructions about how to predict** —
that part is entirely yours. What it does contain is the objective (validation is
instrumental; sealed held-out studies are what count) and the environment's mechanics
(fresh-draw truths, 2-submission budget, diagnostics-only feedback, the promotion gate).

## This session

1. **Read how you will be scored.** `inputs/organizer_code/` is the benchmark's actual
   scoring pipeline. Work out what it rewards — in particular what "Pearson r within
   outcomes" isolates, what r_adj corrects for, and what the floors and the Human-2 row
   mean for a submission. Write your conclusions into `DESIGN.md`.
2. **Inventory.** `/workspace/benchmark` (the target's full design, including the 16
   intervention texts), `/workspace/datasets` (the train split), `inputs/val/*/brief/`
   (7 validation briefs: `task.json` lists sections, moderators, submission files),
   `inputs/idea01_lib/` and `SCAFFOLD.md` (what the earlier campaigns learned — starting
   material, not rules).
3. **One honest submission per validation task.** Predict each of the 7 tasks from its
   brief and the train split, and submit `runs/<run-id>/val/<task>/submission_1.csv`
   (run id = `$SSB_RUN_ID`). The scorer answers within seconds. Remember the budget: 2
   scored submissions per task, and the truth re-rolls each time — spend the second one
   only on a *question*, never on a retry of the same idea. Record everything in
   `runs/scoreboard.csv`.
4. **Interpret the diagnostics, not the number.** For each task: is calibration β off? Is
   the spread ratio wrong? Is the signed error a level problem? The diagnostics name
   failure types; your job this session is a mechanism-level reading of where your
   predictions fail, written into `DESIGN.md`.
5. **Report.** `REPORT.md` for an operator who was away: what you predicted, what the
   diagnostics say, what you would change and *why it should generalize* (the gate will
   test exactly that), what you need from the operator. Open questions in `OPEN.md`.

Budget for this session: the launcher's defaults. No target prediction; no simulator
batches without asking.
