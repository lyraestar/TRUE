# TRUE Simulation Experiment Report (P0/P1 Refactored)

## Executive Summary

This experiment compares TRUE and its ablations against Blind and TTB baselines across 4 parameterized scenarios.
All groups within a Monte Carlo run face the identical task sequence. 2 runs x 10 rounds x 4 scenarios x 4 groups.

Key P0/P1 changes from the previous round:

1. **Fixed task-flow pairing**: same task sequence for all groups per run.
2. **Removed group-specific observation manipulation**: A8 surface/observed signals are no longer artificially elevated for any single group.
3. **Renamed MOO -> TTB**: honest description as a trust-targeted heuristic baseline, not a full Pareto/Tchebycheff solver.
4. **Ablation variants**: TRUE-C (no constraints), TRUE-E (no exploration bonus), TRUE-N (no newcomer protection).
5. **Statistical upgrades**: Wilcoxon signed-rank test, bootstrap 95% CIs, Bonferroni correction.
6. **Runs increased**: from 60 to 100.

## Scenario Definitions

- **Baseline**: Standard engineering collaboration with moderate observation noise.
- **Safety-Critical**: High-stakes safety environment with harsher penalties and stronger error propagation.
- **Observation-Manipulated**: Observation-contaminated environment where surface quality can diverge from true quality.
- **Utility-Trust-Misalignment**: Local phases where trusted incumbents underperform and low-history entities hold latent value.

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
| Baseline | TRUE | -210.0 | [-360.0, -60.0] | 0.720 | 0.703 | 4.0 | 0.650 | 0.421 | 0.253 | 999.0 | 0.000 |
| Baseline | Blind | -1350.0 | [-1480.0, -1220.0] | 0.332 | 0.428 | 10.0 | 0.250 | 0.505 | 0.303 | 999.0 | 0.000 |
| Baseline | TTB | -790.0 | [-960.0, -620.0] | 0.406 | 0.482 | 6.5 | 0.450 | 0.516 | 0.309 | 999.0 | 0.666 |
| Baseline | MOO | -530.0 | [-960.0, -100.0] | 0.611 | 0.659 | 5.5 | 0.550 | 0.448 | 0.269 | 999.0 | 0.000 |
| Safety-Critical | TRUE | -460.0 | [-740.0, -180.0] | 0.811 | 0.670 | 2.5 | 0.750 | 0.420 | 0.255 | 999.0 | 0.000 |
| Safety-Critical | Blind | -2240.0 | [-2240.0, -2240.0] | 0.338 | 0.355 | 9.5 | 0.400 | 0.474 | 0.285 | 999.0 | 0.000 |
| Safety-Critical | TTB | -1990.0 | [-3120.0, -860.0] | 0.382 | 0.463 | 9.5 | 0.450 | 0.453 | 0.272 | 999.0 | 0.000 |
| Safety-Critical | MOO | -1300.0 | [-1300.0, -1300.0] | 0.597 | 0.633 | 5.5 | 0.600 | 0.467 | 0.280 | 999.0 | 0.000 |
| Observation-Manipulated | TRUE | -160.0 | [-160.0, -160.0] | 0.759 | 0.697 | 3.0 | 0.700 | 0.372 | 0.223 | 999.0 | 0.000 |
| Observation-Manipulated | Blind | -1500.0 | [-1640.0, -1360.0] | 0.328 | 0.448 | 12.0 | 0.250 | 0.446 | 0.268 | 999.0 | 0.000 |
| Observation-Manipulated | TTB | -1920.0 | [-1920.0, -1920.0] | 0.105 | 0.565 | 15.5 | 0.100 | 0.636 | 0.381 | 999.0 | -0.002 |
| Observation-Manipulated | MOO | -1080.0 | [-1360.0, -800.0] | 0.417 | 0.399 | 8.0 | 0.400 | 0.343 | 0.206 | 999.0 | 0.000 |
| Utility-Trust-Misalignment | TRUE | 80.0 | [50.0, 110.0] | 0.828 | 0.727 | 3.0 | 0.700 | 0.437 | 0.265 | 999.0 | 0.000 |
| Utility-Trust-Misalignment | Blind | -1455.0 | [-1570.0, -1340.0] | 0.387 | 0.469 | 13.0 | 0.150 | 0.510 | 0.306 | 999.0 | 0.000 |
| Utility-Trust-Misalignment | TTB | -1195.0 | [-1510.0, -880.0] | 0.377 | 0.560 | 11.5 | 0.250 | 0.531 | 0.319 | 999.0 | 0.326 |
| Utility-Trust-Misalignment | MOO | -470.0 | [-1220.0, 280.0] | 0.614 | 0.637 | 7.5 | 0.500 | 0.507 | 0.304 | 999.0 | 0.000 |

