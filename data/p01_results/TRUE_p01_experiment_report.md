# TRUE Simulation Experiment Report (P0/P1 Refactored)

## Executive Summary

This experiment compares TRUE and its ablations against Blind and TTB baselines across 4 parameterized scenarios.
All groups within a Monte Carlo run face the identical task sequence. 100 runs x 200 rounds x 4 scenarios x 7 groups.

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
- **Utility-Trust-Misalignment**: Local phases where trusted incumbents underperform and low-history entities hold latent value.
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
| Baseline | TRUE | 896.8 | [520.4, 1274.0] | 0.767 | 0.739 | 61.0 | 0.733 | 0.637 | 0.394 | 0.2 | 0.293 |
| Baseline | TRUE-C | 1377.6 | [1037.2, 1739.0] | 0.799 | 0.767 | 60.7 | 0.735 | 0.679 | 0.408 | 0.9 | 0.000 |
| Baseline | TRUE-E | 779.2 | [451.0, 1103.0] | 0.765 | 0.737 | 61.0 | 0.731 | 0.639 | 0.396 | 0.2 | 0.214 |
| Baseline | TRUE-N | 1326.0 | [974.4, 1671.8] | 0.798 | 0.766 | 60.5 | 0.734 | 0.702 | 0.422 | 383.9 | 0.000 |
| Baseline | Blind | -23753.6 | [-24089.4, -23428.6] | 0.343 | 0.402 | 208.2 | 0.310 | 0.529 | 0.317 | 6.8 | 0.000 |
| Baseline | TTB | 174.8 | [-289.0, 599.6] | 0.764 | 0.741 | 64.7 | 0.720 | 0.736 | 0.442 | 859.7 | 0.009 |
| Baseline | MOO | -547.4 | [-1097.4, -40.4] | 0.769 | 0.743 | 69.2 | 0.705 | 0.708 | 0.425 | 789.9 | 0.042 |
| Safety-Critical | TRUE | -3079.0 | [-3677.6, -2488.6] | 0.797 | 0.720 | 40.4 | 0.818 | 0.661 | 0.418 | 0.5 | 0.163 |
| Safety-Critical | TRUE-C | -1918.0 | [-2516.0, -1328.2] | 0.831 | 0.746 | 39.1 | 0.823 | 0.688 | 0.420 | 1.1 | 0.000 |
| Safety-Critical | TRUE-E | -2895.4 | [-3402.0, -2418.0] | 0.799 | 0.721 | 39.8 | 0.819 | 0.657 | 0.414 | 0.6 | 0.183 |
| Safety-Critical | TRUE-N | -1590.6 | [-2162.6, -1009.8] | 0.830 | 0.751 | 38.5 | 0.826 | 0.723 | 0.439 | 890.2 | 0.000 |
| Safety-Critical | Blind | -53661.6 | [-54214.6, -53149.4] | 0.347 | 0.379 | 213.7 | 0.298 | 0.541 | 0.324 | 7.7 | 0.000 |
| Safety-Critical | TTB | -5326.2 | [-6808.2, -4138.0] | 0.789 | 0.718 | 45.9 | 0.795 | 0.746 | 0.454 | 780.9 | 0.025 |
| Safety-Critical | MOO | -5473.4 | [-6306.2, -4684.4] | 0.796 | 0.725 | 47.1 | 0.791 | 0.713 | 0.434 | 809.9 | 0.033 |
| Utility-Trust-Misalignment | TRUE | 2345.4 | [2040.2, 2640.5] | 0.749 | 0.705 | 56.1 | 0.752 | 0.619 | 0.381 | 0.1 | 0.257 |
| Utility-Trust-Misalignment | TRUE-C | 2954.1 | [2640.3, 3284.8] | 0.782 | 0.735 | 55.6 | 0.752 | 0.659 | 0.396 | 0.7 | 0.000 |
| Utility-Trust-Misalignment | TRUE-E | 2473.9 | [2188.1, 2762.3] | 0.748 | 0.710 | 54.9 | 0.755 | 0.621 | 0.384 | 0.3 | 0.258 |
| Utility-Trust-Misalignment | TRUE-N | 3332.8 | [3057.4, 3626.7] | 0.784 | 0.737 | 54.2 | 0.758 | 0.679 | 0.408 | 407.3 | 0.000 |
| Utility-Trust-Misalignment | Blind | -21939.2 | [-22229.4, -21643.8] | 0.335 | 0.393 | 206.9 | 0.303 | 0.533 | 0.320 | 7.3 | 0.000 |
| Utility-Trust-Misalignment | TTB | 934.2 | [74.9, 1645.6] | 0.741 | 0.707 | 62.4 | 0.725 | 0.733 | 0.440 | 799.8 | 0.056 |
| Utility-Trust-Misalignment | MOO | 1442.8 | [865.3, 1954.9] | 0.751 | 0.715 | 62.3 | 0.730 | 0.700 | 0.420 | 771.4 | 0.068 |
| Observation-Manipulated | TRUE | 2342.4 | [1975.2, 2704.8] | 0.772 | 0.644 | 50.4 | 0.774 | 0.606 | 0.365 | 0.0 | -0.011 |
| Observation-Manipulated | TRUE-C | 2600.4 | [2256.0, 2933.6] | 0.806 | 0.653 | 51.1 | 0.773 | 0.657 | 0.394 | 0.7 | 0.000 |
| Observation-Manipulated | TRUE-E | 2111.2 | [1774.0, 2455.2] | 0.769 | 0.645 | 51.8 | 0.770 | 0.612 | 0.368 | 0.0 | -0.032 |
| Observation-Manipulated | TRUE-N | 2894.0 | [2521.6, 3264.0] | 0.810 | 0.659 | 50.5 | 0.776 | 0.664 | 0.399 | 6.0 | 0.000 |
| Observation-Manipulated | Blind | -25392.8 | [-25722.4, -25050.4] | 0.336 | 0.440 | 198.6 | 0.330 | 0.517 | 0.310 | 7.5 | 0.000 |
| Observation-Manipulated | TTB | 359.6 | [-676.0, 1235.2] | 0.754 | 0.634 | 58.4 | 0.744 | 0.739 | 0.444 | 860.6 | 0.001 |
| Observation-Manipulated | MOO | -856.8 | [-1423.6, -334.4] | 0.753 | 0.637 | 65.9 | 0.722 | 0.635 | 0.381 | 517.5 | 0.003 |

