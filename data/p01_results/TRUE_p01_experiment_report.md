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

- **Safety-Critical**: High-stakes safety environment with harsher penalties and stronger error propagation.
- **Observation-Manipulated**: Observation-contaminated environment where surface quality can diverge from true quality.
- **Baseline**: Standard engineering collaboration with moderate observation noise.
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
| Safety-Critical | TRUE | -3596.2 | [-4179.6, -3014.4] | 0.796 | 0.718 | 41.7 | 0.812 | 0.654 | 0.413 | 0.3 | 0.177 |
| Safety-Critical | TRUE-no-cap | -5401.6 | [-5973.6, -4817.4] | 0.740 | 0.679 | 43.4 | 0.805 | 0.619 | 0.406 | 0.0 | 0.170 |
| Safety-Critical | TTB | -5524.4 | [-7212.0, -4153.8] | 0.787 | 0.719 | 47.0 | 0.793 | 0.743 | 0.451 | 800.5 | 0.009 |
| Safety-Critical | TTB-cap | -1797.4 | [-2406.8, -1219.6] | 0.830 | 0.742 | 39.1 | 0.823 | 0.746 | 0.454 | 999.0 | 0.000 |
| Safety-Critical | MOO | -4532.0 | [-5238.8, -3816.2] | 0.801 | 0.724 | 44.7 | 0.800 | 0.724 | 0.440 | 850.0 | 0.041 |
| Safety-Critical | MOO-cap | -3370.4 | [-4114.4, -2626.0] | 0.816 | 0.735 | 41.9 | 0.811 | 0.734 | 0.447 | 861.1 | 0.000 |
| Safety-Critical | Blind | -53595.0 | [-54161.8, -53049.4] | 0.341 | 0.379 | 213.9 | 0.298 | 0.539 | 0.323 | 6.6 | 0.000 |
| Observation-Manipulated | TRUE | 2102.4 | [1752.4, 2443.6] | 0.769 | 0.638 | 51.7 | 0.770 | 0.602 | 0.363 | 0.0 | -0.008 |
| Observation-Manipulated | TRUE-no-cap | -1176.0 | [-1570.8, -780.4] | 0.635 | 0.572 | 58.9 | 0.741 | 0.470 | 0.297 | 0.0 | -0.011 |
| Observation-Manipulated | TTB | 1110.0 | [464.8, 1646.0] | 0.759 | 0.638 | 55.4 | 0.757 | 0.738 | 0.443 | 831.3 | 0.006 |
| Observation-Manipulated | TTB-cap | 2929.2 | [2570.0, 3255.6] | 0.808 | 0.660 | 49.8 | 0.778 | 0.737 | 0.442 | 999.0 | 0.000 |
| Observation-Manipulated | MOO | -910.0 | [-1735.6, -230.8] | 0.757 | 0.638 | 66.6 | 0.720 | 0.646 | 0.388 | 544.4 | 0.008 |
| Observation-Manipulated | MOO-cap | 1696.8 | [1234.0, 2140.4] | 0.791 | 0.653 | 54.6 | 0.761 | 0.693 | 0.416 | 859.8 | -0.012 |
| Observation-Manipulated | Blind | -25003.2 | [-25364.4, -24659.6] | 0.338 | 0.438 | 197.2 | 0.338 | 0.519 | 0.312 | 6.0 | 0.000 |
| Baseline | TRUE | 708.0 | [353.2, 1075.8] | 0.765 | 0.739 | 61.7 | 0.730 | 0.639 | 0.395 | 0.2 | 0.226 |
| Baseline | TRUE-no-cap | -397.4 | [-802.0, 6.2] | 0.700 | 0.685 | 63.9 | 0.724 | 0.574 | 0.375 | 0.0 | 0.232 |
| Baseline | TTB | -565.2 | [-1380.0, 160.4] | 0.759 | 0.735 | 67.4 | 0.708 | 0.737 | 0.443 | 801.6 | 0.034 |
| Baseline | TTB-cap | 1811.8 | [1483.0, 2186.0] | 0.801 | 0.766 | 58.8 | 0.743 | 0.740 | 0.444 | 999.0 | 0.000 |
| Baseline | MOO | -477.0 | [-940.8, -32.8] | 0.766 | 0.743 | 69.3 | 0.706 | 0.702 | 0.422 | 750.5 | 0.075 |
| Baseline | MOO-cap | 542.6 | [-39.4, 1114.0] | 0.787 | 0.753 | 64.0 | 0.723 | 0.720 | 0.432 | 880.3 | 0.009 |
| Baseline | Blind | -23858.4 | [-24178.0, -23543.4] | 0.344 | 0.403 | 208.9 | 0.308 | 0.527 | 0.316 | 5.9 | 0.000 |
| Utility-Trust-Misalignment | TRUE | 2250.8 | [1927.9, 2570.9] | 0.745 | 0.707 | 56.1 | 0.751 | 0.616 | 0.379 | 0.1 | 0.311 |
| Utility-Trust-Misalignment | TRUE-no-cap | 341.0 | [-2.8, 674.4] | 0.660 | 0.638 | 58.8 | 0.741 | 0.540 | 0.364 | 0.0 | 0.264 |
| Utility-Trust-Misalignment | TTB | 686.8 | [-254.0, 1514.4] | 0.740 | 0.709 | 63.9 | 0.720 | 0.736 | 0.442 | 852.1 | 0.024 |
| Utility-Trust-Misalignment | TTB-cap | 3216.1 | [2906.2, 3520.6] | 0.782 | 0.734 | 54.5 | 0.757 | 0.737 | 0.442 | 999.0 | 0.000 |
| Utility-Trust-Misalignment | MOO | 818.0 | [209.7, 1388.4] | 0.746 | 0.709 | 64.9 | 0.719 | 0.694 | 0.416 | 771.1 | 0.084 |
| Utility-Trust-Misalignment | MOO-cap | 2079.4 | [1667.0, 2511.5] | 0.765 | 0.722 | 58.6 | 0.740 | 0.716 | 0.430 | 849.8 | 0.078 |
| Utility-Trust-Misalignment | Blind | -21858.2 | [-22104.5, -21593.7] | 0.336 | 0.391 | 205.9 | 0.305 | 0.533 | 0.320 | 6.5 | 0.000 |

