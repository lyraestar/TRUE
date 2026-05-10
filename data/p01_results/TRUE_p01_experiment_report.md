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
| Safety-Critical | TRUE | -3596.2 | [-4179.6, -3014.4] | 0.796 | 0.718 | 41.7 | 0.812 | 0.654 | 0.413 | 0.3 | 0.177 |
| Safety-Critical | TRUE-C | -2034.6 | [-2543.0, -1504.4] | 0.828 | 0.744 | 39.4 | 0.822 | 0.688 | 0.420 | 0.9 | 0.000 |
| Safety-Critical | TRUE-E | -3580.0 | [-4218.2, -2915.6] | 0.796 | 0.720 | 42.0 | 0.811 | 0.657 | 0.416 | 0.6 | 0.161 |
| Safety-Critical | TRUE-N | -1677.0 | [-2187.2, -1166.4] | 0.833 | 0.746 | 38.4 | 0.824 | 0.724 | 0.440 | 959.4 | 0.000 |
| Safety-Critical | Blind | -53594.0 | [-54118.8, -53063.4] | 0.345 | 0.376 | 212.6 | 0.298 | 0.538 | 0.323 | 7.8 | 0.000 |
| Safety-Critical | TTB | -5979.4 | [-7357.8, -4786.8] | 0.782 | 0.717 | 48.4 | 0.788 | 0.733 | 0.446 | 751.6 | 0.154 |
| Safety-Critical | MOO | -4972.8 | [-5730.0, -4202.0] | 0.803 | 0.729 | 46.0 | 0.795 | 0.721 | 0.438 | 840.0 | 0.026 |
| Utility-Trust-Misalignment | TRUE | 2482.9 | [2205.5, 2761.0] | 0.750 | 0.711 | 55.2 | 0.754 | 0.619 | 0.380 | 0.2 | 0.312 |
| Utility-Trust-Misalignment | TRUE-C | 3506.0 | [3192.1, 3835.0] | 0.784 | 0.733 | 53.7 | 0.763 | 0.661 | 0.397 | 0.7 | 0.000 |
| Utility-Trust-Misalignment | TRUE-E | 2340.4 | [2023.2, 2664.0] | 0.749 | 0.708 | 55.9 | 0.752 | 0.620 | 0.381 | 0.1 | 0.278 |
| Utility-Trust-Misalignment | TRUE-N | 3022.6 | [2660.6, 3381.8] | 0.783 | 0.733 | 55.3 | 0.753 | 0.676 | 0.406 | 339.7 | 0.000 |
| Utility-Trust-Misalignment | Blind | -21783.3 | [-22110.9, -21456.9] | 0.339 | 0.397 | 206.3 | 0.306 | 0.535 | 0.321 | 6.2 | 0.000 |
| Utility-Trust-Misalignment | TTB | 167.4 | [-540.1, 793.5] | 0.727 | 0.702 | 68.0 | 0.710 | 0.722 | 0.434 | 780.2 | 0.365 |
| Utility-Trust-Misalignment | MOO | 1250.3 | [661.9, 1764.8] | 0.747 | 0.712 | 63.3 | 0.727 | 0.699 | 0.419 | 772.9 | 0.117 |
| Observation-Manipulated | TRUE | 1815.6 | [1488.4, 2130.8] | 0.769 | 0.644 | 52.5 | 0.765 | 0.605 | 0.365 | 0.0 | -0.021 |
| Observation-Manipulated | TRUE-C | 2517.2 | [2184.0, 2867.2] | 0.803 | 0.660 | 51.2 | 0.772 | 0.658 | 0.395 | 0.8 | 0.000 |
| Observation-Manipulated | TRUE-E | 2270.8 | [1973.2, 2560.4] | 0.770 | 0.645 | 51.0 | 0.773 | 0.611 | 0.368 | 0.0 | -0.012 |
| Observation-Manipulated | TRUE-N | 2596.4 | [2223.2, 2964.0] | 0.805 | 0.659 | 50.7 | 0.773 | 0.663 | 0.398 | 4.2 | 0.000 |
| Observation-Manipulated | Blind | -24965.6 | [-25318.0, -24577.2] | 0.335 | 0.437 | 196.3 | 0.338 | 0.517 | 0.310 | 7.3 | 0.000 |
| Observation-Manipulated | TTB | -28713.6 | [-29066.4, -28348.8] | 0.229 | 0.735 | 222.3 | 0.273 | 0.858 | 0.515 | 999.0 | 0.004 |
| Observation-Manipulated | MOO | -710.4 | [-1292.0, -134.8] | 0.757 | 0.638 | 66.3 | 0.723 | 0.645 | 0.387 | 594.2 | -0.001 |
| Baseline | TRUE | 1185.0 | [865.4, 1506.8] | 0.769 | 0.740 | 59.3 | 0.738 | 0.640 | 0.396 | 0.2 | 0.218 |
| Baseline | TRUE-C | 1407.6 | [1064.4, 1752.4] | 0.800 | 0.765 | 60.4 | 0.735 | 0.677 | 0.407 | 0.8 | 0.000 |
| Baseline | TRUE-E | 872.2 | [500.8, 1228.2] | 0.767 | 0.738 | 61.2 | 0.732 | 0.641 | 0.397 | 0.2 | 0.255 |
| Baseline | TRUE-N | 1570.0 | [1209.4, 1912.0] | 0.802 | 0.768 | 59.5 | 0.737 | 0.707 | 0.425 | 465.2 | 0.000 |
| Baseline | Blind | -23644.8 | [-23935.4, -23335.2] | 0.342 | 0.402 | 209.6 | 0.313 | 0.524 | 0.315 | 7.0 | 0.000 |
| Baseline | TTB | -1289.8 | [-2340.8, -369.2] | 0.741 | 0.728 | 72.0 | 0.697 | 0.727 | 0.439 | 700.4 | 0.311 |
| Baseline | MOO | -695.8 | [-1442.4, -32.0] | 0.767 | 0.740 | 69.5 | 0.702 | 0.699 | 0.420 | 790.3 | 0.095 |

