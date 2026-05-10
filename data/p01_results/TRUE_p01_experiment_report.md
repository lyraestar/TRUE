# TRUE Simulation Experiment Report (P0/P1 Refactored)

## Executive Summary

This experiment compares TRUE and its ablations against Blind and TTB baselines across 4 parameterized scenarios.
All groups within a Monte Carlo run face the identical task sequence. 100 runs x 200 rounds x 4 scenarios x 6 groups.

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
| Baseline | TRUE | 896.8 | [520.4, 1274.0] | 0.767 | 0.739 | 61.0 | 0.733 | 0.637 | 0.394 | 0.2 | 0.293 |
| Baseline | TRUE-C | 1377.6 | [1037.2, 1739.0] | 0.799 | 0.767 | 60.7 | 0.735 | 0.679 | 0.408 | 0.9 | 0.000 |
| Baseline | TRUE-E | 779.2 | [451.0, 1103.0] | 0.765 | 0.737 | 61.0 | 0.731 | 0.639 | 0.396 | 0.2 | 0.214 |
| Baseline | TRUE-N | 1326.0 | [974.4, 1671.8] | 0.798 | 0.766 | 60.5 | 0.734 | 0.702 | 0.422 | 383.9 | 0.000 |
| Baseline | Blind | -23753.6 | [-24089.4, -23428.6] | 0.343 | 0.402 | 208.2 | 0.310 | 0.529 | 0.317 | 6.8 | 0.000 |
| Baseline | TTB | -2289.2 | [-3435.4, -1271.8] | 0.738 | 0.726 | 77.2 | 0.677 | 0.721 | 0.436 | 701.3 | 0.221 |
| Observation-Manipulated | TRUE | 2102.4 | [1752.4, 2443.6] | 0.769 | 0.638 | 51.7 | 0.770 | 0.602 | 0.363 | 0.0 | -0.008 |
| Observation-Manipulated | TRUE-C | 2819.6 | [2452.4, 3204.4] | 0.805 | 0.656 | 50.5 | 0.776 | 0.655 | 0.393 | 0.5 | 0.000 |
| Observation-Manipulated | TRUE-E | 2070.4 | [1720.4, 2422.4] | 0.769 | 0.640 | 51.7 | 0.770 | 0.611 | 0.368 | 0.0 | -0.018 |
| Observation-Manipulated | TRUE-N | 2457.2 | [2102.8, 2828.4] | 0.802 | 0.660 | 51.7 | 0.771 | 0.657 | 0.394 | 3.8 | 0.000 |
| Observation-Manipulated | Blind | -25168.4 | [-25488.0, -24823.6] | 0.335 | 0.437 | 198.5 | 0.335 | 0.519 | 0.311 | 5.0 | 0.000 |
| Observation-Manipulated | TTB | -28398.8 | [-29048.8, -27646.0] | 0.233 | 0.730 | 221.8 | 0.278 | 0.855 | 0.513 | 999.0 | 0.007 |
| Utility-Trust-Misalignment | TRUE | 2345.4 | [2040.2, 2640.5] | 0.749 | 0.705 | 56.1 | 0.752 | 0.619 | 0.381 | 0.1 | 0.257 |
| Utility-Trust-Misalignment | TRUE-C | 2954.1 | [2640.3, 3284.8] | 0.782 | 0.735 | 55.6 | 0.752 | 0.659 | 0.396 | 0.7 | 0.000 |
| Utility-Trust-Misalignment | TRUE-E | 2473.9 | [2188.1, 2762.3] | 0.748 | 0.710 | 54.9 | 0.755 | 0.621 | 0.384 | 0.3 | 0.258 |
| Utility-Trust-Misalignment | TRUE-N | 3332.8 | [3057.4, 3626.7] | 0.784 | 0.737 | 54.2 | 0.758 | 0.679 | 0.408 | 407.3 | 0.000 |
| Utility-Trust-Misalignment | Blind | -21939.2 | [-22229.4, -21643.8] | 0.335 | 0.393 | 206.9 | 0.303 | 0.533 | 0.320 | 7.3 | 0.000 |
| Utility-Trust-Misalignment | TTB | 603.8 | [-377.7, 1502.8] | 0.731 | 0.703 | 65.2 | 0.720 | 0.727 | 0.438 | 791.1 | 0.302 |
| Safety-Critical | TRUE | -3313.0 | [-3820.2, -2813.8] | 0.794 | 0.723 | 41.5 | 0.815 | 0.656 | 0.414 | 0.4 | 0.151 |
| Safety-Critical | TRUE-C | -2116.4 | [-2635.4, -1568.0] | 0.826 | 0.746 | 39.3 | 0.822 | 0.685 | 0.418 | 0.9 | 0.000 |
| Safety-Critical | TRUE-E | -3262.6 | [-3825.4, -2707.4] | 0.795 | 0.718 | 40.9 | 0.816 | 0.655 | 0.414 | 0.3 | 0.169 |
| Safety-Critical | TRUE-N | -1725.8 | [-2209.2, -1218.0] | 0.831 | 0.748 | 38.8 | 0.824 | 0.721 | 0.438 | 920.5 | 0.000 |
| Safety-Critical | Blind | -53506.0 | [-54045.8, -52926.2] | 0.340 | 0.376 | 214.4 | 0.299 | 0.538 | 0.323 | 7.0 | 0.000 |
| Safety-Critical | TTB | -5295.6 | [-6260.4, -4436.8] | 0.775 | 0.711 | 46.0 | 0.798 | 0.736 | 0.450 | 683.1 | 0.247 |

