# TRUE Simulation Experiment Report (P0/P1 Refactored)

## Executive Summary

This experiment compares TRUE and its ablations against Blind and TTB baselines across 1 parameterized scenarios.
All groups within a Monte Carlo run face the identical task sequence. 100 runs x 200 rounds x 1 scenarios x 2 groups.

Key P0/P1 changes from the previous round:

1. **Fixed task-flow pairing**: same task sequence for all groups per run.
2. **Removed group-specific observation manipulation**: A8 surface/observed signals are no longer artificially elevated for any single group.
3. **Renamed MOO -> TTB**: honest description as a trust-targeted heuristic baseline, not a full Pareto/Tchebycheff solver.
4. **Ablation variants**: TRUE-C (no constraints), TRUE-E (no exploration bonus), TRUE-N (no newcomer protection).
5. **Statistical upgrades**: Wilcoxon signed-rank test, bootstrap 95% CIs, Bonferroni correction.
6. **Runs increased**: from 60 to 100.

## Scenario Definitions

- **Baseline**: Standard engineering collaboration with moderate observation noise.

## Group Definitions

- **TRUE**: full mechanism (constraints + Thompson sampling + exploration bonus + newcomer protection).
- **TRUE-C**: ablation -- safety constraints removed (fatal pre-filter disabled, feasible always true).
- **TRUE-E**: ablation -- exploration bonus removed (tv term set to zero).
- **TRUE-N**: ablation -- newcomer protection removed (no coverage bonus, no auto-feasible for low-coverage candidates).
- **Blind**: no trust system; assignment by seniority/type-preference randomization.
- **TTB**: Trust-Targeted Baseline; deterministic heuristic that optimizes a single score heavily weighted by trust mean + selection popularity.

## Results Summary

| Scenario | Group | Cum.Utility | 95% CI | True Q | Surface Q | Fatal | Success | Gini | Collapse | A9 Delay | A8 Corr |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | TRUE | 1161.4 | [822.4, 1529.4] | 0.768 | 0.739 | 60.3 | 0.737 | 0.636 | 0.395 | 0.4 | 0.293 |
| Baseline | Blind | -23924.6 | [-24255.4, -23621.6] | 0.343 | 0.402 | 209.6 | 0.307 | 0.529 | 0.318 | 6.3 | 0.000 |

## Scenario Conclusions

### Baseline

- TRUE vs Blind: cumulative utility diff = 25086.0; fatal errors diff = -149.2.
- TRUE A9 first delay = 0.4; collapse index = 0.395.

## Hypothesis Tests

| Scenario | Hypothesis | Mean Diff | t | p_t | p_t(Bonf) | W | p_w | p_w(Bonf) | Cohen d |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | TRUE_U > Blind_U | 25086.000 | 129.016 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.902 |
| Baseline | TRUE_Fatal < Blind_Fatal | 149.240 | 136.247 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.625 |
| Baseline | TRUE_A9 < Blind_A9 | 5.930 | 8.326 | 0.0000 | 0.0000 | 80.500 | 0.0000 | 0.0000 | 0.833 |

## Interpretation & Limitations

- Task flows are paired: within each run all groups see the same module sequence. Differences in outcome are therefore attributable to selection mechanisms, not task luck.
- A8 surface-quality bonus is uniform across groups. The only remaining A8 asymmetry is inside TTB's scoring function (A8 receives extra trust-objective weight), which is a *mechanism-level* difference, not an observation-level manipulation.
- Ablation results isolate component contributions: if TRUE-C is substantially worse than TRUE, the constraint filter is a key driver of advantage.
- Bonferroni correction is conservative; if a hypothesis remains significant after correction, the conclusion is robust.
- The experiment remains a probabilistic generative model; no real engineering tools are used.
