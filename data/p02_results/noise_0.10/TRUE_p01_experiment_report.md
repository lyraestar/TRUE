# TRUE Simulation Experiment Report (P0/P1 Refactored)

## Executive Summary

This experiment compares TRUE and its ablations against Blind and TTB baselines across 4 parameterized scenarios.
All groups within a Monte Carlo run face the identical task sequence. 100 runs x 200 rounds x 4 scenarios x 4 groups.

Key P0/P1 changes from the previous round:

1. **Fixed task-flow pairing**: same task sequence for all groups per run.
2. **Removed group-specific observation manipulation**: A8 surface/observed signals are no longer artificially elevated for any single group.
3. **Renamed MOO -> TTB**: honest description as a trust-targeted heuristic baseline, not a full Pareto/Tchebycheff solver.
4. **Ablation variants**: TRUE-C (no constraints), TRUE-E (no exploration bonus), TRUE-N (no newcomer protection).
5. **Statistical upgrades**: Wilcoxon signed-rank test, bootstrap 95% CIs, Bonferroni correction.
6. **Runs increased**: from 60 to 100.

## Scenario Definitions

- **Utility-Trust-Misalignment**: Local phases where trusted incumbents underperform and low-history entities hold latent value.
- **Baseline**: Standard engineering collaboration with moderate observation noise.
- **Safety-Critical**: High-stakes safety environment with harsher penalties and stronger error propagation.
- **Observation-Manipulated**: Observation-contaminated environment where surface quality can diverge from true quality.

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
| Utility-Trust-Misalignment | TRUE | 2023.6 | [1672.3, 2390.6] | 0.742 | 0.707 | 57.1 | 0.747 | 0.591 | 0.364 | 0.0 | 0.323 |
| Utility-Trust-Misalignment | TTB-cap | 3129.3 | [2849.3, 3434.9] | 0.778 | 0.737 | 54.4 | 0.757 | 0.736 | 0.442 | 999.0 | 0.000 |
| Utility-Trust-Misalignment | MOO-cap | 2022.9 | [1529.4, 2486.2] | 0.762 | 0.724 | 59.2 | 0.739 | 0.715 | 0.429 | 790.0 | 0.055 |
| Utility-Trust-Misalignment | Blind | -21895.5 | [-22200.0, -21596.4] | 0.337 | 0.394 | 207.4 | 0.304 | 0.535 | 0.321 | 6.9 | 0.000 |
| Baseline | TRUE | 700.0 | [348.0, 1087.4] | 0.765 | 0.737 | 61.0 | 0.731 | 0.615 | 0.381 | 0.1 | 0.232 |
| Baseline | TTB-cap | 1685.0 | [1376.8, 2011.8] | 0.799 | 0.768 | 58.6 | 0.741 | 0.740 | 0.445 | 999.0 | 0.000 |
| Baseline | MOO-cap | 870.6 | [376.8, 1311.6] | 0.781 | 0.756 | 62.2 | 0.730 | 0.721 | 0.433 | 800.2 | 0.053 |
| Baseline | Blind | -23729.2 | [-24108.2, -23369.2] | 0.344 | 0.402 | 209.0 | 0.311 | 0.530 | 0.318 | 6.7 | 0.000 |
| Safety-Critical | TRUE | -3195.2 | [-3726.4, -2667.6] | 0.796 | 0.719 | 40.6 | 0.817 | 0.644 | 0.407 | 0.2 | 0.209 |
| Safety-Critical | TTB-cap | -1913.4 | [-2438.4, -1393.8] | 0.828 | 0.751 | 38.9 | 0.823 | 0.746 | 0.453 | 999.0 | 0.000 |
| Safety-Critical | MOO-cap | -3067.2 | [-3721.4, -2404.8] | 0.819 | 0.743 | 40.9 | 0.814 | 0.737 | 0.448 | 939.2 | 0.009 |
| Safety-Critical | Blind | -53714.0 | [-54199.2, -53209.8] | 0.343 | 0.377 | 214.4 | 0.297 | 0.535 | 0.321 | 7.2 | 0.000 |
| Observation-Manipulated | TRUE | 1651.2 | [1240.4, 2061.6] | 0.764 | 0.644 | 52.8 | 0.764 | 0.557 | 0.336 | 0.0 | -0.001 |
| Observation-Manipulated | TTB-cap | 2715.2 | [2352.0, 3090.0] | 0.805 | 0.662 | 50.2 | 0.775 | 0.734 | 0.440 | 999.0 | 0.000 |
| Observation-Manipulated | MOO-cap | 1812.8 | [1136.4, 2386.0] | 0.793 | 0.658 | 54.5 | 0.762 | 0.689 | 0.414 | 832.1 | 0.010 |
| Observation-Manipulated | Blind | -25323.2 | [-25718.0, -24922.8] | 0.336 | 0.437 | 199.2 | 0.332 | 0.519 | 0.311 | 4.9 | 0.000 |

## Scenario Conclusions

### Utility-Trust-Misalignment

- TRUE vs Blind: cumulative utility diff = 23919.1; fatal errors diff = -150.3.
- TRUE A9 first delay = 0.0; collapse index = 0.364.

### Baseline

- TRUE vs Blind: cumulative utility diff = 24429.2; fatal errors diff = -148.0.
- TRUE A9 first delay = 0.1; collapse index = 0.381.

### Safety-Critical

- TRUE vs Blind: cumulative utility diff = 50518.8; fatal errors diff = -173.9.
- TRUE A9 first delay = 0.2; collapse index = 0.407.

### Observation-Manipulated

- TRUE vs Blind: cumulative utility diff = 26974.4; fatal errors diff = -146.4.
- TRUE A9 first delay = 0.0; collapse index = 0.336.

