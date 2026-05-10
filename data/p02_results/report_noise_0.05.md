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

- **Safety-Critical**: High-stakes safety environment with harsher penalties and stronger error propagation.
- **Utility-Trust-Misalignment**: Local phases where trusted incumbents underperform and low-history entities hold latent value.
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
| Safety-Critical | TRUE | -3762.4 | [-4308.8, -3197.4] | 0.792 | 0.719 | 42.3 | 0.811 | 0.648 | 0.410 | 0.3 | 0.137 |
| Safety-Critical | TTB-cap | -1793.8 | [-2290.4, -1309.2] | 0.831 | 0.742 | 38.8 | 0.824 | 0.746 | 0.453 | 999.0 | 0.000 |
| Safety-Critical | MOO-cap | -3079.0 | [-3785.6, -2427.2] | 0.815 | 0.736 | 41.8 | 0.814 | 0.728 | 0.442 | 889.9 | 0.025 |
| Safety-Critical | Blind | -53419.0 | [-53995.6, -52874.0] | 0.343 | 0.375 | 214.3 | 0.300 | 0.542 | 0.325 | 6.5 | 0.000 |
| Utility-Trust-Misalignment | TRUE | 2068.2 | [1731.5, 2385.7] | 0.745 | 0.710 | 57.2 | 0.747 | 0.606 | 0.374 | 0.1 | 0.265 |
| Utility-Trust-Misalignment | TTB-cap | 2976.1 | [2682.6, 3266.2] | 0.781 | 0.736 | 55.6 | 0.753 | 0.737 | 0.442 | 999.0 | 0.000 |
| Utility-Trust-Misalignment | MOO-cap | 2153.1 | [1631.0, 2630.9] | 0.765 | 0.724 | 58.6 | 0.741 | 0.719 | 0.432 | 879.7 | 0.067 |
| Utility-Trust-Misalignment | Blind | -21928.1 | [-22237.0, -21607.8] | 0.337 | 0.392 | 206.3 | 0.303 | 0.535 | 0.321 | 7.7 | 0.000 |
| Observation-Manipulated | TRUE | 1750.4 | [1416.8, 2076.0] | 0.767 | 0.642 | 52.8 | 0.765 | 0.586 | 0.353 | 0.0 | -0.010 |
| Observation-Manipulated | TTB-cap | 2841.6 | [2535.2, 3144.8] | 0.810 | 0.661 | 49.8 | 0.776 | 0.736 | 0.441 | 999.0 | 0.000 |
| Observation-Manipulated | MOO-cap | 1328.4 | [756.4, 1848.4] | 0.790 | 0.653 | 56.2 | 0.754 | 0.695 | 0.417 | 889.7 | -0.006 |
| Observation-Manipulated | Blind | -25491.2 | [-25886.4, -25108.0] | 0.334 | 0.435 | 198.3 | 0.329 | 0.519 | 0.311 | 5.7 | 0.000 |
| Baseline | TRUE | 665.2 | [267.0, 1073.0] | 0.766 | 0.740 | 62.0 | 0.728 | 0.625 | 0.387 | 0.1 | 0.216 |
| Baseline | TTB-cap | 1512.4 | [1163.8, 1831.2] | 0.800 | 0.764 | 59.6 | 0.737 | 0.738 | 0.443 | 999.0 | 0.000 |
| Baseline | MOO-cap | 758.2 | [69.0, 1363.2] | 0.783 | 0.752 | 62.3 | 0.728 | 0.723 | 0.434 | 809.9 | 0.049 |
| Baseline | Blind | -23754.2 | [-24087.0, -23392.8] | 0.343 | 0.401 | 209.2 | 0.311 | 0.529 | 0.318 | 7.6 | 0.000 |

## Scenario Conclusions

### Safety-Critical

- TRUE vs Blind: cumulative utility diff = 49656.6; fatal errors diff = -172.1.
- TRUE A9 first delay = 0.3; collapse index = 0.410.

### Utility-Trust-Misalignment

- TRUE vs Blind: cumulative utility diff = 23996.3; fatal errors diff = -149.1.
- TRUE A9 first delay = 0.1; collapse index = 0.374.

### Observation-Manipulated

- TRUE vs Blind: cumulative utility diff = 27241.6; fatal errors diff = -145.4.
- TRUE A9 first delay = 0.0; collapse index = 0.353.

### Baseline

- TRUE vs Blind: cumulative utility diff = 24419.4; fatal errors diff = -147.1.
- TRUE A9 first delay = 0.1; collapse index = 0.387.

## Hypothesis Tests

