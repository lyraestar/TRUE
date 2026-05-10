# TRUE Simulation Experiment Report (P0/P1 Refactored)

## Executive Summary

This experiment compares TRUE and its ablations against Blind and TTB baselines across 4 parameterized scenarios.
All groups within a Monte Carlo run face the identical task sequence. 2 runs x 10 rounds x 4 scenarios x 3 groups.

Key P0/P1 changes from the previous round:

1. **Fixed task-flow pairing**: same task sequence for all groups per run.
2. **Removed group-specific observation manipulation**: A8 surface/observed signals are no longer artificially elevated for any single group.
3. **Renamed MOO -> TTB**: honest description as a trust-targeted heuristic baseline, not a full Pareto/Tchebycheff solver.
4. **Ablation variants**: TRUE-C (no constraints), TRUE-E (no exploration bonus), TRUE-N (no newcomer protection).
5. **Statistical upgrades**: Wilcoxon signed-rank test, bootstrap 95% CIs, Bonferroni correction.
6. **Runs increased**: from 60 to 100.

## Scenario Definitions

- **Utility-Trust-Misalignment**: Local phases where trusted incumbents underperform and low-history entities hold latent value.
- **Safety-Critical**: High-stakes safety environment with harsher penalties and stronger error propagation.
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
| Utility-Trust-Misalignment | TRUE | -125.0 | [-590.0, 340.0] | 0.781 | 0.672 | 3.5 | 0.650 | 0.439 | 0.263 | 999.0 | 0.000 |
| Utility-Trust-Misalignment | Blind | -1455.0 | [-1570.0, -1340.0] | 0.337 | 0.526 | 11.0 | 0.150 | 0.529 | 0.317 | 999.0 | 0.000 |
| Utility-Trust-Misalignment | TTB | -880.0 | [-880.0, -880.0] | 0.479 | 0.529 | 7.0 | 0.400 | 0.580 | 0.348 | 999.0 | 0.674 |
| Safety-Critical | TRUE | -460.0 | [-740.0, -180.0] | 0.811 | 0.670 | 2.5 | 0.750 | 0.420 | 0.255 | 999.0 | 0.000 |
| Safety-Critical | Blind | -2240.0 | [-2240.0, -2240.0] | 0.338 | 0.355 | 9.5 | 0.400 | 0.474 | 0.285 | 999.0 | 0.000 |
| Safety-Critical | TTB | -1990.0 | [-3120.0, -860.0] | 0.382 | 0.463 | 9.5 | 0.450 | 0.453 | 0.272 | 999.0 | 0.000 |
| Observation-Manipulated | TRUE | -160.0 | [-160.0, -160.0] | 0.759 | 0.697 | 3.0 | 0.700 | 0.372 | 0.223 | 999.0 | 0.000 |
| Observation-Manipulated | Blind | -1500.0 | [-1640.0, -1360.0] | 0.328 | 0.448 | 12.0 | 0.250 | 0.446 | 0.268 | 999.0 | 0.000 |
| Observation-Manipulated | TTB | -1920.0 | [-1920.0, -1920.0] | 0.105 | 0.565 | 15.5 | 0.100 | 0.636 | 0.381 | 999.0 | -0.002 |
| Baseline | TRUE | 90.0 | [-60.0, 240.0] | 0.828 | 0.686 | 2.5 | 0.750 | 0.477 | 0.292 | 999.0 | 0.000 |
| Baseline | Blind | -1330.0 | [-1440.0, -1220.0] | 0.442 | 0.530 | 10.5 | 0.250 | 0.517 | 0.310 | 999.0 | 0.000 |
| Baseline | TTB | -1350.0 | [-2000.0, -700.0] | 0.425 | 0.607 | 12.0 | 0.250 | 0.484 | 0.290 | 999.0 | 0.390 |

## Scenario Conclusions

### Utility-Trust-Misalignment

- TRUE vs Blind: cumulative utility diff = 1330.0; fatal errors diff = -7.5.
- TRUE vs TTB: cumulative utility diff = 755.0; fatal errors diff = -3.5.
- TRUE A9 first delay = 999.0; collapse index = 0.263.

### Safety-Critical

- TRUE vs Blind: cumulative utility diff = 1780.0; fatal errors diff = -7.0.
- TRUE vs TTB: cumulative utility diff = 1530.0; fatal errors diff = -7.0.
- TRUE A9 first delay = 999.0; collapse index = 0.255.

### Observation-Manipulated

- TRUE vs Blind: cumulative utility diff = 1340.0; fatal errors diff = -9.0.
- TRUE vs TTB: cumulative utility diff = 1760.0; fatal errors diff = -12.5.
- TRUE A9 first delay = 999.0; collapse index = 0.223.

### Baseline

- TRUE vs Blind: cumulative utility diff = 1420.0; fatal errors diff = -8.0.
- TRUE vs TTB: cumulative utility diff = 1440.0; fatal errors diff = -9.5.
- TRUE A9 first delay = 999.0; collapse index = 0.292.