## Scenario Conclusions

### Baseline

- TRUE vs Blind: cumulative utility diff = 24650.4; fatal errors diff = -147.2.
- TRUE vs TTB: cumulative utility diff = 3186.0; fatal errors diff = -16.2.
- TRUE A9 first delay = 0.2; collapse index = 0.394.

### Observation-Manipulated

- TRUE vs Blind: cumulative utility diff = 27270.8; fatal errors diff = -146.8.
- TRUE vs TTB: cumulative utility diff = 30501.2; fatal errors diff = -170.0.
- TRUE A9 first delay = 0.0; collapse index = 0.363.

### Utility-Trust-Misalignment

- TRUE vs Blind: cumulative utility diff = 24284.6; fatal errors diff = -150.8.
- TRUE vs TTB: cumulative utility diff = 1741.6; fatal errors diff = -9.1.
- TRUE A9 first delay = 0.1; collapse index = 0.381.

### Safety-Critical

- TRUE vs Blind: cumulative utility diff = 50193.0; fatal errors diff = -172.9.
- TRUE vs TTB: cumulative utility diff = 1982.6; fatal errors diff = -4.5.
- TRUE A9 first delay = 0.4; collapse index = 0.414.

## Hypothesis Tests

| Scenario | Hypothesis | Mean Diff | t | p_t | p_t(Bonf) | W | p_w | p_w(Bonf) | Cohen d |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | TRUE_U > Blind_U | 24650.400 | 116.802 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.680 |
| Baseline | TRUE_Fatal < Blind_Fatal | 147.150 | 121.144 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.114 |
| Baseline | TRUE_U > TTB_U | 3186.000 | 5.319 | 0.0000 | 0.0000 | 964.500 | 0.0000 | 0.0000 | 0.532 |
| Baseline | TRUE_Fatal < TTB_Fatal | 16.180 | 5.402 | 0.0000 | 0.0000 | 813.000 | 0.0000 | 0.0000 | 0.540 |
| Baseline | TRUE_Collapse < TTB_Collapse | 0.042 | 15.420 | 0.0000 | 0.0000 | 83.000 | 0.0000 | 0.0000 | 1.542 |
| Baseline | TRUE_A9 < Blind_A9 | 6.530 | 9.155 | 0.0000 | 0.0000 | 47.000 | 0.0000 | 0.0000 | 0.915 |
| Baseline | TRUE-C_U > Blind_U | 25131.200 | 122.175 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.217 |
| Baseline | TRUE-C_Fatal < Blind_Fatal | 147.420 | 114.162 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.416 |
| Baseline | TRUE-C_U > TTB_U | 3666.800 | 6.021 | 0.0000 | 0.0000 | 769.500 | 0.0000 | 0.0000 | 0.602 |
| Baseline | TRUE-C_Fatal < TTB_Fatal | 16.450 | 5.549 | 0.0000 | 0.0000 | 780.000 | 0.0000 | 0.0000 | 0.555 |
| Baseline | TRUE-C_Collapse < TTB_Collapse | 0.028 | 12.365 | 0.0000 | 0.0000 | 260.000 | 0.0000 | 0.0000 | 1.236 |
| Baseline | TRUE-C_A9 < Blind_A9 | 5.880 | 7.914 | 0.0000 | 0.0000 | 240.500 | 0.0000 | 0.0000 | 0.791 |
| Baseline | TRUE-E_U > Blind_U | 24532.800 | 128.186 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.819 |
| Baseline | TRUE-E_Fatal < Blind_Fatal | 147.170 | 124.015 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.401 |
| Baseline | TRUE-E_U > TTB_U | 3068.400 | 5.357 | 0.0000 | 0.0000 | 1002.000 | 0.0000 | 0.0000 | 0.536 |
| Baseline | TRUE-E_Fatal < TTB_Fatal | 16.200 | 5.609 | 0.0000 | 0.0000 | 783.500 | 0.0000 | 0.0000 | 0.561 |
| Baseline | TRUE-E_Collapse < TTB_Collapse | 0.039 | 14.987 | 0.0000 | 0.0000 | 73.000 | 0.0000 | 0.0000 | 1.499 |
| Baseline | TRUE-E_A9 < Blind_A9 | 6.560 | 9.236 | 0.0000 | 0.0000 | 13.000 | 0.0000 | 0.0000 | 0.924 |
| Baseline | TRUE-N_U > Blind_U | 25079.600 | 112.232 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.223 |
| Baseline | TRUE-N_Fatal < Blind_Fatal | 147.630 | 107.736 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.774 |
| Baseline | TRUE-N_U > TTB_U | 3615.200 | 6.066 | 0.0000 | 0.0000 | 711.000 | 0.0000 | 0.0000 | 0.607 |
| Baseline | TRUE-N_Fatal < TTB_Fatal | 16.660 | 5.674 | 0.0000 | 0.0000 | 736.500 | 0.0000 | 0.0000 | 0.567 |
| Baseline | TRUE-N_Collapse < TTB_Collapse | 0.014 | 5.507 | 0.0000 | 0.0000 | 1062.000 | 0.0000 | 0.0000 | 0.551 |
| Baseline | TRUE-N_A9 < Blind_A9 | -377.150 | -8.126 | 0.0000 | 0.0000 | 274.500 | 0.0000 | 0.0000 | -0.813 |
| Observation-Manipulated | TRUE_U > Blind_U | 27270.800 | 127.767 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.777 |
| Observation-Manipulated | TRUE_Fatal < Blind_Fatal | 146.750 | 125.028 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.503 |
| Observation-Manipulated | TRUE_U > TTB_U | 30501.200 | 74.133 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 7.413 |
| Observation-Manipulated | TRUE_Fatal < TTB_Fatal | 170.040 | 58.094 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 5.809 |
| Observation-Manipulated | TRUE_Collapse < TTB_Collapse | 0.151 | 118.507 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.851 |
| Observation-Manipulated | TRUE_A9 < Blind_A9 | 5.010 | 8.624 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.862 |
| Observation-Manipulated | TRUE-C_U > Blind_U | 27988.000 | 115.210 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.521 |
| Observation-Manipulated | TRUE-C_Fatal < Blind_Fatal | 147.990 | 122.490 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.249 |
| Observation-Manipulated | TRUE-C_U > TTB_U | 31218.400 | 76.292 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 7.629 |
| Observation-Manipulated | TRUE-C_Fatal < TTB_Fatal | 171.280 | 59.654 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 5.965 |
| Observation-Manipulated | TRUE-C_Collapse < TTB_Collapse | 0.120 | 105.311 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.531 |
| Observation-Manipulated | TRUE-C_A9 < Blind_A9 | 4.510 | 7.806 | 0.0000 | 0.0000 | 137.000 | 0.0000 | 0.0000 | 0.781 |
| Observation-Manipulated | TRUE-E_U > Blind_U | 27238.800 | 120.459 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.046 |
| Observation-Manipulated | TRUE-E_Fatal < Blind_Fatal | 146.770 | 123.037 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.304 |
| Observation-Manipulated | TRUE-E_U > TTB_U | 30469.200 | 78.136 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 7.814 |
| Observation-Manipulated | TRUE-E_Fatal < TTB_Fatal | 170.060 | 59.994 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 5.999 |
| Observation-Manipulated | TRUE-E_Collapse < TTB_Collapse | 0.146 | 111.201 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.120 |
| Observation-Manipulated | TRUE-E_A9 < Blind_A9 | 5.000 | 8.595 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.860 |
| Observation-Manipulated | TRUE-N_U > Blind_U | 27625.600 | 129.304 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.930 |
| Observation-Manipulated | TRUE-N_Fatal < Blind_Fatal | 146.750 | 132.879 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.288 |
| Observation-Manipulated | TRUE-N_U > TTB_U | 30856.000 | 77.477 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 7.748 |
| Observation-Manipulated | TRUE-N_Fatal < TTB_Fatal | 170.040 | 60.875 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 6.087 |
| Observation-Manipulated | TRUE-N_Collapse < TTB_Collapse | 0.119 | 82.257 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 8.226 |
| Observation-Manipulated | TRUE-N_A9 < Blind_A9 | 1.250 | 1.601 | 0.1093 | 1.0000 | 1305.500 | 0.0325 | 1.0000 | 0.160 |
| Safety-Critical | TRUE_U > Blind_U | 50193.000 | 133.675 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.368 |
| Safety-Critical | TRUE_Fatal < Blind_Fatal | 172.920 | 136.717 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.672 |
| Safety-Critical | TRUE_U > TTB_U | 1982.600 | 3.848 | 0.0001 | 0.0114 | 1470.000 | 0.0005 | 0.0434 | 0.385 |
| Safety-Critical | TRUE_Fatal < TTB_Fatal | 4.510 | 3.341 | 0.0008 | 0.0802 | 1478.000 | 0.0044 | 0.4261 | 0.334 |
| Safety-Critical | TRUE_Collapse < TTB_Collapse | 0.035 | 11.573 | 0.0000 | 0.0000 | 223.000 | 0.0000 | 0.0000 | 1.157 |
| Safety-Critical | TRUE_A9 < Blind_A9 | 6.600 | 9.569 | 0.0000 | 0.0000 | 50.000 | 0.0000 | 0.0000 | 0.957 |
| Safety-Critical | TRUE-C_U > Blind_U | 51389.600 | 138.703 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.870 |
| Safety-Critical | TRUE-C_Fatal < Blind_Fatal | 175.130 | 133.758 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.376 |
| Safety-Critical | TRUE-C_U > TTB_U | 3179.200 | 5.901 | 0.0000 | 0.0000 | 1024.000 | 0.0000 | 0.0000 | 0.590 |
| Safety-Critical | TRUE-C_Fatal < TTB_Fatal | 6.720 | 4.914 | 0.0000 | 0.0001 | 1159.500 | 0.0000 | 0.0007 | 0.491 |
| Safety-Critical | TRUE-C_Collapse < TTB_Collapse | 0.032 | 13.679 | 0.0000 | 0.0000 | 203.000 | 0.0000 | 0.0000 | 1.368 |
| Safety-Critical | TRUE-C_A9 < Blind_A9 | 6.060 | 8.896 | 0.0000 | 0.0000 | 171.000 | 0.0000 | 0.0000 | 0.890 |
| Safety-Critical | TRUE-E_U > Blind_U | 50243.400 | 138.720 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.872 |
| Safety-Critical | TRUE-E_Fatal < Blind_Fatal | 173.480 | 131.679 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.168 |
| Safety-Critical | TRUE-E_U > TTB_U | 2033.000 | 4.010 | 0.0001 | 0.0058 | 1480.000 | 0.0003 | 0.0314 | 0.401 |
| Safety-Critical | TRUE-E_Fatal < TTB_Fatal | 5.070 | 3.797 | 0.0001 | 0.0140 | 1562.000 | 0.0009 | 0.0892 | 0.380 |
| Safety-Critical | TRUE-E_Collapse < TTB_Collapse | 0.035 | 14.660 | 0.0000 | 0.0000 | 81.000 | 0.0000 | 0.0000 | 1.466 |
| Safety-Critical | TRUE-E_A9 < Blind_A9 | 6.640 | 9.889 | 0.0000 | 0.0000 | 61.500 | 0.0000 | 0.0000 | 0.989 |
| Safety-Critical | TRUE-N_U > Blind_U | 51780.200 | 136.258 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.626 |
| Safety-Critical | TRUE-N_Fatal < Blind_Fatal | 175.610 | 132.700 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.270 |
| Safety-Critical | TRUE-N_U > TTB_U | 3569.800 | 6.590 | 0.0000 | 0.0000 | 784.000 | 0.0000 | 0.0000 | 0.659 |
| Safety-Critical | TRUE-N_Fatal < TTB_Fatal | 7.200 | 5.060 | 0.0000 | 0.0000 | 1095.500 | 0.0000 | 0.0004 | 0.506 |
| Safety-Critical | TRUE-N_Collapse < TTB_Collapse | 0.011 | 4.705 | 0.0000 | 0.0002 | 1276.000 | 0.0000 | 0.0017 | 0.470 |
| Safety-Critical | TRUE-N_A9 < Blind_A9 | -913.510 | -34.277 | 0.0000 | 0.0000 | 1.500 | 0.0000 | 0.0000 | -3.428 |
| Utility-Trust-Misalignment | TRUE_U > Blind_U | 24284.600 | 118.415 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.842 |
| Utility-Trust-Misalignment | TRUE_Fatal < Blind_Fatal | 150.750 | 107.400 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.740 |
| Utility-Trust-Misalignment | TRUE_U > TTB_U | 1741.600 | 3.738 | 0.0002 | 0.0178 | 1514.000 | 0.0005 | 0.0488 | 0.374 |
| Utility-Trust-Misalignment | TRUE_Fatal < TTB_Fatal | 9.070 | 3.847 | 0.0001 | 0.0115 | 1335.000 | 0.0002 | 0.0171 | 0.385 |
| Utility-Trust-Misalignment | TRUE_Collapse < TTB_Collapse | 0.057 | 25.540 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 2.554 |
| Utility-Trust-Misalignment | TRUE_A9 < Blind_A9 | 7.150 | 9.645 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.964 |
| Utility-Trust-Misalignment | TRUE-C_U > Blind_U | 24893.300 | 128.532 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.853 |
| Utility-Trust-Misalignment | TRUE-C_Fatal < Blind_Fatal | 151.270 | 117.596 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.760 |
| Utility-Trust-Misalignment | TRUE-C_U > TTB_U | 2350.300 | 4.662 | 0.0000 | 0.0003 | 1117.500 | 0.0000 | 0.0001 | 0.466 |
| Utility-Trust-Misalignment | TRUE-C_Fatal < TTB_Fatal | 9.590 | 3.869 | 0.0001 | 0.0105 | 1341.500 | 0.0002 | 0.0188 | 0.387 |
| Utility-Trust-Misalignment | TRUE-C_Collapse < TTB_Collapse | 0.042 | 22.718 | 0.0000 | 0.0000 | 15.000 | 0.0000 | 0.0000 | 2.272 |
| Utility-Trust-Misalignment | TRUE-C_A9 < Blind_A9 | 6.590 | 8.749 | 0.0000 | 0.0000 | 143.000 | 0.0000 | 0.0000 | 0.875 |
| Utility-Trust-Misalignment | TRUE-E_U > Blind_U | 24413.100 | 133.220 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.322 |
| Utility-Trust-Misalignment | TRUE-E_Fatal < Blind_Fatal | 152.000 | 121.196 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.120 |
| Utility-Trust-Misalignment | TRUE-E_U > TTB_U | 1870.100 | 3.793 | 0.0001 | 0.0143 | 1470.000 | 0.0003 | 0.0275 | 0.379 |
| Utility-Trust-Misalignment | TRUE-E_Fatal < TTB_Fatal | 10.320 | 4.187 | 0.0000 | 0.0027 | 1097.000 | 0.0000 | 0.0011 | 0.419 |
| Utility-Trust-Misalignment | TRUE-E_Collapse < TTB_Collapse | 0.054 | 22.567 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 2.257 |
| Utility-Trust-Misalignment | TRUE-E_A9 < Blind_A9 | 7.010 | 9.425 | 0.0000 | 0.0000 | 24.500 | 0.0000 | 0.0000 | 0.942 |
| Utility-Trust-Misalignment | TRUE-N_U > Blind_U | 25272.000 | 143.210 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 14.321 |
| Utility-Trust-Misalignment | TRUE-N_Fatal < Blind_Fatal | 152.670 | 119.695 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.969 |
| Utility-Trust-Misalignment | TRUE-N_U > TTB_U | 2729.000 | 5.806 | 0.0000 | 0.0000 | 741.000 | 0.0000 | 0.0000 | 0.581 |
| Utility-Trust-Misalignment | TRUE-N_Fatal < TTB_Fatal | 10.990 | 4.603 | 0.0000 | 0.0004 | 1043.000 | 0.0000 | 0.0001 | 0.460 |
| Utility-Trust-Misalignment | TRUE-N_Collapse < TTB_Collapse | 0.030 | 14.385 | 0.0000 | 0.0000 | 26.000 | 0.0000 | 0.0000 | 1.438 |
| Utility-Trust-Misalignment | TRUE-N_A9 < Blind_A9 | -400.030 | -8.382 | 0.0000 | 0.0000 | 316.000 | 0.0000 | 0.0000 | -0.838 |

## Interpretation & Limitations

- Task flows are paired: within each run all groups see the same module sequence. Differences in outcome are therefore attributable to selection mechanisms, not task luck.
- A8 surface-quality bonus is uniform across groups. The only remaining A8 asymmetry is inside TTB's scoring function (A8 receives extra trust-objective weight), which is a *mechanism-level* difference, not an observation-level manipulation.
- Ablation results isolate component contributions: if TRUE-C is substantially worse than TRUE, the constraint filter is a key driver of advantage.
- Bonferroni correction is conservative; if a hypothesis remains significant after correction, the conclusion is robust.
- The experiment remains a probabilistic generative model; no real engineering tools are used.