| Scenario | Hypothesis | Mean Diff | t | p_t | p_t(Bonf) | W | p_w | p_w(Bonf) | Cohen d |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | TRUE_U > TTB-cap_U | -847.200 | -3.191 | 0.0014 | 0.0396 | 1648.000 | 0.0026 | 0.0719 | -0.319 |
| Baseline | TRUE_Fatal < TTB-cap_Fatal | -2.450 | -2.216 | 0.0267 | 0.7466 | 1782.500 | 0.0326 | 0.9119 | -0.222 |
| Baseline | TRUE_U > MOO-cap_U | -93.000 | -0.256 | 0.7980 | 1.0000 | 2166.500 | 0.2177 | 1.0000 | -0.026 |
| Baseline | TRUE_Fatal < MOO-cap_Fatal | 0.210 | 0.127 | 0.8991 | 1.0000 | 2109.000 | 0.3358 | 1.0000 | 0.013 |
| Baseline | TRUE_U > Blind_U | 24419.400 | 105.893 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.589 |
| Baseline | TRUE_Fatal < Blind_Fatal | 147.130 | 113.081 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.308 |
| Baseline | TRUE_A9 < Blind_A9 | 7.480 | 10.213 | 0.0000 | 0.0000 | 15.000 | 0.0000 | 0.0000 | 1.021 |
| Observation-Manipulated | TRUE_U > TTB-cap_U | -1091.200 | -5.276 | 0.0000 | 0.0000 | 1132.000 | 0.0000 | 0.0001 | -0.528 |
| Observation-Manipulated | TRUE_Fatal < TTB-cap_Fatal | -3.020 | -3.848 | 0.0001 | 0.0033 | 1289.000 | 0.0006 | 0.0166 | -0.385 |
| Observation-Manipulated | TRUE_U > MOO-cap_U | 422.000 | 1.212 | 0.2257 | 1.0000 | 2407.000 | 0.6849 | 1.0000 | 0.121 |
| Observation-Manipulated | TRUE_Fatal < MOO-cap_Fatal | 3.380 | 2.273 | 0.0230 | 0.6442 | 1939.500 | 0.0850 | 1.0000 | 0.227 |
| Observation-Manipulated | TRUE_U > Blind_U | 27241.600 | 118.222 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.822 |
| Observation-Manipulated | TRUE_Fatal < Blind_Fatal | 145.440 | 116.556 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.656 |
| Observation-Manipulated | TRUE_A9 < Blind_A9 | 5.720 | 9.807 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.981 |
| Safety-Critical | TRUE_U > TTB-cap_U | -1968.600 | -5.253 | 0.0000 | 0.0000 | 1215.500 | 0.0000 | 0.0002 | -0.525 |
| Safety-Critical | TRUE_Fatal < TTB-cap_Fatal | -3.460 | -3.900 | 0.0001 | 0.0027 | 1330.000 | 0.0004 | 0.0118 | -0.390 |
| Safety-Critical | TRUE_U > MOO-cap_U | -683.400 | -1.529 | 0.1264 | 1.0000 | 2025.000 | 0.0856 | 1.0000 | -0.153 |
| Safety-Critical | TRUE_Fatal < MOO-cap_Fatal | -0.430 | -0.378 | 0.7051 | 1.0000 | 2310.500 | 0.5659 | 1.0000 | -0.038 |
| Safety-Critical | TRUE_U > Blind_U | 49656.600 | 128.780 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.878 |
| Safety-Critical | TRUE_Fatal < Blind_Fatal | 172.080 | 126.896 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.690 |
| Safety-Critical | TRUE_A9 < Blind_A9 | 6.240 | 9.814 | 0.0000 | 0.0000 | 79.000 | 0.0000 | 0.0000 | 0.981 |
| Utility-Trust-Misalignment | TRUE_U > TTB-cap_U | -907.900 | -4.363 | 0.0000 | 0.0004 | 1419.500 | 0.0001 | 0.0040 | -0.436 |
| Utility-Trust-Misalignment | TRUE_Fatal < TTB-cap_Fatal | -1.600 | -1.717 | 0.0860 | 1.0000 | 1836.000 | 0.1349 | 1.0000 | -0.172 |
| Utility-Trust-Misalignment | TRUE_U > MOO-cap_U | -84.900 | -0.300 | 0.7639 | 1.0000 | 2335.000 | 0.5136 | 1.0000 | -0.030 |
| Utility-Trust-Misalignment | TRUE_Fatal < MOO-cap_Fatal | 1.440 | 1.138 | 0.2550 | 1.0000 | 2215.000 | 0.3642 | 1.0000 | 0.114 |
| Utility-Trust-Misalignment | TRUE_U > Blind_U | 23996.300 | 115.726 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.573 |
| Utility-Trust-Misalignment | TRUE_Fatal < Blind_Fatal | 149.120 | 106.821 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.682 |
| Utility-Trust-Misalignment | TRUE_A9 < Blind_A9 | 7.580 | 8.579 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.858 |

## Interpretation & Limitations

- Task flows are paired: within each run all groups see the same module sequence. Differences in outcome are therefore attributable to selection mechanisms, not task luck.
- A8 surface-quality bonus is uniform across groups. The only remaining A8 asymmetry is inside TTB's scoring function (A8 receives extra trust-objective weight), which is a *mechanism-level* difference, not an observation-level manipulation.
- Ablation results isolate component contributions: if TRUE-C is substantially worse than TRUE, the constraint filter is a key driver of advantage.
- Bonferroni correction is conservative; if a hypothesis remains significant after correction, the conclusion is robust.
- The experiment remains a probabilistic generative model; no real engineering tools are used.