## Scenario Conclusions

### Safety-Critical

- TRUE vs Blind: cumulative utility diff = 49997.8; fatal errors diff = -171.0.
- TRUE vs TTB: cumulative utility diff = 2383.2; fatal errors diff = -6.7.
- TRUE A9 first delay = 0.3; collapse index = 0.413.

### Utility-Trust-Misalignment

- TRUE vs Blind: cumulative utility diff = 24266.2; fatal errors diff = -151.2.
- TRUE vs TTB: cumulative utility diff = 2315.5; fatal errors diff = -12.8.
- TRUE A9 first delay = 0.2; collapse index = 0.380.

### Observation-Manipulated

- TRUE vs Blind: cumulative utility diff = 26781.2; fatal errors diff = -143.8.
- TRUE vs TTB: cumulative utility diff = 30529.2; fatal errors diff = -169.8.
- TRUE A9 first delay = 0.0; collapse index = 0.365.

### Baseline

- TRUE vs Blind: cumulative utility diff = 24829.8; fatal errors diff = -150.3.
- TRUE vs TTB: cumulative utility diff = 2474.8; fatal errors diff = -12.7.
- TRUE A9 first delay = 0.2; collapse index = 0.396.

## Hypothesis Tests

| Scenario | Hypothesis | Mean Diff | t | p_t | p_t(Bonf) | W | p_w | p_w(Bonf) | Cohen d |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | TRUE_U > Blind_U | 24829.800 | 123.095 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.310 |
| Baseline | TRUE_Fatal < Blind_Fatal | 150.260 | 123.373 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.337 |
| Baseline | TRUE_U > TTB_U | 2474.800 | 4.509 | 0.0000 | 0.0008 | 1220.000 | 0.0000 | 0.0009 | 0.451 |
| Baseline | TRUE_Fatal < TTB_Fatal | 12.680 | 4.506 | 0.0000 | 0.0008 | 1053.500 | 0.0000 | 0.0001 | 0.451 |
| Baseline | TRUE_U > MOO_U | 1880.800 | 4.971 | 0.0000 | 0.0001 | 952.500 | 0.0000 | 0.0000 | 0.497 |
| Baseline | TRUE_Fatal < MOO_Fatal | 10.180 | 5.699 | 0.0000 | 0.0000 | 701.500 | 0.0000 | 0.0000 | 0.570 |
| Baseline | TRUE_Collapse < TTB_Collapse | 0.044 | 19.830 | 0.0000 | 0.0000 | 1.000 | 0.0000 | 0.0000 | 1.983 |
| Baseline | TRUE_A9 < Blind_A9 | 6.800 | 10.048 | 0.0000 | 0.0000 | 14.500 | 0.0000 | 0.0000 | 1.005 |
| Baseline | TRUE-C_U > Blind_U | 25052.400 | 128.681 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.868 |
| Baseline | TRUE-C_Fatal < Blind_Fatal | 149.220 | 123.533 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.353 |
| Baseline | TRUE-C_U > TTB_U | 2697.400 | 5.142 | 0.0000 | 0.0000 | 911.500 | 0.0000 | 0.0000 | 0.514 |
| Baseline | TRUE-C_Fatal < TTB_Fatal | 11.640 | 4.240 | 0.0000 | 0.0029 | 988.000 | 0.0000 | 0.0002 | 0.424 |
| Baseline | TRUE-C_U > MOO_U | 2103.400 | 5.667 | 0.0000 | 0.0000 | 820.500 | 0.0000 | 0.0000 | 0.567 |
| Baseline | TRUE-C_Fatal < MOO_Fatal | 9.140 | 5.220 | 0.0000 | 0.0000 | 802.000 | 0.0000 | 0.0000 | 0.522 |
| Baseline | TRUE-C_Collapse < TTB_Collapse | 0.032 | 17.965 | 0.0000 | 0.0000 | 35.000 | 0.0000 | 0.0000 | 1.796 |
| Baseline | TRUE-C_A9 < Blind_A9 | 6.220 | 9.184 | 0.0000 | 0.0000 | 155.000 | 0.0000 | 0.0000 | 0.918 |
| Baseline | TRUE-E_U > Blind_U | 24517.000 | 119.214 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.921 |
| Baseline | TRUE-E_Fatal < Blind_Fatal | 148.410 | 116.791 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.679 |
| Baseline | TRUE-E_U > TTB_U | 2162.000 | 4.036 | 0.0001 | 0.0070 | 1278.500 | 0.0001 | 0.0100 | 0.404 |
| Baseline | TRUE-E_Fatal < TTB_Fatal | 10.830 | 3.956 | 0.0001 | 0.0098 | 1297.500 | 0.0000 | 0.0051 | 0.396 |
| Baseline | TRUE-E_U > MOO_U | 1568.000 | 4.056 | 0.0000 | 0.0064 | 1314.500 | 0.0000 | 0.0040 | 0.406 |
| Baseline | TRUE-E_Fatal < MOO_Fatal | 8.330 | 4.983 | 0.0000 | 0.0001 | 837.500 | 0.0000 | 0.0000 | 0.498 |
| Baseline | TRUE-E_Collapse < TTB_Collapse | 0.042 | 18.793 | 0.0000 | 0.0000 | 8.000 | 0.0000 | 0.0000 | 1.879 |
| Baseline | TRUE-E_A9 < Blind_A9 | 6.780 | 9.795 | 0.0000 | 0.0000 | 61.000 | 0.0000 | 0.0000 | 0.980 |
| Baseline | TRUE-N_U > Blind_U | 25214.800 | 125.023 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.502 |
| Baseline | TRUE-N_Fatal < Blind_Fatal | 150.140 | 125.328 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.533 |
| Baseline | TRUE-N_U > TTB_U | 2859.800 | 5.631 | 0.0000 | 0.0000 | 750.000 | 0.0000 | 0.0000 | 0.563 |
| Baseline | TRUE-N_Fatal < TTB_Fatal | 12.560 | 4.781 | 0.0000 | 0.0002 | 905.500 | 0.0000 | 0.0000 | 0.478 |
| Baseline | TRUE-N_U > MOO_U | 2265.800 | 5.787 | 0.0000 | 0.0000 | 789.500 | 0.0000 | 0.0000 | 0.579 |
| Baseline | TRUE-N_Fatal < MOO_Fatal | 10.060 | 5.345 | 0.0000 | 0.0000 | 826.500 | 0.0000 | 0.0000 | 0.534 |
| Baseline | TRUE-N_Collapse < TTB_Collapse | 0.015 | 6.861 | 0.0000 | 0.0000 | 797.000 | 0.0000 | 0.0000 | 0.686 |
| Baseline | TRUE-N_A9 < Blind_A9 | -458.150 | -9.427 | 0.0000 | 0.0000 | 346.000 | 0.0000 | 0.0000 | -0.943 |
| Observation-Manipulated | TRUE_U > Blind_U | 26781.200 | 110.026 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.003 |
| Observation-Manipulated | TRUE_Fatal < Blind_Fatal | 143.790 | 102.998 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.300 |
| Observation-Manipulated | TRUE_U > TTB_U | 30529.200 | 134.713 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.471 |
| Observation-Manipulated | TRUE_Fatal < TTB_Fatal | 169.810 | 93.740 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 9.374 |
| Observation-Manipulated | TRUE_U > MOO_U | 2526.000 | 7.737 | 0.0000 | 0.0000 | 691.500 | 0.0000 | 0.0000 | 0.774 |
| Observation-Manipulated | TRUE_Fatal < MOO_Fatal | 13.780 | 8.900 | 0.0000 | 0.0000 | 433.000 | 0.0000 | 0.0000 | 0.890 |
| Observation-Manipulated | TRUE_Collapse < TTB_Collapse | 0.151 | 145.369 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 14.537 |
| Observation-Manipulated | TRUE_A9 < Blind_A9 | 7.350 | 9.311 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.931 |
| Observation-Manipulated | TRUE-C_U > Blind_U | 27482.800 | 113.188 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.319 |
| Observation-Manipulated | TRUE-C_Fatal < Blind_Fatal | 145.150 | 110.576 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.058 |
| Observation-Manipulated | TRUE-C_U > TTB_U | 31230.800 | 137.572 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.757 |
| Observation-Manipulated | TRUE-C_Fatal < TTB_Fatal | 171.170 | 91.976 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 9.198 |
| Observation-Manipulated | TRUE-C_U > MOO_U | 3227.600 | 9.396 | 0.0000 | 0.0000 | 452.000 | 0.0000 | 0.0000 | 0.940 |
| Observation-Manipulated | TRUE-C_Fatal < MOO_Fatal | 15.140 | 9.609 | 0.0000 | 0.0000 | 363.500 | 0.0000 | 0.0000 | 0.961 |
| Observation-Manipulated | TRUE-C_Collapse < TTB_Collapse | 0.120 | 119.046 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.905 |
| Observation-Manipulated | TRUE-C_A9 < Blind_A9 | 6.570 | 8.452 | 0.0000 | 0.0000 | 82.500 | 0.0000 | 0.0000 | 0.845 |
| Observation-Manipulated | TRUE-E_U > Blind_U | 27236.400 | 130.320 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.032 |
| Observation-Manipulated | TRUE-E_Fatal < Blind_Fatal | 145.340 | 115.096 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.510 |
| Observation-Manipulated | TRUE-E_U > TTB_U | 30984.400 | 148.703 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 14.870 |
| Observation-Manipulated | TRUE-E_Fatal < TTB_Fatal | 171.360 | 94.847 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 9.485 |
| Observation-Manipulated | TRUE-E_U > MOO_U | 2981.200 | 9.453 | 0.0000 | 0.0000 | 379.000 | 0.0000 | 0.0000 | 0.945 |
| Observation-Manipulated | TRUE-E_Fatal < MOO_Fatal | 15.330 | 10.603 | 0.0000 | 0.0000 | 236.000 | 0.0000 | 0.0000 | 1.060 |
| Observation-Manipulated | TRUE-E_Collapse < TTB_Collapse | 0.147 | 128.306 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.831 |
| Observation-Manipulated | TRUE-E_A9 < Blind_A9 | 7.340 | 9.299 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.930 |
| Observation-Manipulated | TRUE-N_U > Blind_U | 27562.000 | 110.170 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.017 |
| Observation-Manipulated | TRUE-N_Fatal < Blind_Fatal | 145.590 | 101.397 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.140 |
| Observation-Manipulated | TRUE-N_U > TTB_U | 31310.000 | 138.588 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.859 |
| Observation-Manipulated | TRUE-N_Fatal < TTB_Fatal | 171.610 | 94.261 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 9.426 |
| Observation-Manipulated | TRUE-N_U > MOO_U | 3306.800 | 10.321 | 0.0000 | 0.0000 | 343.000 | 0.0000 | 0.0000 | 1.032 |
| Observation-Manipulated | TRUE-N_Fatal < MOO_Fatal | 15.580 | 10.564 | 0.0000 | 0.0000 | 297.500 | 0.0000 | 0.0000 | 1.056 |
| Observation-Manipulated | TRUE-N_Collapse < TTB_Collapse | 0.117 | 103.765 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.377 |
| Observation-Manipulated | TRUE-N_A9 < Blind_A9 | 3.170 | 3.286 | 0.0010 | 0.1300 | 1355.000 | 0.0023 | 0.2902 | 0.329 |
| Safety-Critical | TRUE_U > Blind_U | 49997.800 | 138.892 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.889 |
| Safety-Critical | TRUE_Fatal < Blind_Fatal | 170.980 | 138.188 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.819 |
| Safety-Critical | TRUE_U > TTB_U | 2383.200 | 3.355 | 0.0008 | 0.1014 | 1582.000 | 0.0018 | 0.2340 | 0.336 |
| Safety-Critical | TRUE_Fatal < TTB_Fatal | 6.720 | 3.719 | 0.0002 | 0.0256 | 1353.000 | 0.0004 | 0.0469 | 0.372 |
| Safety-Critical | TRUE_U > MOO_U | 1376.600 | 3.099 | 0.0019 | 0.2483 | 1722.000 | 0.0058 | 0.7377 | 0.310 |
| Safety-Critical | TRUE_Fatal < MOO_Fatal | 4.360 | 3.803 | 0.0001 | 0.0183 | 1441.500 | 0.0003 | 0.0396 | 0.380 |
| Safety-Critical | TRUE_Collapse < TTB_Collapse | 0.034 | 15.871 | 0.0000 | 0.0000 | 18.000 | 0.0000 | 0.0000 | 1.587 |
| Safety-Critical | TRUE_A9 < Blind_A9 | 7.480 | 7.800 | 0.0000 | 0.0000 | 49.000 | 0.0000 | 0.0000 | 0.780 |
| Safety-Critical | TRUE-C_U > Blind_U | 51559.400 | 152.508 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 15.251 |
| Safety-Critical | TRUE-C_Fatal < Blind_Fatal | 173.290 | 141.193 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 14.119 |
| Safety-Critical | TRUE-C_U > TTB_U | 3944.800 | 5.400 | 0.0000 | 0.0000 | 872.000 | 0.0000 | 0.0000 | 0.540 |
| Safety-Critical | TRUE-C_Fatal < TTB_Fatal | 9.030 | 4.939 | 0.0000 | 0.0001 | 896.000 | 0.0000 | 0.0000 | 0.494 |
| Safety-Critical | TRUE-C_U > MOO_U | 2938.200 | 6.350 | 0.0000 | 0.0000 | 937.000 | 0.0000 | 0.0000 | 0.635 |
| Safety-Critical | TRUE-C_Fatal < MOO_Fatal | 6.670 | 5.696 | 0.0000 | 0.0000 | 1003.500 | 0.0000 | 0.0001 | 0.570 |
| Safety-Critical | TRUE-C_Collapse < TTB_Collapse | 0.027 | 14.363 | 0.0000 | 0.0000 | 113.000 | 0.0000 | 0.0000 | 1.436 |
| Safety-Critical | TRUE-C_A9 < Blind_A9 | 6.900 | 7.110 | 0.0000 | 0.0000 | 155.500 | 0.0000 | 0.0000 | 0.711 |
| Safety-Critical | TRUE-E_U > Blind_U | 50014.000 | 127.770 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.777 |
| Safety-Critical | TRUE-E_Fatal < Blind_Fatal | 170.630 | 127.808 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.781 |
| Safety-Critical | TRUE-E_U > TTB_U | 2399.400 | 3.475 | 0.0005 | 0.0654 | 1473.000 | 0.0003 | 0.0381 | 0.348 |
| Safety-Critical | TRUE-E_Fatal < TTB_Fatal | 6.370 | 3.721 | 0.0002 | 0.0254 | 1313.500 | 0.0001 | 0.0104 | 0.372 |
| Safety-Critical | TRUE-E_U > MOO_U | 1392.800 | 2.619 | 0.0088 | 1.0000 | 1851.000 | 0.0205 | 1.0000 | 0.262 |
| Safety-Critical | TRUE-E_Fatal < MOO_Fatal | 4.010 | 3.031 | 0.0024 | 0.3117 | 1568.000 | 0.0055 | 0.7017 | 0.303 |
| Safety-Critical | TRUE-E_Collapse < TTB_Collapse | 0.031 | 13.817 | 0.0000 | 0.0000 | 110.000 | 0.0000 | 0.0000 | 1.382 |
| Safety-Critical | TRUE-E_A9 < Blind_A9 | 7.170 | 7.483 | 0.0000 | 0.0000 | 113.000 | 0.0000 | 0.0000 | 0.748 |
| Safety-Critical | TRUE-N_U > Blind_U | 51917.000 | 146.630 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 14.663 |
| Safety-Critical | TRUE-N_Fatal < Blind_Fatal | 174.260 | 133.615 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.361 |
| Safety-Critical | TRUE-N_U > TTB_U | 4302.400 | 6.507 | 0.0000 | 0.0000 | 700.500 | 0.0000 | 0.0000 | 0.651 |
| Safety-Critical | TRUE-N_Fatal < TTB_Fatal | 10.000 | 5.928 | 0.0000 | 0.0000 | 756.000 | 0.0000 | 0.0000 | 0.593 |
| Safety-Critical | TRUE-N_U > MOO_U | 3295.800 | 7.329 | 0.0000 | 0.0000 | 779.000 | 0.0000 | 0.0000 | 0.733 |
| Safety-Critical | TRUE-N_Fatal < MOO_Fatal | 7.640 | 6.676 | 0.0000 | 0.0000 | 806.000 | 0.0000 | 0.0000 | 0.668 |
| Safety-Critical | TRUE-N_Collapse < TTB_Collapse | 0.006 | 3.431 | 0.0006 | 0.0771 | 1556.500 | 0.0013 | 0.1724 | 0.343 |
| Safety-Critical | TRUE-N_A9 < Blind_A9 | -951.570 | -48.785 | 0.0000 | 0.0000 | 6.000 | 0.0000 | 0.0000 | -4.878 |
| Utility-Trust-Misalignment | TRUE_U > Blind_U | 24266.200 | 117.438 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.744 |
| Utility-Trust-Misalignment | TRUE_Fatal < Blind_Fatal | 151.150 | 103.420 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.342 |
| Utility-Trust-Misalignment | TRUE_U > TTB_U | 2315.500 | 5.888 | 0.0000 | 0.0000 | 766.000 | 0.0000 | 0.0000 | 0.589 |
| Utility-Trust-Misalignment | TRUE_Fatal < TTB_Fatal | 12.810 | 6.577 | 0.0000 | 0.0000 | 503.500 | 0.0000 | 0.0000 | 0.658 |
| Utility-Trust-Misalignment | TRUE_U > MOO_U | 1232.600 | 3.933 | 0.0001 | 0.0107 | 1471.000 | 0.0003 | 0.0371 | 0.393 |
| Utility-Trust-Misalignment | TRUE_Fatal < MOO_Fatal | 8.130 | 5.443 | 0.0000 | 0.0000 | 830.000 | 0.0000 | 0.0000 | 0.544 |
| Utility-Trust-Misalignment | TRUE_Collapse < TTB_Collapse | 0.054 | 23.571 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 2.357 |
| Utility-Trust-Misalignment | TRUE_A9 < Blind_A9 | 6.030 | 9.333 | 0.0000 | 0.0000 | 23.000 | 0.0000 | 0.0000 | 0.933 |
| Utility-Trust-Misalignment | TRUE-C_U > Blind_U | 25289.300 | 133.453 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.345 |
| Utility-Trust-Misalignment | TRUE-C_Fatal < Blind_Fatal | 152.630 | 105.806 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.581 |
| Utility-Trust-Misalignment | TRUE-C_U > TTB_U | 3338.600 | 8.438 | 0.0000 | 0.0000 | 299.000 | 0.0000 | 0.0000 | 0.844 |
| Utility-Trust-Misalignment | TRUE-C_Fatal < TTB_Fatal | 14.290 | 7.412 | 0.0000 | 0.0000 | 441.500 | 0.0000 | 0.0000 | 0.741 |
| Utility-Trust-Misalignment | TRUE-C_U > MOO_U | 2255.700 | 7.136 | 0.0000 | 0.0000 | 632.500 | 0.0000 | 0.0000 | 0.714 |
| Utility-Trust-Misalignment | TRUE-C_Fatal < MOO_Fatal | 9.610 | 6.081 | 0.0000 | 0.0000 | 810.500 | 0.0000 | 0.0000 | 0.608 |
| Utility-Trust-Misalignment | TRUE-C_Collapse < TTB_Collapse | 0.037 | 23.531 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 2.353 |
| Utility-Trust-Misalignment | TRUE-C_A9 < Blind_A9 | 5.450 | 8.429 | 0.0000 | 0.0000 | 85.000 | 0.0000 | 0.0000 | 0.843 |
| Utility-Trust-Misalignment | TRUE-E_U > Blind_U | 24123.700 | 110.213 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.021 |
| Utility-Trust-Misalignment | TRUE-E_Fatal < Blind_Fatal | 150.410 | 103.130 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.313 |
| Utility-Trust-Misalignment | TRUE-E_U > TTB_U | 2173.000 | 6.268 | 0.0000 | 0.0000 | 699.500 | 0.0000 | 0.0000 | 0.627 |
| Utility-Trust-Misalignment | TRUE-E_Fatal < TTB_Fatal | 12.070 | 6.578 | 0.0000 | 0.0000 | 652.500 | 0.0000 | 0.0000 | 0.658 |
| Utility-Trust-Misalignment | TRUE-E_U > MOO_U | 1090.100 | 3.523 | 0.0004 | 0.0546 | 1513.500 | 0.0005 | 0.0647 | 0.352 |
| Utility-Trust-Misalignment | TRUE-E_Fatal < MOO_Fatal | 7.390 | 4.921 | 0.0000 | 0.0001 | 1033.000 | 0.0000 | 0.0003 | 0.492 |
| Utility-Trust-Misalignment | TRUE-E_Collapse < TTB_Collapse | 0.053 | 22.307 | 0.0000 | 0.0000 | 1.000 | 0.0000 | 0.0000 | 2.231 |
| Utility-Trust-Misalignment | TRUE-E_A9 < Blind_A9 | 6.070 | 9.492 | 0.0000 | 0.0000 | 25.000 | 0.0000 | 0.0000 | 0.949 |
| Utility-Trust-Misalignment | TRUE-N_U > Blind_U | 24805.900 | 106.336 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.634 |
| Utility-Trust-Misalignment | TRUE-N_Fatal < Blind_Fatal | 151.040 | 103.844 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.384 |
| Utility-Trust-Misalignment | TRUE-N_U > TTB_U | 2855.200 | 6.968 | 0.0000 | 0.0000 | 551.000 | 0.0000 | 0.0000 | 0.697 |
| Utility-Trust-Misalignment | TRUE-N_Fatal < TTB_Fatal | 12.700 | 6.266 | 0.0000 | 0.0000 | 608.500 | 0.0000 | 0.0000 | 0.627 |
| Utility-Trust-Misalignment | TRUE-N_U > MOO_U | 1772.300 | 5.347 | 0.0000 | 0.0000 | 984.000 | 0.0000 | 0.0000 | 0.535 |
| Utility-Trust-Misalignment | TRUE-N_Fatal < MOO_Fatal | 8.020 | 5.003 | 0.0000 | 0.0001 | 1087.000 | 0.0000 | 0.0002 | 0.500 |
| Utility-Trust-Misalignment | TRUE-N_Collapse < TTB_Collapse | 0.029 | 12.783 | 0.0000 | 0.0000 | 84.000 | 0.0000 | 0.0000 | 1.278 |
| Utility-Trust-Misalignment | TRUE-N_A9 < Blind_A9 | -333.530 | -7.314 | 0.0000 | 0.0000 | 374.000 | 0.0000 | 0.0000 | -0.731 |

## Interpretation & Limitations

- Task flows are paired: within each run all groups see the same module sequence. Differences in outcome are therefore attributable to selection mechanisms, not task luck.
- A8 surface-quality bonus is uniform across groups. The only remaining A8 asymmetry is inside TTB's scoring function (A8 receives extra trust-objective weight), which is a *mechanism-level* difference, not an observation-level manipulation.
- Ablation results isolate component contributions: if TRUE-C is substantially worse than TRUE, the constraint filter is a key driver of advantage.
- Bonferroni correction is conservative; if a hypothesis remains significant after correction, the conclusion is robust.
- The experiment remains a probabilistic generative model; no real engineering tools are used.