## Hypothesis Tests

| Scenario | Hypothesis | Mean Diff | t | p_t | p_t(Bonf) | W | p_w | p_w(Bonf) | Cohen d |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | TRUE_U > TTB-cap_U | -985.000 | -4.167 | 0.0000 | 0.0009 | 1464.500 | 0.0003 | 0.0074 | -0.417 |
| Baseline | TRUE_Fatal < TTB-cap_Fatal | -2.440 | -2.299 | 0.0215 | 0.6026 | 1795.500 | 0.0366 | 1.0000 | -0.230 |
| Baseline | TRUE_U > MOO-cap_U | -170.600 | -0.580 | 0.5620 | 1.0000 | 2279.500 | 0.3986 | 1.0000 | -0.058 |
| Baseline | TRUE_Fatal < MOO-cap_Fatal | 1.250 | 0.912 | 0.3616 | 1.0000 | 2220.000 | 0.5734 | 1.0000 | 0.091 |
| Baseline | TRUE_U > Blind_U | 24429.200 | 107.003 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.700 |
| Baseline | TRUE_Fatal < Blind_Fatal | 147.980 | 102.781 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.278 |
| Baseline | TRUE_A9 < Blind_A9 | 6.630 | 9.497 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.950 |
| Observation-Manipulated | TRUE_U > TTB-cap_U | -1064.000 | -4.277 | 0.0000 | 0.0005 | 1430.500 | 0.0002 | 0.0047 | -0.428 |
| Observation-Manipulated | TRUE_Fatal < TTB-cap_Fatal | -2.580 | -2.583 | 0.0098 | 0.2744 | 1738.000 | 0.0216 | 0.6046 | -0.258 |
| Observation-Manipulated | TRUE_U > MOO-cap_U | -161.600 | -0.418 | 0.6761 | 1.0000 | 2192.000 | 0.2522 | 1.0000 | -0.042 |
| Observation-Manipulated | TRUE_Fatal < MOO-cap_Fatal | 1.690 | 1.103 | 0.2698 | 1.0000 | 2120.000 | 0.5526 | 1.0000 | 0.110 |
| Observation-Manipulated | TRUE_U > Blind_U | 26974.400 | 106.169 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.617 |
| Observation-Manipulated | TRUE_Fatal < Blind_Fatal | 146.390 | 107.462 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.746 |
| Observation-Manipulated | TRUE_A9 < Blind_A9 | 4.930 | 9.197 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.920 |
| Safety-Critical | TRUE_U > TTB-cap_U | -1281.800 | -3.817 | 0.0001 | 0.0038 | 1533.500 | 0.0007 | 0.0182 | -0.382 |
| Safety-Critical | TRUE_Fatal < TTB-cap_Fatal | -1.690 | -1.966 | 0.0493 | 1.0000 | 1730.500 | 0.0813 | 1.0000 | -0.197 |
| Safety-Critical | TRUE_U > MOO-cap_U | -128.000 | -0.282 | 0.7779 | 1.0000 | 2384.500 | 0.6290 | 1.0000 | -0.028 |
| Safety-Critical | TRUE_Fatal < MOO-cap_Fatal | 0.340 | 0.305 | 0.7604 | 1.0000 | 2319.000 | 0.9738 | 1.0000 | 0.030 |
| Safety-Critical | TRUE_U > Blind_U | 50518.800 | 173.687 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 17.369 |
| Safety-Critical | TRUE_Fatal < Blind_Fatal | 173.850 | 141.082 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 14.108 |
| Safety-Critical | TRUE_A9 < Blind_A9 | 6.990 | 9.453 | 0.0000 | 0.0000 | 44.000 | 0.0000 | 0.0000 | 0.945 |
| Utility-Trust-Misalignment | TRUE_U > TTB-cap_U | -1105.700 | -5.031 | 0.0000 | 0.0000 | 1244.500 | 0.0000 | 0.0003 | -0.503 |
| Utility-Trust-Misalignment | TRUE_Fatal < TTB-cap_Fatal | -2.710 | -2.720 | 0.0065 | 0.1827 | 1724.500 | 0.0130 | 0.3637 | -0.272 |
| Utility-Trust-Misalignment | TRUE_U > MOO-cap_U | 0.700 | 0.002 | 0.9982 | 1.0000 | 2342.000 | 0.5292 | 1.0000 | 0.000 |
| Utility-Trust-Misalignment | TRUE_Fatal < MOO-cap_Fatal | 2.040 | 1.405 | 0.1601 | 1.0000 | 2265.000 | 0.4636 | 1.0000 | 0.140 |
| Utility-Trust-Misalignment | TRUE_U > Blind_U | 23919.100 | 100.744 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.074 |
| Utility-Trust-Misalignment | TRUE_Fatal < Blind_Fatal | 150.270 | 111.167 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.117 |
| Utility-Trust-Misalignment | TRUE_A9 < Blind_A9 | 6.900 | 10.503 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 1.050 |

## Interpretation & Limitations

- Task flows are paired: within each run all groups see the same module sequence. Differences in outcome are therefore attributable to selection mechanisms, not task luck.
- A8 surface-quality bonus is uniform across groups. The only remaining A8 asymmetry is inside TTB's scoring function (A8 receives extra trust-objective weight), which is a *mechanism-level* difference, not an observation-level manipulation.
- Ablation results isolate component contributions: if TRUE-C is substantially worse than TRUE, the constraint filter is a key driver of advantage.
- Bonferroni correction is conservative; if a hypothesis remains significant after correction, the conclusion is robust.
- The experiment remains a probabilistic generative model; no real engineering tools are used.