## Scenario Conclusions

### Baseline

- TRUE vs Blind: cumulative utility diff = 24650.4; fatal errors diff = -147.2.
- TRUE vs TTB: cumulative utility diff = 722.0; fatal errors diff = -3.7.
- TRUE A9 first delay = 0.2; collapse index = 0.394.

### Safety-Critical

- TRUE vs Blind: cumulative utility diff = 50582.6; fatal errors diff = -173.2.
- TRUE vs TTB: cumulative utility diff = 2247.2; fatal errors diff = -5.5.
- TRUE A9 first delay = 0.5; collapse index = 0.418.

### Utility-Trust-Misalignment

- TRUE vs Blind: cumulative utility diff = 24284.6; fatal errors diff = -150.8.
- TRUE vs TTB: cumulative utility diff = 1411.2; fatal errors diff = -6.3.
- TRUE A9 first delay = 0.1; collapse index = 0.381.

### Observation-Manipulated

- TRUE vs Blind: cumulative utility diff = 27735.2; fatal errors diff = -148.2.
- TRUE vs TTB: cumulative utility diff = 1982.8; fatal errors diff = -8.0.
- TRUE A9 first delay = 0.0; collapse index = 0.365.

## Hypothesis Tests

| Scenario | Hypothesis | Mean Diff | t | p_t | p_t(Bonf) | W | p_w | p_w(Bonf) | Cohen d |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | TRUE_U > Blind_U | 24650.400 | 116.802 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.680 |
| Baseline | TRUE_Fatal < Blind_Fatal | 147.150 | 121.144 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.114 |
| Baseline | TRUE_U > TTB_U | 722.000 | 2.480 | 0.0131 | 1.0000 | 1879.000 | 0.0263 | 1.0000 | 0.248 |
| Baseline | TRUE_Fatal < TTB_Fatal | 3.710 | 2.779 | 0.0055 | 0.6976 | 1740.500 | 0.0104 | 1.0000 | 0.278 |
| Baseline | TRUE_U > MOO_U | 1444.200 | 4.315 | 0.0000 | 0.0020 | 1373.500 | 0.0001 | 0.0096 | 0.431 |
| Baseline | TRUE_Fatal < MOO_Fatal | 8.180 | 5.128 | 0.0000 | 0.0000 | 1097.000 | 0.0000 | 0.0005 | 0.513 |
| Baseline | TRUE_Collapse < TTB_Collapse | 0.048 | 21.074 | 0.0000 | 0.0000 | 9.000 | 0.0000 | 0.0000 | 2.107 |
| Baseline | TRUE_A9 < Blind_A9 | 6.530 | 9.155 | 0.0000 | 0.0000 | 47.000 | 0.0000 | 0.0000 | 0.915 |
| Baseline | TRUE-C_U > Blind_U | 25131.200 | 122.175 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.217 |
| Baseline | TRUE-C_Fatal < Blind_Fatal | 147.420 | 114.162 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.416 |
| Baseline | TRUE-C_U > TTB_U | 1202.800 | 4.605 | 0.0000 | 0.0005 | 1374.500 | 0.0001 | 0.0098 | 0.460 |
| Baseline | TRUE-C_Fatal < TTB_Fatal | 3.980 | 3.372 | 0.0007 | 0.0956 | 1571.000 | 0.0057 | 0.7257 | 0.337 |
| Baseline | TRUE-C_U > MOO_U | 1925.000 | 5.945 | 0.0000 | 0.0000 | 995.500 | 0.0000 | 0.0000 | 0.595 |
| Baseline | TRUE-C_Fatal < MOO_Fatal | 8.450 | 5.502 | 0.0000 | 0.0000 | 937.000 | 0.0000 | 0.0001 | 0.550 |
| Baseline | TRUE-C_Collapse < TTB_Collapse | 0.035 | 19.780 | 0.0000 | 0.0000 | 32.000 | 0.0000 | 0.0000 | 1.978 |
| Baseline | TRUE-C_A9 < Blind_A9 | 5.880 | 7.914 | 0.0000 | 0.0000 | 240.500 | 0.0000 | 0.0000 | 0.791 |
| Baseline | TRUE-E_U > Blind_U | 24532.800 | 128.186 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.819 |
| Baseline | TRUE-E_Fatal < Blind_Fatal | 147.170 | 124.015 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.401 |
| Baseline | TRUE-E_U > TTB_U | 604.400 | 2.309 | 0.0209 | 1.0000 | 2110.500 | 0.2033 | 1.0000 | 0.231 |
| Baseline | TRUE-E_Fatal < TTB_Fatal | 3.730 | 3.101 | 0.0019 | 0.2471 | 1659.500 | 0.0213 | 1.0000 | 0.310 |
| Baseline | TRUE-E_U > MOO_U | 1326.600 | 4.439 | 0.0000 | 0.0012 | 1335.500 | 0.0000 | 0.0055 | 0.444 |
| Baseline | TRUE-E_Fatal < MOO_Fatal | 8.200 | 5.682 | 0.0000 | 0.0000 | 946.000 | 0.0000 | 0.0001 | 0.568 |
| Baseline | TRUE-E_Collapse < TTB_Collapse | 0.046 | 18.883 | 0.0000 | 0.0000 | 6.000 | 0.0000 | 0.0000 | 1.888 |
| Baseline | TRUE-E_A9 < Blind_A9 | 6.560 | 9.236 | 0.0000 | 0.0000 | 13.000 | 0.0000 | 0.0000 | 0.924 |
| Baseline | TRUE-N_U > Blind_U | 25079.600 | 112.232 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.223 |
| Baseline | TRUE-N_Fatal < Blind_Fatal | 147.630 | 107.736 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.774 |
| Baseline | TRUE-N_U > TTB_U | 1151.200 | 4.166 | 0.0000 | 0.0040 | 1314.000 | 0.0001 | 0.0065 | 0.417 |
| Baseline | TRUE-N_Fatal < TTB_Fatal | 4.190 | 3.286 | 0.0010 | 0.1300 | 1470.500 | 0.0011 | 0.1426 | 0.329 |
| Baseline | TRUE-N_U > MOO_U | 1873.400 | 5.956 | 0.0000 | 0.0000 | 1002.500 | 0.0000 | 0.0000 | 0.596 |
| Baseline | TRUE-N_Fatal < MOO_Fatal | 8.660 | 5.810 | 0.0000 | 0.0000 | 1031.000 | 0.0000 | 0.0000 | 0.581 |
| Baseline | TRUE-N_Collapse < TTB_Collapse | 0.020 | 9.411 | 0.0000 | 0.0000 | 400.000 | 0.0000 | 0.0000 | 0.941 |
| Baseline | TRUE-N_A9 < Blind_A9 | -377.150 | -8.126 | 0.0000 | 0.0000 | 274.500 | 0.0000 | 0.0000 | -0.813 |
| Observation-Manipulated | TRUE_U > Blind_U | 27735.200 | 125.991 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.599 |
| Observation-Manipulated | TRUE_Fatal < Blind_Fatal | 148.170 | 123.001 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.300 |
| Observation-Manipulated | TRUE_U > TTB_U | 1982.800 | 3.922 | 0.0001 | 0.0112 | 1381.000 | 0.0001 | 0.0172 | 0.392 |
| Observation-Manipulated | TRUE_Fatal < TTB_Fatal | 8.010 | 3.391 | 0.0007 | 0.0891 | 1404.000 | 0.0011 | 0.1469 | 0.339 |
| Observation-Manipulated | TRUE_U > MOO_U | 3199.200 | 9.846 | 0.0000 | 0.0000 | 400.000 | 0.0000 | 0.0000 | 0.985 |
| Observation-Manipulated | TRUE_Fatal < MOO_Fatal | 15.460 | 10.506 | 0.0000 | 0.0000 | 249.000 | 0.0000 | 0.0000 | 1.051 |
| Observation-Manipulated | TRUE_Collapse < TTB_Collapse | 0.079 | 46.622 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 4.662 |
| Observation-Manipulated | TRUE_A9 < Blind_A9 | 7.470 | 10.591 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 1.059 |
| Observation-Manipulated | TRUE-C_U > Blind_U | 27993.200 | 121.106 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.111 |
| Observation-Manipulated | TRUE-C_Fatal < Blind_Fatal | 147.470 | 117.694 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.769 |
| Observation-Manipulated | TRUE-C_U > TTB_U | 2240.800 | 4.279 | 0.0000 | 0.0024 | 1168.500 | 0.0000 | 0.0004 | 0.428 |
| Observation-Manipulated | TRUE-C_Fatal < TTB_Fatal | 7.310 | 2.969 | 0.0030 | 0.3829 | 1469.500 | 0.0061 | 0.7783 | 0.297 |
| Observation-Manipulated | TRUE-C_U > MOO_U | 3457.200 | 11.671 | 0.0000 | 0.0000 | 160.000 | 0.0000 | 0.0000 | 1.167 |
| Observation-Manipulated | TRUE-C_Fatal < MOO_Fatal | 14.760 | 10.472 | 0.0000 | 0.0000 | 305.500 | 0.0000 | 0.0000 | 1.047 |
| Observation-Manipulated | TRUE-C_Collapse < TTB_Collapse | 0.049 | 27.824 | 0.0000 | 0.0000 | 3.000 | 0.0000 | 0.0000 | 2.782 |
| Observation-Manipulated | TRUE-C_A9 < Blind_A9 | 6.780 | 9.547 | 0.0000 | 0.0000 | 79.500 | 0.0000 | 0.0000 | 0.955 |
| Observation-Manipulated | TRUE-E_U > Blind_U | 27504.000 | 119.069 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.907 |
| Observation-Manipulated | TRUE-E_Fatal < Blind_Fatal | 146.850 | 116.653 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.665 |
| Observation-Manipulated | TRUE-E_U > TTB_U | 1751.600 | 3.307 | 0.0009 | 0.1205 | 1673.000 | 0.0034 | 0.4346 | 0.331 |
| Observation-Manipulated | TRUE-E_Fatal < TTB_Fatal | 6.690 | 2.703 | 0.0069 | 0.8798 | 1738.500 | 0.0444 | 1.0000 | 0.270 |
| Observation-Manipulated | TRUE-E_U > MOO_U | 2968.000 | 9.187 | 0.0000 | 0.0000 | 412.000 | 0.0000 | 0.0000 | 0.919 |
| Observation-Manipulated | TRUE-E_Fatal < MOO_Fatal | 14.140 | 9.620 | 0.0000 | 0.0000 | 388.500 | 0.0000 | 0.0000 | 0.962 |
| Observation-Manipulated | TRUE-E_Collapse < TTB_Collapse | 0.075 | 39.860 | 0.0000 | 0.0000 | 1.000 | 0.0000 | 0.0000 | 3.986 |
| Observation-Manipulated | TRUE-E_A9 < Blind_A9 | 7.460 | 10.573 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 1.057 |
| Observation-Manipulated | TRUE-N_U > Blind_U | 28286.800 | 117.953 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.795 |
| Observation-Manipulated | TRUE-N_Fatal < Blind_Fatal | 148.150 | 114.408 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.441 |
| Observation-Manipulated | TRUE-N_U > TTB_U | 2534.400 | 5.178 | 0.0000 | 0.0000 | 850.500 | 0.0000 | 0.0000 | 0.518 |
| Observation-Manipulated | TRUE-N_Fatal < TTB_Fatal | 7.990 | 3.510 | 0.0004 | 0.0573 | 1245.000 | 0.0001 | 0.0156 | 0.351 |
| Observation-Manipulated | TRUE-N_U > MOO_U | 3750.800 | 11.246 | 0.0000 | 0.0000 | 233.500 | 0.0000 | 0.0000 | 1.125 |
| Observation-Manipulated | TRUE-N_Fatal < MOO_Fatal | 15.440 | 10.277 | 0.0000 | 0.0000 | 281.000 | 0.0000 | 0.0000 | 1.028 |
| Observation-Manipulated | TRUE-N_Collapse < TTB_Collapse | 0.045 | 24.348 | 0.0000 | 0.0000 | 19.000 | 0.0000 | 0.0000 | 2.435 |
| Observation-Manipulated | TRUE-N_A9 < Blind_A9 | 1.520 | 1.253 | 0.2101 | 1.0000 | 1390.000 | 0.0082 | 1.0000 | 0.125 |
| Safety-Critical | TRUE_U > Blind_U | 50582.600 | 153.220 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 15.322 |
| Safety-Critical | TRUE_Fatal < Blind_Fatal | 173.250 | 134.294 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.429 |
| Safety-Critical | TRUE_U > TTB_U | 2247.200 | 2.898 | 0.0038 | 0.4810 | 1680.500 | 0.0056 | 0.7109 | 0.290 |
| Safety-Critical | TRUE_Fatal < TTB_Fatal | 5.490 | 2.811 | 0.0049 | 0.6319 | 1593.500 | 0.0108 | 1.0000 | 0.281 |
| Safety-Critical | TRUE_U > MOO_U | 2394.400 | 4.869 | 0.0000 | 0.0001 | 1190.000 | 0.0000 | 0.0006 | 0.487 |
| Safety-Critical | TRUE_Fatal < MOO_Fatal | 6.710 | 4.936 | 0.0000 | 0.0001 | 1240.500 | 0.0000 | 0.0013 | 0.494 |
| Safety-Critical | TRUE_Collapse < TTB_Collapse | 0.036 | 17.391 | 0.0000 | 0.0000 | 12.000 | 0.0000 | 0.0000 | 1.739 |
| Safety-Critical | TRUE_A9 < Blind_A9 | 7.250 | 9.610 | 0.0000 | 0.0000 | 39.500 | 0.0000 | 0.0000 | 0.961 |
| Safety-Critical | TRUE-C_U > Blind_U | 51743.600 | 131.477 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.148 |
| Safety-Critical | TRUE-C_Fatal < Blind_Fatal | 174.570 | 126.651 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.665 |
| Safety-Critical | TRUE-C_U > TTB_U | 3408.200 | 4.605 | 0.0000 | 0.0005 | 970.000 | 0.0000 | 0.0000 | 0.460 |
| Safety-Critical | TRUE-C_Fatal < TTB_Fatal | 6.810 | 3.766 | 0.0002 | 0.0213 | 1141.000 | 0.0000 | 0.0018 | 0.377 |
| Safety-Critical | TRUE-C_U > MOO_U | 3555.400 | 7.450 | 0.0000 | 0.0000 | 697.000 | 0.0000 | 0.0000 | 0.745 |
| Safety-Critical | TRUE-C_Fatal < MOO_Fatal | 8.030 | 6.393 | 0.0000 | 0.0000 | 805.500 | 0.0000 | 0.0000 | 0.639 |
| Safety-Critical | TRUE-C_Collapse < TTB_Collapse | 0.033 | 19.310 | 0.0000 | 0.0000 | 9.000 | 0.0000 | 0.0000 | 1.931 |
| Safety-Critical | TRUE-C_A9 < Blind_A9 | 6.620 | 8.691 | 0.0000 | 0.0000 | 99.000 | 0.0000 | 0.0000 | 0.869 |
| Safety-Critical | TRUE-E_U > Blind_U | 50766.200 | 155.050 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 15.505 |
| Safety-Critical | TRUE-E_Fatal < Blind_Fatal | 173.840 | 130.021 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.002 |
| Safety-Critical | TRUE-E_U > TTB_U | 2430.800 | 3.500 | 0.0005 | 0.0596 | 1402.500 | 0.0001 | 0.0145 | 0.350 |
| Safety-Critical | TRUE-E_Fatal < TTB_Fatal | 6.080 | 3.469 | 0.0005 | 0.0669 | 1285.500 | 0.0001 | 0.0111 | 0.347 |
| Safety-Critical | TRUE-E_U > MOO_U | 2578.000 | 5.625 | 0.0000 | 0.0000 | 1009.500 | 0.0000 | 0.0000 | 0.563 |
| Safety-Critical | TRUE-E_Fatal < MOO_Fatal | 7.300 | 6.061 | 0.0000 | 0.0000 | 844.500 | 0.0000 | 0.0000 | 0.606 |
| Safety-Critical | TRUE-E_Collapse < TTB_Collapse | 0.039 | 17.592 | 0.0000 | 0.0000 | 3.000 | 0.0000 | 0.0000 | 1.759 |
| Safety-Critical | TRUE-E_A9 < Blind_A9 | 7.140 | 9.382 | 0.0000 | 0.0000 | 39.000 | 0.0000 | 0.0000 | 0.938 |
| Safety-Critical | TRUE-N_U > Blind_U | 52071.000 | 141.024 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 14.102 |
| Safety-Critical | TRUE-N_Fatal < Blind_Fatal | 175.140 | 133.184 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.318 |
| Safety-Critical | TRUE-N_U > TTB_U | 3735.600 | 4.603 | 0.0000 | 0.0005 | 989.500 | 0.0000 | 0.0000 | 0.460 |
| Safety-Critical | TRUE-N_Fatal < TTB_Fatal | 7.380 | 3.686 | 0.0002 | 0.0291 | 1178.500 | 0.0001 | 0.0090 | 0.369 |
| Safety-Critical | TRUE-N_U > MOO_U | 3882.800 | 8.152 | 0.0000 | 0.0000 | 631.000 | 0.0000 | 0.0000 | 0.815 |
| Safety-Critical | TRUE-N_Fatal < MOO_Fatal | 8.600 | 6.896 | 0.0000 | 0.0000 | 729.500 | 0.0000 | 0.0000 | 0.690 |
| Safety-Critical | TRUE-N_Collapse < TTB_Collapse | 0.014 | 7.549 | 0.0000 | 0.0000 | 671.000 | 0.0000 | 0.0000 | 0.755 |
| Safety-Critical | TRUE-N_A9 < Blind_A9 | -882.450 | -28.186 | 0.0000 | 0.0000 | 29.000 | 0.0000 | 0.0000 | -2.819 |
| Utility-Trust-Misalignment | TRUE_U > Blind_U | 24284.600 | 118.415 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.842 |
| Utility-Trust-Misalignment | TRUE_Fatal < Blind_Fatal | 150.750 | 107.400 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.740 |
| Utility-Trust-Misalignment | TRUE_U > TTB_U | 1411.200 | 3.319 | 0.0009 | 0.1158 | 1692.500 | 0.0042 | 0.5382 | 0.332 |
| Utility-Trust-Misalignment | TRUE_Fatal < TTB_Fatal | 6.270 | 3.084 | 0.0020 | 0.2612 | 1721.500 | 0.0126 | 1.0000 | 0.308 |
| Utility-Trust-Misalignment | TRUE_U > MOO_U | 902.600 | 2.971 | 0.0030 | 0.3794 | 1742.500 | 0.0071 | 0.9132 | 0.297 |
| Utility-Trust-Misalignment | TRUE_Fatal < MOO_Fatal | 6.180 | 4.210 | 0.0000 | 0.0033 | 1274.000 | 0.0001 | 0.0093 | 0.421 |
| Utility-Trust-Misalignment | TRUE_Collapse < TTB_Collapse | 0.059 | 23.207 | 0.0000 | 0.0000 | 5.000 | 0.0000 | 0.0000 | 2.321 |
| Utility-Trust-Misalignment | TRUE_A9 < Blind_A9 | 7.150 | 9.645 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.964 |
| Utility-Trust-Misalignment | TRUE-C_U > Blind_U | 24893.300 | 128.532 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.853 |
| Utility-Trust-Misalignment | TRUE-C_Fatal < Blind_Fatal | 151.270 | 117.596 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.760 |
| Utility-Trust-Misalignment | TRUE-C_U > TTB_U | 2019.900 | 4.718 | 0.0000 | 0.0003 | 1053.500 | 0.0000 | 0.0001 | 0.472 |
| Utility-Trust-Misalignment | TRUE-C_Fatal < TTB_Fatal | 6.790 | 3.295 | 0.0010 | 0.1262 | 1425.500 | 0.0036 | 0.4597 | 0.329 |
| Utility-Trust-Misalignment | TRUE-C_U > MOO_U | 1511.300 | 4.792 | 0.0000 | 0.0002 | 1125.500 | 0.0000 | 0.0003 | 0.479 |
| Utility-Trust-Misalignment | TRUE-C_Fatal < MOO_Fatal | 6.700 | 4.303 | 0.0000 | 0.0022 | 1202.000 | 0.0000 | 0.0030 | 0.430 |
| Utility-Trust-Misalignment | TRUE-C_Collapse < TTB_Collapse | 0.044 | 23.320 | 0.0000 | 0.0000 | 8.000 | 0.0000 | 0.0000 | 2.332 |
| Utility-Trust-Misalignment | TRUE-C_A9 < Blind_A9 | 6.590 | 8.749 | 0.0000 | 0.0000 | 143.000 | 0.0000 | 0.0000 | 0.875 |
| Utility-Trust-Misalignment | TRUE-E_U > Blind_U | 24413.100 | 133.220 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.322 |
| Utility-Trust-Misalignment | TRUE-E_Fatal < Blind_Fatal | 152.000 | 121.196 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.120 |
| Utility-Trust-Misalignment | TRUE-E_U > TTB_U | 1539.700 | 3.518 | 0.0004 | 0.0556 | 1541.000 | 0.0007 | 0.0917 | 0.352 |
| Utility-Trust-Misalignment | TRUE-E_Fatal < TTB_Fatal | 7.520 | 3.710 | 0.0002 | 0.0266 | 1190.000 | 0.0002 | 0.0281 | 0.371 |
| Utility-Trust-Misalignment | TRUE-E_U > MOO_U | 1031.100 | 3.833 | 0.0001 | 0.0162 | 1451.500 | 0.0002 | 0.0286 | 0.383 |
| Utility-Trust-Misalignment | TRUE-E_Fatal < MOO_Fatal | 7.430 | 5.455 | 0.0000 | 0.0000 | 904.000 | 0.0000 | 0.0000 | 0.546 |
| Utility-Trust-Misalignment | TRUE-E_Collapse < TTB_Collapse | 0.057 | 24.274 | 0.0000 | 0.0000 | 2.000 | 0.0000 | 0.0000 | 2.427 |
| Utility-Trust-Misalignment | TRUE-E_A9 < Blind_A9 | 7.010 | 9.425 | 0.0000 | 0.0000 | 24.500 | 0.0000 | 0.0000 | 0.942 |
| Utility-Trust-Misalignment | TRUE-N_U > Blind_U | 25272.000 | 143.210 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 14.321 |
| Utility-Trust-Misalignment | TRUE-N_Fatal < Blind_Fatal | 152.670 | 119.695 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.969 |
| Utility-Trust-Misalignment | TRUE-N_U > TTB_U | 2398.600 | 5.740 | 0.0000 | 0.0000 | 698.000 | 0.0000 | 0.0000 | 0.574 |
| Utility-Trust-Misalignment | TRUE-N_Fatal < TTB_Fatal | 8.190 | 4.092 | 0.0000 | 0.0055 | 1144.500 | 0.0000 | 0.0020 | 0.409 |
| Utility-Trust-Misalignment | TRUE-N_U > MOO_U | 1890.000 | 6.550 | 0.0000 | 0.0000 | 700.500 | 0.0000 | 0.0000 | 0.655 |
| Utility-Trust-Misalignment | TRUE-N_Fatal < MOO_Fatal | 8.100 | 5.753 | 0.0000 | 0.0000 | 836.500 | 0.0000 | 0.0000 | 0.575 |
| Utility-Trust-Misalignment | TRUE-N_Collapse < TTB_Collapse | 0.033 | 12.698 | 0.0000 | 0.0000 | 164.000 | 0.0000 | 0.0000 | 1.270 |
| Utility-Trust-Misalignment | TRUE-N_A9 < Blind_A9 | -400.030 | -8.382 | 0.0000 | 0.0000 | 316.000 | 0.0000 | 0.0000 | -0.838 |

## Interpretation & Limitations

- Task flows are paired: within each run all groups see the same module sequence. Differences in outcome are therefore attributable to selection mechanisms, not task luck.
- A8 surface-quality bonus is uniform across groups. The only remaining A8 asymmetry is inside TTB's scoring function (A8 receives extra trust-objective weight), which is a *mechanism-level* difference, not an observation-level manipulation.
- Ablation results isolate component contributions: if TRUE-C is substantially worse than TRUE, the constraint filter is a key driver of advantage.
- Bonferroni correction is conservative; if a hypothesis remains significant after correction, the conclusion is robust.
- The experiment remains a probabilistic generative model; no real engineering tools are used.