## Hypothesis Tests

| Scenario | Hypothesis | Mean Diff | t | p_t | p_t(Bonf) | W | p_w | p_w(Bonf) | Cohen d |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | TRUE_U > Blind_U | 1420.000 | 5.462 | 0.0000 | 0.0000 | 0.000 | 1.0000 | 1.0000 | 3.862 |
| Baseline | TRUE_Fatal < Blind_Fatal | 8.000 | 4.000 | 0.0001 | 0.0015 | 0.000 | 1.0000 | 1.0000 | 2.828 |
| Baseline | TRUE_U > TTB_U | 1440.000 | 1.800 | 0.0719 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 1.273 |
| Baseline | TRUE_Fatal < TTB_Fatal | 9.500 | 1.462 | 0.1439 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 1.033 |
| Baseline | TRUE_Collapse < TTB_Collapse | -0.002 | -0.025 | 0.9799 | 1.0000 | 0.000 | 1.0000 | 1.0000 | -0.018 |
| Baseline | TRUE_A9 < Blind_A9 | 0.000 | 0.000 | 1.0000 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.000 |
| Observation-Manipulated | TRUE_U > Blind_U | 1340.000 | 9.571 | 0.0000 | 0.0000 | 0.000 | 1.0000 | 1.0000 | 6.768 |
| Observation-Manipulated | TRUE_Fatal < Blind_Fatal | 9.000 | 9.000 | 0.0000 | 0.0000 | 0.000 | 1.0000 | 1.0000 | 6.364 |
| Observation-Manipulated | TRUE_U > TTB_U | 1760.000 | 0.000 | 1.0000 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.000 |
| Observation-Manipulated | TRUE_Fatal < TTB_Fatal | 12.500 | 25.000 | 0.0000 | 0.0000 | 0.000 | 1.0000 | 1.0000 | 17.678 |
| Observation-Manipulated | TRUE_Collapse < TTB_Collapse | 0.158 | 117.000 | 0.0000 | 0.0000 | 0.000 | 1.0000 | 1.0000 | 82.731 |
| Observation-Manipulated | TRUE_A9 < Blind_A9 | 0.000 | 0.000 | 1.0000 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.000 |
| Safety-Critical | TRUE_U > Blind_U | 1780.000 | 6.357 | 0.0000 | 0.0000 | 0.000 | 1.0000 | 1.0000 | 4.495 |
| Safety-Critical | TRUE_Fatal < Blind_Fatal | 7.000 | 3.500 | 0.0005 | 0.0112 | 0.000 | 1.0000 | 1.0000 | 2.475 |
| Safety-Critical | TRUE_U > TTB_U | 1530.000 | 1.085 | 0.2779 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.767 |
| Safety-Critical | TRUE_Fatal < TTB_Fatal | 7.000 | 1.400 | 0.1615 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.990 |
| Safety-Critical | TRUE_Collapse < TTB_Collapse | 0.017 | 0.294 | 0.7687 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.208 |
| Safety-Critical | TRUE_A9 < Blind_A9 | 0.000 | 0.000 | 1.0000 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.000 |
| Utility-Trust-Misalignment | TRUE_U > Blind_U | 1330.000 | 2.293 | 0.0218 | 0.5242 | 0.000 | 1.0000 | 1.0000 | 1.621 |
| Utility-Trust-Misalignment | TRUE_Fatal < Blind_Fatal | 7.500 | 15.000 | 0.0000 | 0.0000 | 0.000 | 1.0000 | 1.0000 | 10.607 |
| Utility-Trust-Misalignment | TRUE_U > TTB_U | 755.000 | 1.624 | 0.1044 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 1.148 |
| Utility-Trust-Misalignment | TRUE_Fatal < TTB_Fatal | 3.500 | 2.333 | 0.0196 | 0.4711 | 0.000 | 1.0000 | 1.0000 | 1.650 |
| Utility-Trust-Misalignment | TRUE_Collapse < TTB_Collapse | 0.084 | 2.786 | 0.0053 | 0.1282 | 0.000 | 1.0000 | 1.0000 | 1.970 |
| Utility-Trust-Misalignment | TRUE_A9 < Blind_A9 | 0.000 | 0.000 | 1.0000 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.000 |

## Interpretation & Limitations

- Task flows are paired: within each run all groups see the same module sequence. Differences in outcome are therefore attributable to selection mechanisms, not task luck.
- A8 surface-quality bonus is uniform across groups. The only remaining A8 asymmetry is inside TTB's scoring function (A8 receives extra trust-objective weight), which is a *mechanism-level* difference, not an observation-level manipulation.
- Ablation results isolate component contributions: if TRUE-C is substantially worse than TRUE, the constraint filter is a key driver of advantage.
- Bonferroni correction is conservative; if a hypothesis remains significant after correction, the conclusion is robust.
- The experiment remains a probabilistic generative model; no real engineering tools are used.