## Scenario Conclusions

### Safety-Critical

- TRUE vs Blind: cumulative utility diff = 49998.8; fatal errors diff = -172.2.
- TRUE vs TTB: cumulative utility diff = 1928.2; fatal errors diff = -5.4.
- TRUE A9 first delay = 0.3; collapse index = 0.413.

### Observation-Manipulated

- TRUE vs Blind: cumulative utility diff = 27105.6; fatal errors diff = -145.5.
- TRUE vs TTB: cumulative utility diff = 992.4; fatal errors diff = -3.7.
- TRUE A9 first delay = 0.0; collapse index = 0.363.

### Baseline

- TRUE vs Blind: cumulative utility diff = 24566.4; fatal errors diff = -147.3.
- TRUE vs TTB: cumulative utility diff = 1273.2; fatal errors diff = -5.7.
- TRUE A9 first delay = 0.2; collapse index = 0.395.

### Utility-Trust-Misalignment

- TRUE vs Blind: cumulative utility diff = 24109.0; fatal errors diff = -149.7.
- TRUE vs TTB: cumulative utility diff = 1564.0; fatal errors diff = -7.8.
- TRUE A9 first delay = 0.1; collapse index = 0.379.

## Hypothesis Tests

| Scenario | Hypothesis | Mean Diff | t | p_t | p_t(Bonf) | W | p_w | p_w(Bonf) | Cohen d |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | TRUE_U > TTB_U | 1273.200 | 2.832 | 0.0046 | 0.4435 | 1886.500 | 0.0281 | 1.0000 | 0.283 |
| Baseline | TRUE_Fatal < TTB_Fatal | 5.690 | 2.773 | 0.0056 | 0.5335 | 1820.000 | 0.0222 | 1.0000 | 0.277 |
| Baseline | TRUE_U > TTB-cap_U | -1103.800 | -4.419 | 0.0000 | 0.0009 | 1351.000 | 0.0001 | 0.0052 | -0.442 |
| Baseline | TRUE_Fatal < TTB-cap_Fatal | -2.910 | -2.662 | 0.0078 | 0.7461 | 1768.000 | 0.0286 | 1.0000 | -0.266 |
| Baseline | TRUE_U > MOO_U | 1185.000 | 4.126 | 0.0000 | 0.0035 | 1430.500 | 0.0002 | 0.0161 | 0.413 |
| Baseline | TRUE_Fatal < MOO_Fatal | 7.610 | 5.392 | 0.0000 | 0.0000 | 943.500 | 0.0000 | 0.0001 | 0.539 |
| Baseline | TRUE_U > MOO-cap_U | 165.400 | 0.491 | 0.6235 | 1.0000 | 2404.500 | 0.8056 | 1.0000 | 0.049 |
| Baseline | TRUE_Fatal < MOO-cap_Fatal | 2.280 | 1.522 | 0.1280 | 1.0000 | 2026.500 | 0.3467 | 1.0000 | 0.152 |
| Baseline | TRUE_U > Blind_U | 24566.400 | 117.378 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.738 |
| Baseline | TRUE_Fatal < Blind_Fatal | 147.270 | 109.757 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.976 |
| Baseline | TRUE_Collapse < TTB_Collapse | 0.048 | 23.000 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 2.300 |
| Baseline | TRUE_A9 < Blind_A9 | 5.740 | 8.955 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.896 |
| Baseline | TRUE-no-cap_U > TTB_U | 167.800 | 0.355 | 0.7228 | 1.0000 | 2228.500 | 0.3896 | 1.0000 | 0.035 |
| Baseline | TRUE-no-cap_Fatal < TTB_Fatal | 3.490 | 1.654 | 0.0981 | 1.0000 | 2113.500 | 0.5366 | 1.0000 | 0.165 |
| Baseline | TRUE-no-cap_U > TTB-cap_U | -2209.200 | -8.296 | 0.0000 | 0.0000 | 666.500 | 0.0000 | 0.0000 | -0.830 |
| Baseline | TRUE-no-cap_Fatal < TTB-cap_Fatal | -5.110 | -4.280 | 0.0000 | 0.0018 | 1295.500 | 0.0001 | 0.0096 | -0.428 |
| Baseline | TRUE-no-cap_U > MOO_U | 79.600 | 0.251 | 0.8016 | 1.0000 | 2418.000 | 0.7129 | 1.0000 | 0.025 |
| Baseline | TRUE-no-cap_Fatal < MOO_Fatal | 5.410 | 3.461 | 0.0005 | 0.0517 | 1601.500 | 0.0079 | 0.7617 | 0.346 |
| Baseline | TRUE-no-cap_U > MOO-cap_U | -940.000 | -2.742 | 0.0061 | 0.5866 | 1510.500 | 0.0008 | 0.0731 | -0.274 |
| Baseline | TRUE-no-cap_Fatal < MOO-cap_Fatal | 0.080 | 0.052 | 0.9582 | 1.0000 | 2210.500 | 0.6676 | 1.0000 | 0.005 |
| Baseline | TRUE-no-cap_U > Blind_U | 23461.000 | 102.587 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.259 |
| Baseline | TRUE-no-cap_Fatal < Blind_Fatal | 145.070 | 103.716 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.372 |
| Baseline | TRUE-no-cap_Collapse < TTB_Collapse | 0.067 | 23.680 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 2.368 |
| Baseline | TRUE-no-cap_A9 < Blind_A9 | 5.890 | 9.157 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.916 |
| Observation-Manipulated | TRUE_U > TTB_U | 992.400 | 2.806 | 0.0050 | 0.4819 | 1688.500 | 0.0060 | 0.5807 | 0.281 |
| Observation-Manipulated | TRUE_Fatal < TTB_Fatal | 3.660 | 2.540 | 0.0111 | 1.0000 | 1644.000 | 0.0124 | 1.0000 | 0.254 |
| Observation-Manipulated | TRUE_U > TTB-cap_U | -826.800 | -3.444 | 0.0006 | 0.0550 | 1546.500 | 0.0018 | 0.1767 | -0.344 |
| Observation-Manipulated | TRUE_Fatal < TTB-cap_Fatal | -1.910 | -2.022 | 0.0432 | 1.0000 | 1745.500 | 0.0663 | 1.0000 | -0.202 |
| Observation-Manipulated | TRUE_U > MOO_U | 3012.400 | 7.583 | 0.0000 | 0.0000 | 433.500 | 0.0000 | 0.0000 | 0.758 |
| Observation-Manipulated | TRUE_Fatal < MOO_Fatal | 14.870 | 8.381 | 0.0000 | 0.0000 | 334.500 | 0.0000 | 0.0000 | 0.838 |
| Observation-Manipulated | TRUE_U > MOO-cap_U | 405.600 | 1.529 | 0.1264 | 1.0000 | 2044.000 | 0.2315 | 1.0000 | 0.153 |
| Observation-Manipulated | TRUE_Fatal < MOO-cap_Fatal | 2.860 | 2.601 | 0.0093 | 0.8930 | 1779.000 | 0.0220 | 1.0000 | 0.260 |
| Observation-Manipulated | TRUE_U > Blind_U | 27105.600 | 116.149 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.615 |
| Observation-Manipulated | TRUE_Fatal < Blind_Fatal | 145.500 | 115.097 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.510 |
| Observation-Manipulated | TRUE_Collapse < TTB_Collapse | 0.080 | 44.103 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 4.410 |
| Observation-Manipulated | TRUE_A9 < Blind_A9 | 6.020 | 10.552 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 1.055 |
| Observation-Manipulated | TRUE-no-cap_U > TTB_U | -2286.000 | -6.628 | 0.0000 | 0.0000 | 597.000 | 0.0000 | 0.0000 | -0.663 |
| Observation-Manipulated | TRUE-no-cap_Fatal < TTB_Fatal | -3.530 | -2.556 | 0.0106 | 1.0000 | 1341.000 | 0.0002 | 0.0187 | -0.256 |
| Observation-Manipulated | TRUE-no-cap_U > TTB-cap_U | -4105.200 | -15.173 | 0.0000 | 0.0000 | 68.500 | 0.0000 | 0.0000 | -1.517 |
| Observation-Manipulated | TRUE-no-cap_Fatal < TTB-cap_Fatal | -9.100 | -8.579 | 0.0000 | 0.0000 | 515.000 | 0.0000 | 0.0000 | -0.858 |
| Observation-Manipulated | TRUE-no-cap_U > MOO_U | -266.000 | -0.634 | 0.5262 | 1.0000 | 1916.000 | 0.0710 | 1.0000 | -0.063 |
| Observation-Manipulated | TRUE-no-cap_Fatal < MOO_Fatal | 7.680 | 4.104 | 0.0000 | 0.0039 | 1370.500 | 0.0001 | 0.0111 | 0.410 |
| Observation-Manipulated | TRUE-no-cap_U > MOO-cap_U | -2872.800 | -10.567 | 0.0000 | 0.0000 | 372.000 | 0.0000 | 0.0000 | -1.057 |
| Observation-Manipulated | TRUE-no-cap_Fatal < MOO-cap_Fatal | -4.330 | -3.773 | 0.0002 | 0.0155 | 1225.000 | 0.0001 | 0.0086 | -0.377 |
| Observation-Manipulated | TRUE-no-cap_U > Blind_U | 23827.200 | 99.539 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 9.954 |
| Observation-Manipulated | TRUE-no-cap_Fatal < Blind_Fatal | 138.310 | 107.234 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.723 |
| Observation-Manipulated | TRUE-no-cap_Collapse < TTB_Collapse | 0.146 | 68.140 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 6.814 |
| Observation-Manipulated | TRUE-no-cap_A9 < Blind_A9 | 6.020 | 10.552 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 1.055 |
| Safety-Critical | TRUE_U > TTB_U | 1928.200 | 2.386 | 0.0170 | 1.0000 | 2008.500 | 0.0758 | 1.0000 | 0.239 |
| Safety-Critical | TRUE_Fatal < TTB_Fatal | 5.360 | 2.595 | 0.0095 | 0.9092 | 1795.500 | 0.0177 | 1.0000 | 0.259 |
| Safety-Critical | TRUE_U > TTB-cap_U | -1798.800 | -4.918 | 0.0000 | 0.0001 | 1225.500 | 0.0000 | 0.0008 | -0.492 |
| Safety-Critical | TRUE_Fatal < TTB-cap_Fatal | -2.540 | -2.820 | 0.0048 | 0.4608 | 1480.000 | 0.0045 | 0.4363 | -0.282 |
| Safety-Critical | TRUE_U > MOO_U | 935.800 | 2.043 | 0.0411 | 1.0000 | 2004.000 | 0.0732 | 1.0000 | 0.204 |
| Safety-Critical | TRUE_Fatal < MOO_Fatal | 3.020 | 2.602 | 0.0093 | 0.8897 | 1710.500 | 0.0240 | 1.0000 | 0.260 |
| Safety-Critical | TRUE_U > MOO-cap_U | -225.800 | -0.461 | 0.6449 | 1.0000 | 2214.000 | 0.2849 | 1.0000 | -0.046 |
| Safety-Critical | TRUE_Fatal < MOO-cap_Fatal | 0.240 | 0.206 | 0.8369 | 1.0000 | 2287.000 | 0.7474 | 1.0000 | 0.021 |
| Safety-Critical | TRUE_U > Blind_U | 49998.800 | 147.664 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 14.766 |
| Safety-Critical | TRUE_Fatal < Blind_Fatal | 172.210 | 137.044 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.704 |
| Safety-Critical | TRUE_Collapse < TTB_Collapse | 0.039 | 18.883 | 0.0000 | 0.0000 | 26.000 | 0.0000 | 0.0000 | 1.888 |
| Safety-Critical | TRUE_A9 < Blind_A9 | 6.230 | 9.243 | 0.0000 | 0.0000 | 19.500 | 0.0000 | 0.0000 | 0.924 |
| Safety-Critical | TRUE-no-cap_U > TTB_U | 122.800 | 0.155 | 0.8772 | 1.0000 | 2053.000 | 0.1046 | 1.0000 | 0.015 |
| Safety-Critical | TRUE-no-cap_Fatal < TTB_Fatal | 3.620 | 1.777 | 0.0755 | 1.0000 | 1933.500 | 0.2595 | 1.0000 | 0.178 |
| Safety-Critical | TRUE-no-cap_U > TTB-cap_U | -3604.200 | -8.213 | 0.0000 | 0.0000 | 665.500 | 0.0000 | 0.0000 | -0.821 |
| Safety-Critical | TRUE-no-cap_Fatal < TTB-cap_Fatal | -4.280 | -3.828 | 0.0001 | 0.0124 | 1385.000 | 0.0004 | 0.0346 | -0.383 |
| Safety-Critical | TRUE-no-cap_U > MOO_U | -869.600 | -2.061 | 0.0393 | 1.0000 | 1920.000 | 0.0375 | 1.0000 | -0.206 |
| Safety-Critical | TRUE-no-cap_Fatal < MOO_Fatal | 1.280 | 1.112 | 0.2660 | 1.0000 | 1972.500 | 0.2537 | 1.0000 | 0.111 |
| Safety-Critical | TRUE-no-cap_U > MOO-cap_U | -2031.200 | -4.108 | 0.0000 | 0.0038 | 1161.000 | 0.0000 | 0.0003 | -0.411 |
| Safety-Critical | TRUE-no-cap_Fatal < MOO-cap_Fatal | -1.500 | -1.221 | 0.2220 | 1.0000 | 1851.000 | 0.0813 | 1.0000 | -0.122 |
| Safety-Critical | TRUE-no-cap_U > Blind_U | 48193.400 | 120.548 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.055 |
| Safety-Critical | TRUE-no-cap_Fatal < Blind_Fatal | 170.470 | 121.374 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.137 |
| Safety-Critical | TRUE-no-cap_Collapse < TTB_Collapse | 0.045 | 18.750 | 0.0000 | 0.0000 | 15.000 | 0.0000 | 0.0000 | 1.875 |
| Safety-Critical | TRUE-no-cap_A9 < Blind_A9 | 6.520 | 9.772 | 0.0000 | 0.0000 | 5.500 | 0.0000 | 0.0000 | 0.977 |
| Utility-Trust-Misalignment | TRUE_U > TTB_U | 1564.000 | 3.110 | 0.0019 | 0.1796 | 1788.000 | 0.0113 | 1.0000 | 0.311 |
| Utility-Trust-Misalignment | TRUE_Fatal < TTB_Fatal | 7.750 | 3.089 | 0.0020 | 0.1927 | 1634.000 | 0.0112 | 1.0000 | 0.309 |
| Utility-Trust-Misalignment | TRUE_U > TTB-cap_U | -965.300 | -4.413 | 0.0000 | 0.0010 | 1389.500 | 0.0001 | 0.0091 | -0.441 |
| Utility-Trust-Misalignment | TRUE_Fatal < TTB-cap_Fatal | -1.670 | -1.679 | 0.0932 | 1.0000 | 2058.000 | 0.1455 | 1.0000 | -0.168 |
| Utility-Trust-Misalignment | TRUE_U > MOO_U | 1432.800 | 4.159 | 0.0000 | 0.0031 | 1376.000 | 0.0001 | 0.0075 | 0.416 |
| Utility-Trust-Misalignment | TRUE_Fatal < MOO_Fatal | 8.780 | 5.152 | 0.0000 | 0.0000 | 1102.500 | 0.0000 | 0.0003 | 0.515 |
| Utility-Trust-Misalignment | TRUE_U > MOO-cap_U | 171.400 | 0.697 | 0.4861 | 1.0000 | 2393.000 | 0.6499 | 1.0000 | 0.070 |
| Utility-Trust-Misalignment | TRUE_Fatal < MOO-cap_Fatal | 2.490 | 2.092 | 0.0365 | 1.0000 | 1855.500 | 0.0608 | 1.0000 | 0.209 |
| Utility-Trust-Misalignment | TRUE_U > Blind_U | 24109.000 | 126.463 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.646 |
| Utility-Trust-Misalignment | TRUE_Fatal < Blind_Fatal | 149.720 | 122.859 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.286 |
| Utility-Trust-Misalignment | TRUE_Collapse < TTB_Collapse | 0.062 | 24.765 | 0.0000 | 0.0000 | 1.000 | 0.0000 | 0.0000 | 2.476 |
| Utility-Trust-Misalignment | TRUE_A9 < Blind_A9 | 6.430 | 7.894 | 0.0000 | 0.0000 | 17.000 | 0.0000 | 0.0000 | 0.789 |
| Utility-Trust-Misalignment | TRUE-no-cap_U > TTB_U | -345.800 | -0.667 | 0.5045 | 1.0000 | 1682.500 | 0.0038 | 0.3619 | -0.067 |
| Utility-Trust-Misalignment | TRUE-no-cap_Fatal < TTB_Fatal | 5.120 | 1.996 | 0.0460 | 1.0000 | 2274.500 | 0.3891 | 1.0000 | 0.200 |
| Utility-Trust-Misalignment | TRUE-no-cap_U > TTB-cap_U | -2875.100 | -12.312 | 0.0000 | 0.0000 | 222.000 | 0.0000 | 0.0000 | -1.231 |
| Utility-Trust-Misalignment | TRUE-no-cap_Fatal < TTB-cap_Fatal | -4.300 | -3.824 | 0.0001 | 0.0126 | 1334.500 | 0.0002 | 0.0170 | -0.382 |
| Utility-Trust-Misalignment | TRUE-no-cap_U > MOO_U | -477.000 | -1.456 | 0.1455 | 1.0000 | 1940.500 | 0.0445 | 1.0000 | -0.146 |
| Utility-Trust-Misalignment | TRUE-no-cap_Fatal < MOO_Fatal | 6.150 | 3.926 | 0.0001 | 0.0083 | 1332.500 | 0.0004 | 0.0419 | 0.393 |
| Utility-Trust-Misalignment | TRUE-no-cap_U > MOO-cap_U | -1738.400 | -5.961 | 0.0000 | 0.0000 | 870.000 | 0.0000 | 0.0000 | -0.596 |
| Utility-Trust-Misalignment | TRUE-no-cap_Fatal < MOO-cap_Fatal | -0.140 | -0.099 | 0.9212 | 1.0000 | 2241.500 | 0.8864 | 1.0000 | -0.010 |
| Utility-Trust-Misalignment | TRUE-no-cap_U > Blind_U | 22199.200 | 99.481 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 9.948 |
| Utility-Trust-Misalignment | TRUE-no-cap_Fatal < Blind_Fatal | 147.090 | 103.147 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.315 |
| Utility-Trust-Misalignment | TRUE-no-cap_Collapse < TTB_Collapse | 0.078 | 25.726 | 0.0000 | 0.0000 | 1.000 | 0.0000 | 0.0000 | 2.573 |
| Utility-Trust-Misalignment | TRUE-no-cap_A9 < Blind_A9 | 6.520 | 8.008 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.801 |

## Interpretation & Limitations

- Task flows are paired: within each run all groups see the same module sequence. Differences in outcome are therefore attributable to selection mechanisms, not task luck.
- A8 surface-quality bonus is uniform across groups. The only remaining A8 asymmetry is inside TTB's scoring function (A8 receives extra trust-objective weight), which is a *mechanism-level* difference, not an observation-level manipulation.
- Ablation results isolate component contributions: if TRUE-C is substantially worse than TRUE, the constraint filter is a key driver of advantage.
- Bonferroni correction is conservative; if a hypothesis remains significant after correction, the conclusion is robust.
- The experiment remains a probabilistic generative model; no real engineering tools are used.
