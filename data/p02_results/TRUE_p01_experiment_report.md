# TRUE Simulation Experiment Report (P0/P1 Refactored)

## Executive Summary

This experiment compares TRUE and its ablations against Blind and TTB baselines across 2 parameterized scenarios.
All groups within a Monte Carlo run face the identical task sequence. 20 runs x 200 rounds x 2 scenarios x 2 groups.

Key P0/P1 changes from the previous round:

1. **Fixed task-flow pairing**: same task sequence for all groups per run.
2. **Removed group-specific observation manipulation**: A8 surface/observed signals are no longer artificially elevated for any single group.
3. **Renamed MOO -> TTB**: honest description as a trust-targeted heuristic baseline, not a full Pareto/Tchebycheff solver.
4. **Ablation variants**: TRUE-C (no constraints), TRUE-E (no exploration bonus), TRUE-N (no newcomer protection).
5. **Statistical upgrades**: Wilcoxon signed-rank test, bootstrap 95% CIs, Bonferroni correction.
6. **Runs increased**: from 60 to 100.

## Scenario Definitions

- **Observation-Manipulated**: Observation-contaminated environment where surface quality can diverge from true quality.
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
| Observation-Manipulated | TTB-cap | 2884.0 | [1998.0, 3780.0] | 0.809 | 0.660 | 50.3 | 0.778 | 0.738 | 0.443 | 999.0 | 0.000 |
| Observation-Manipulated | Blind | -26416.0 | [-27234.0, -25616.0] | 0.334 | 0.441 | 203.2 | 0.313 | 0.521 | 0.313 | 6.7 | 0.000 |
| Baseline | TTB-cap | 1152.0 | [530.0, 1820.0] | 0.797 | 0.763 | 60.6 | 0.733 | 0.741 | 0.445 | 999.0 | 0.000 |
| Baseline | Blind | -23574.0 | [-24493.0, -22716.0] | 0.347 | 0.407 | 208.3 | 0.314 | 0.528 | 0.317 | 6.0 | 0.000 |

## Scenario Conclusions

### Observation-Manipulated


### Baseline


## Hypothesis Tests

| Scenario | Hypothesis | Mean Diff | t | p_t | p_t(Bonf) | W | p_w | p_w(Bonf) | Cohen d |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

## Interpretation & Limitations

- Task flows are paired: within each run all groups see the same module sequence. Differences in outcome are therefore attributable to selection mechanisms, not task luck.
- A8 surface-quality bonus is uniform across groups. The only remaining A8 asymmetry is inside TTB's scoring function (A8 receives extra trust-objective weight), which is a *mechanism-level* difference, not an observation-level manipulation.
- Ablation results isolate component contributions: if TRUE-C is substantially worse than TRUE, the constraint filter is a key driver of advantage.
- Bonferroni correction is conservative; if a hypothesis remains significant after correction, the conclusion is robust.
- The experiment remains a probabilistic generative model; no real engineering tools are used.
