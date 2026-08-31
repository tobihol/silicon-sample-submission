# SCAFFOLD — what the earlier campaigns measured (defaults, not rules)

You may edit or delete this file. Nothing in it is binding; each line is an empirical
result from idea_01/idea_02 with the evidence class attached. Adopt, test, or discard.

| finding | evidence | status |
|---|---|---|
| Shrink predicted effect spread by κ ≈ 0.85 toward each outcome's mean | transferred blind (calibration β 0.94 on a study neither idea trained on) | strongest prior |
| Calibration β tends to run high without shrinkage (~1.5) | recurred across two independent campaigns | strong |
| Abstain from confident subgroup-moderation calls; low-rank moderation | held up wherever tested | strong |
| Brief richness matters: stripping items/texts from a brief cost r-within 0.44 → 0.16 | single ablation, idea_01 | medium |
| Prompt-lever tinkering (variants, draws, temperature, model line) | pre-registered null across idea_01's grid | known dead end |
| Per-study "solved optima" / frozen effect tables | transferred brittlely out-of-family (β −0.82 on an unseen study) | known failure mode |
| Rank-shifting predictions after the fact ("rankshift") | 69–88% precision on development studies, 27% blind | known failure mode |

The last three are why this environment exists: techniques that looked excellent on fixed
validation draws failed blind. The fresh-draw truths and the gate are how you avoid
re-learning that the expensive way.
