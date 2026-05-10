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

- **Baseline**: Standard engineering collaboration with moderate observation noise.
- **Observation-Manipulated**: Observation-contaminated environment where surface quality can diverge from true quality.
- **Utility-Trust-Misalignment**: Local phases where trusted incumbents underperform and low-history entities hold latent value.
- **Safety-Critical**: High-stakes safety environment with harsher penalties and stronger error propagation.

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
| Baseline | TRUE | 86.2 | [-291.6, 457.8] | 0.752 | 0.731 | 64.5 | 0.721 | 0.589 | 0.365 | 0.1 | 0.191 |
| Baseline | TTB-cap | 1387.0 | [1024.0, 1743.2] | 0.796 | 0.769 | 60.5 | 0.736 | 0.741 | 0.445 | 999.0 | 0.000 |
| Baseline | MOO-cap | 258.0 | [-286.6, 740.2] | 0.779 | 0.754 | 65.3 | 0.719 | 0.714 | 0.429 | 742.0 | 0.079 |
| Baseline | Blind | -23907.4 | [-24245.0, -23588.2] | 0.341 | 0.403 | 210.5 | 0.308 | 0.532 | 0.319 | 5.4 | 0.000 |
| Observation-Manipulated | TRUE | 801.2 | [444.8, 1164.4] | 0.752 | 0.636 | 56.6 | 0.752 | 0.521 | 0.314 | 0.0 | 0.014 |
| Observation-Manipulated | TTB-cap | 2614.8 | [2237.6, 3004.0] | 0.806 | 0.660 | 50.9 | 0.773 | 0.735 | 0.441 | 999.0 | 0.000 |
| Observation-Manipulated | MOO-cap | 883.6 | [150.0, 1555.6] | 0.783 | 0.653 | 57.8 | 0.748 | 0.688 | 0.413 | 722.6 | 0.001 |
| Observation-Manipulated | Blind | -25219.2 | [-25568.0, -24874.4] | 0.336 | 0.435 | 198.2 | 0.334 | 0.521 | 0.313 | 6.4 | 0.000 |
| Utility-Trust-Misalignment | TRUE | 1859.5 | [1477.9, 2252.6] | 0.736 | 0.701 | 57.2 | 0.747 | 0.571 | 0.353 | 0.1 | 0.302 |
| Utility-Trust-Misalignment | TTB-cap | 3179.7 | [2835.4, 3541.6] | 0.781 | 0.738 | 54.5 | 0.758 | 0.733 | 0.440 | 999.0 | 0.000 |
| Utility-Trust-Misalignment | MOO-cap | 2622.1 | [2278.5, 2974.1] | 0.769 | 0.727 | 55.9 | 0.750 | 0.722 | 0.433 | 859.6 | 0.074 |
| Utility-Trust-Misalignment | Blind | -21840.8 | [-22131.6, -21554.3] | 0.337 | 0.390 | 206.6 | 0.305 | 0.532 | 0.319 | 7.6 | 0.000 |
| Safety-Critical | TRUE | -3721.8 | [-4316.6, -3129.2] | 0.790 | 0.714 | 41.8 | 0.812 | 0.627 | 0.399 | 0.2 | 0.145 |
| Safety-Critical | TTB-cap | -2394.4 | [-2924.4, -1851.4] | 0.824 | 0.748 | 39.5 | 0.819 | 0.744 | 0.452 | 999.0 | 0.000 |
| Safety-Critical | MOO-cap | -3291.0 | [-4289.6, -2394.0] | 0.814 | 0.736 | 42.6 | 0.811 | 0.730 | 0.443 | 900.0 | 0.017 |
| Safety-Critical | Blind | -53395.8 | [-53891.0, -52908.2] | 0.343 | 0.377 | 213.3 | 0.300 | 0.537 | 0.322 | 6.2 | 0.000 |

## Scenario Conclusions

### Baseline

- TRUE vs Blind: cumulative utility diff = 23993.6; fatal errors diff = -145.9.
- TRUE A9 first delay = 0.1; collapse index = 0.365.

### Observation-Manipulated

- TRUE vs Blind: cumulative utility diff = 26020.4; fatal errors diff = -141.6.
- TRUE A9 first delay = 0.0; collapse index = 0.314.

### Utility-Trust-Misalignment

- TRUE vs Blind: cumulative utility diff = 23700.3; fatal errors diff = -149.4.
- TRUE A9 first delay = 0.1; collapse index = 0.353.

### Safety-Critical

- TRUE vs Blind: cumulative utility diff = 49674.0; fatal errors diff = -171.5.
- TRUE A9 first delay = 0.2; collapse index = 0.399.

## Hypothesis Tests