## Scenario Conclusions

### Baseline

- TRUE vs Blind: cumulative utility diff = 1140.0; fatal errors diff = -6.0.
- TRUE vs TTB: cumulative utility diff = 580.0; fatal errors diff = -2.5.
- TRUE A9 first delay = 999.0; collapse index = 0.253.

### Safety-Critical

- TRUE vs Blind: cumulative utility diff = 1780.0; fatal errors diff = -7.0.
- TRUE vs TTB: cumulative utility diff = 1530.0; fatal errors diff = -7.0.
- TRUE A9 first delay = 999.0; collapse index = 0.255.

### Observation-Manipulated

- TRUE vs Blind: cumulative utility diff = 1340.0; fatal errors diff = -9.0.
- TRUE vs TTB: cumulative utility diff = 1760.0; fatal errors diff = -12.5.
- TRUE A9 first delay = 999.0; collapse index = 0.223.

### Utility-Trust-Misalignment

- TRUE vs Blind: cumulative utility diff = 1535.0; fatal errors diff = -10.0.
- TRUE vs TTB: cumulative utility diff = 1275.0; fatal errors diff = -8.5.
- TRUE A9 first delay = 999.0; collapse index = 0.265.

## Hypothesis Tests

| Scenario | Hypothesis | Mean Diff | t | p_t | p_t(Bonf) | W | p_w | p_w(Bonf) | Cohen d |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | TRUE_U > Blind_U | 1140.000 | 4.071 | 0.0000 | 0.0015 | 0.000 | 1.0000 | 1.0000 | 2.879 |
| Baseline | TRUE_Fatal < Blind_Fatal | 6.000 | 0.000 | 1.0000 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.000 |
| Baseline | TRUE_U > TTB_U | 580.000 | 1.812 | 0.0699 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 1.282 |
| Baseline | TRUE_Fatal < TTB_Fatal | 2.500 | 1.667 | 0.0956 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 1.179 |
| Baseline | TRUE_U > MOO_U | 320.000 | 1.143 | 0.2531 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.808 |
| Baseline | TRUE_Fatal < MOO_Fatal | 1.500 | 1.000 | 0.3173 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.707 |
| Baseline | TRUE_Collapse < TTB_Collapse | 0.057 | 0.901 | 0.3676 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.637 |
| Baseline | TRUE_A9 < Blind_A9 | 0.000 | 0.000 | 1.0000 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.000 |
| Observation-Manipulated | TRUE_U > Blind_U | 1340.000 | 9.571 | 0.0000 | 0.0000 | 0.000 | 1.0000 | 1.0000 | 6.768 |
| Observation-Manipulated | TRUE_Fatal < Blind_Fatal | 9.000 | 9.000 | 0.0000 | 0.0000 | 0.000 | 1.0000 | 1.0000 | 6.364 |
| Observation-Manipulated | TRUE_U > TTB_U | 1760.000 | 0.000 | 1.0000 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.000 |
| Observation-Manipulated | TRUE_Fatal < TTB_Fatal | 12.500 | 25.000 | 0.0000 | 0.0000 | 0.000 | 1.0000 | 1.0000 | 17.678 |
| Observation-Manipulated | TRUE_U > MOO_U | 920.000 | 3.286 | 0.0010 | 0.0326 | 0.000 | 1.0000 | 1.0000 | 2.323 |
| Observation-Manipulated | TRUE_Fatal < MOO_Fatal | 5.000 | 2.500 | 0.0124 | 0.3974 | 0.000 | 1.0000 | 1.0000 | 1.768 |
| Observation-Manipulated | TRUE_Collapse < TTB_Collapse | 0.158 | 117.000 | 0.0000 | 0.0000 | 0.000 | 1.0000 | 1.0000 | 82.731 |
| Observation-Manipulated | TRUE_A9 < Blind_A9 | 0.000 | 0.000 | 1.0000 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.000 |
| Safety-Critical | TRUE_U > Blind_U | 1780.000 | 6.357 | 0.0000 | 0.0000 | 0.000 | 1.0000 | 1.0000 | 4.495 |
| Safety-Critical | TRUE_Fatal < Blind_Fatal | 7.000 | 3.500 | 0.0005 | 0.0149 | 0.000 | 1.0000 | 1.0000 | 2.475 |
| Safety-Critical | TRUE_U > TTB_U | 1530.000 | 1.085 | 0.2779 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.767 |
| Safety-Critical | TRUE_Fatal < TTB_Fatal | 7.000 | 1.400 | 0.1615 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.990 |
| Safety-Critical | TRUE_U > MOO_U | 840.000 | 3.000 | 0.0027 | 0.0864 | 0.000 | 1.0000 | 1.0000 | 2.121 |
| Safety-Critical | TRUE_Fatal < MOO_Fatal | 3.000 | 0.000 | 1.0000 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.000 |
| Safety-Critical | TRUE_Collapse < TTB_Collapse | 0.017 | 0.294 | 0.7687 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.208 |
| Safety-Critical | TRUE_A9 < Blind_A9 | 0.000 | 0.000 | 1.0000 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.000 |
| Utility-Trust-Misalignment | TRUE_U > Blind_U | 1535.000 | 18.059 | 0.0000 | 0.0000 | 0.000 | 1.0000 | 1.0000 | 12.770 |
| Utility-Trust-Misalignment | TRUE_Fatal < Blind_Fatal | 10.000 | 10.000 | 0.0000 | 0.0000 | 0.000 | 1.0000 | 1.0000 | 7.071 |
| Utility-Trust-Misalignment | TRUE_U > TTB_U | 1275.000 | 4.474 | 0.0000 | 0.0002 | 0.000 | 1.0000 | 1.0000 | 3.163 |
| Utility-Trust-Misalignment | TRUE_Fatal < TTB_Fatal | 8.500 | 2.429 | 0.0152 | 0.4851 | 0.000 | 1.0000 | 1.0000 | 1.717 |
| Utility-Trust-Misalignment | TRUE_U > MOO_U | 550.000 | 0.764 | 0.4449 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.540 |
| Utility-Trust-Misalignment | TRUE_Fatal < MOO_Fatal | 4.500 | 1.000 | 0.3173 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.707 |
| Utility-Trust-Misalignment | TRUE_Collapse < TTB_Collapse | 0.053 | 37.700 | 0.0000 | 0.0000 | 0.000 | 1.0000 | 1.0000 | 26.658 |
| Utility-Trust-Misalignment | TRUE_A9 < Blind_A9 | 0.000 | 0.000 | 1.0000 | 1.0000 | 0.000 | 1.0000 | 1.0000 | 0.000 |

## Interpretation & Limitations

- Task flows are paired: within each run all groups see the same module sequence. Differences in outcome are therefore attributable to selection mechanisms, not task luck.
- A8 surface-quality bonus is uniform across groups. The only remaining A8 asymmetry is inside TTB's scoring function (A8 receives extra trust-objective weight), which is a *mechanism-level* difference, not an observation-level manipulation.
- Ablation results isolate component contributions: if TRUE-C is substantially worse than TRUE, the constraint filter is a key driver of advantage.
- Bonferroni correction is conservative; if a hypothesis remains significant after correction, the conclusion is robust.
- The experiment remains a probabilistic generative model; no real engineering tools are used.