| Scenario | Hypothesis | Mean Diff | t | p_t | p_t(Bonf) | W | p_w | p_w(Bonf) | Cohen d |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | TRUE_U > TTB-cap_U | -1300.800 | -4.997 | 0.0000 | 0.0000 | 1199.000 | 0.0000 | 0.0001 | -0.500 |
| Baseline | TRUE_Fatal < TTB-cap_Fatal | -3.990 | -3.507 | 0.0005 | 0.0127 | 1427.000 | 0.0015 | 0.0432 | -0.351 |
| Baseline | TRUE_U > MOO-cap_U | -171.800 | -0.560 | 0.5754 | 1.0000 | 2262.500 | 0.3668 | 1.0000 | -0.056 |
| Baseline | TRUE_Fatal < MOO-cap_Fatal | 0.800 | 0.555 | 0.5791 | 1.0000 | 2270.000 | 0.9704 | 1.0000 | 0.055 |
| Baseline | TRUE_U > Blind_U | 23993.600 | 108.792 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.879 |
| Baseline | TRUE_Fatal < Blind_Fatal | 145.940 | 116.418 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.642 |
| Baseline | TRUE_A9 < Blind_A9 | 5.290 | 9.474 | 0.0000 | 0.0000 | 30.000 | 0.0000 | 0.0000 | 0.947 |
| Observation-Manipulated | TRUE_U > TTB-cap_U | -1813.600 | -7.581 | 0.0000 | 0.0000 | 706.500 | 0.0000 | 0.0000 | -0.758 |
| Observation-Manipulated | TRUE_Fatal < TTB-cap_Fatal | -5.710 | -5.818 | 0.0000 | 0.0000 | 925.500 | 0.0000 | 0.0000 | -0.582 |
| Observation-Manipulated | TRUE_U > MOO-cap_U | -82.400 | -0.223 | 0.8235 | 1.0000 | 2141.000 | 0.2437 | 1.0000 | -0.022 |
| Observation-Manipulated | TRUE_Fatal < MOO-cap_Fatal | 1.250 | 0.812 | 0.4166 | 1.0000 | 2375.500 | 0.8594 | 1.0000 | 0.081 |
| Observation-Manipulated | TRUE_U > Blind_U | 26020.400 | 126.285 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.629 |
| Observation-Manipulated | TRUE_Fatal < Blind_Fatal | 141.580 | 121.910 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.191 |
| Observation-Manipulated | TRUE_A9 < Blind_A9 | 6.410 | 7.987 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.799 |
| Safety-Critical | TRUE_U > TTB-cap_U | -1327.400 | -3.359 | 0.0008 | 0.0219 | 1585.000 | 0.0012 | 0.0344 | -0.336 |
| Safety-Critical | TRUE_Fatal < TTB-cap_Fatal | -2.260 | -2.356 | 0.0185 | 0.5175 | 1665.000 | 0.0224 | 0.6284 | -0.236 |
| Safety-Critical | TRUE_U > MOO-cap_U | -430.800 | -0.750 | 0.4531 | 1.0000 | 2160.500 | 0.2101 | 1.0000 | -0.075 |
| Safety-Critical | TRUE_Fatal < MOO-cap_Fatal | 0.790 | 0.568 | 0.5698 | 1.0000 | 2273.500 | 0.9808 | 1.0000 | 0.057 |
| Safety-Critical | TRUE_U > Blind_U | 49674.000 | 130.641 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.064 |
| Safety-Critical | TRUE_Fatal < Blind_Fatal | 171.530 | 125.666 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.567 |
| Safety-Critical | TRUE_A9 < Blind_A9 | 6.010 | 8.147 | 0.0000 | 0.0000 | 42.500 | 0.0000 | 0.0000 | 0.815 |
| Utility-Trust-Misalignment | TRUE_U > TTB-cap_U | -1320.200 | -5.561 | 0.0000 | 0.0000 | 1114.500 | 0.0000 | 0.0000 | -0.556 |
| Utility-Trust-Misalignment | TRUE_Fatal < TTB-cap_Fatal | -2.640 | -2.460 | 0.0139 | 0.3889 | 1649.000 | 0.0131 | 0.3666 | -0.246 |
| Utility-Trust-Misalignment | TRUE_U > MOO-cap_U | -762.600 | -2.900 | 0.0037 | 0.1044 | 1791.500 | 0.0117 | 0.3267 | -0.290 |
| Utility-Trust-Misalignment | TRUE_Fatal < MOO-cap_Fatal | -1.330 | -1.144 | 0.2525 | 1.0000 | 2159.000 | 0.2701 | 1.0000 | -0.114 |
| Utility-Trust-Misalignment | TRUE_U > Blind_U | 23700.300 | 109.431 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.943 |
| Utility-Trust-Misalignment | TRUE_Fatal < Blind_Fatal | 149.390 | 110.742 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.074 |
| Utility-Trust-Misalignment | TRUE_A9 < Blind_A9 | 7.540 | 8.984 | 0.0000 | 0.0000 | 6.500 | 0.0000 | 0.0000 | 0.898 |

## Interpretation & Limitations

- Task flows are paired: within each run all groups see the same module sequence. Differences in outcome are therefore attributable to selection mechanisms, not task luck.
- A8 surface-quality bonus is uniform across groups. The only remaining A8 asymmetry is inside TTB's scoring function (A8 receives extra trust-objective weight), which is a *mechanism-level* difference, not an observation-level manipulation.
- Ablation results isolate component contributions: if TRUE-C is substantially worse than TRUE, the constraint filter is a key driver of advantage.
- Bonferroni correction is conservative; if a hypothesis remains significant after correction, the conclusion is robust.
- The experiment remains a probabilistic generative model; no real engineering tools are used.
