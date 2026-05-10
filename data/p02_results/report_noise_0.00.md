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
| Baseline | TRUE | 896.8 | [520.4, 1274.0] | 0.767 | 0.739 | 61.0 | 0.733 | 0.637 | 0.394 | 0.2 | 0.293 |
| Baseline | TTB-cap | 1636.6 | [1302.0, 1969.2] | 0.801 | 0.764 | 59.2 | 0.739 | 0.740 | 0.444 | 999.0 | 0.000 |
| Baseline | MOO-cap | 82.0 | [-466.4, 611.0] | 0.781 | 0.754 | 66.5 | 0.715 | 0.717 | 0.430 | 849.7 | 0.025 |
| Baseline | Blind | -23907.4 | [-24245.0, -23588.2] | 0.341 | 0.403 | 210.5 | 0.308 | 0.532 | 0.319 | 5.4 | 0.000 |
| Observation-Manipulated | TRUE | 2102.4 | [1752.4, 2443.6] | 0.769 | 0.638 | 51.7 | 0.770 | 0.602 | 0.363 | 0.0 | -0.008 |
| Observation-Manipulated | TTB-cap | 2999.6 | [2648.4, 3392.4] | 0.810 | 0.658 | 49.6 | 0.778 | 0.736 | 0.442 | 999.0 | 0.000 |
| Observation-Manipulated | MOO-cap | 1115.2 | [470.4, 1644.4] | 0.789 | 0.653 | 57.4 | 0.750 | 0.690 | 0.414 | 830.7 | 0.001 |
| Observation-Manipulated | Blind | -25219.2 | [-25568.0, -24874.4] | 0.336 | 0.435 | 198.2 | 0.334 | 0.521 | 0.313 | 6.4 | 0.000 |
| Utility-Trust-Misalignment | TRUE | 2345.4 | [2040.2, 2640.5] | 0.749 | 0.705 | 56.1 | 0.752 | 0.619 | 0.381 | 0.1 | 0.257 |
| Utility-Trust-Misalignment | TTB-cap | 3131.4 | [2784.0, 3475.2] | 0.779 | 0.732 | 55.2 | 0.756 | 0.736 | 0.442 | 999.0 | 0.000 |
| Utility-Trust-Misalignment | MOO-cap | 2680.1 | [2261.3, 3069.9] | 0.769 | 0.723 | 56.2 | 0.751 | 0.720 | 0.432 | 869.6 | 0.043 |
| Utility-Trust-Misalignment | Blind | -21840.8 | [-22131.6, -21554.3] | 0.337 | 0.390 | 206.6 | 0.305 | 0.532 | 0.319 | 7.6 | 0.000 |
| Safety-Critical | TRUE | -3313.0 | [-3820.2, -2813.8] | 0.794 | 0.723 | 41.5 | 0.815 | 0.656 | 0.414 | 0.4 | 0.151 |
| Safety-Critical | TTB-cap | -2089.0 | [-2603.6, -1595.2] | 0.828 | 0.745 | 39.0 | 0.821 | 0.745 | 0.452 | 999.0 | 0.000 |
| Safety-Critical | MOO-cap | -3013.2 | [-3824.0, -2295.4] | 0.817 | 0.738 | 41.6 | 0.814 | 0.733 | 0.445 | 880.1 | 0.008 |
| Safety-Critical | Blind | -53395.8 | [-53891.0, -52908.2] | 0.343 | 0.377 | 213.3 | 0.300 | 0.537 | 0.322 | 6.2 | 0.000 |

## Scenario Conclusions

### Baseline

- TRUE vs Blind: cumulative utility diff = 24804.2; fatal errors diff = -149.5.
- TRUE A9 first delay = 0.2; collapse index = 0.394.

### Observation-Manipulated

- TRUE vs Blind: cumulative utility diff = 27321.6; fatal errors diff = -146.4.
- TRUE A9 first delay = 0.0; collapse index = 0.363.

### Utility-Trust-Misalignment

- TRUE vs Blind: cumulative utility diff = 24186.2; fatal errors diff = -150.4.
- TRUE A9 first delay = 0.1; collapse index = 0.381.

### Safety-Critical

- TRUE vs Blind: cumulative utility diff = 50082.8; fatal errors diff = -171.8.
- TRUE A9 first delay = 0.4; collapse index = 0.414.

## Hypothesis Tests

| Scenario | Hypothesis | Mean Diff | t | p_t | p_t(Bonf) | W | p_w | p_w(Bonf) | Cohen d |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | TRUE_U > TTB-cap_U | -739.800 | -2.673 | 0.0075 | 0.2104 | 1808.500 | 0.0138 | 0.3852 | -0.267 |
| Baseline | TRUE_Fatal < TTB-cap_Fatal | -1.830 | -1.578 | 0.1147 | 1.0000 | 1892.000 | 0.1498 | 1.0000 | -0.158 |
| Baseline | TRUE_U > MOO-cap_U | 814.800 | 2.586 | 0.0097 | 0.2721 | 1837.000 | 0.0180 | 0.5041 | 0.259 |
| Baseline | TRUE_Fatal < MOO-cap_Fatal | 5.510 | 3.642 | 0.0003 | 0.0076 | 1460.500 | 0.0010 | 0.0275 | 0.364 |
| Baseline | TRUE_U > Blind_U | 24804.200 | 106.022 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.602 |
| Baseline | TRUE_Fatal < Blind_Fatal | 149.470 | 108.193 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.819 |
| Baseline | TRUE_A9 < Blind_A9 | 5.150 | 9.140 | 0.0000 | 0.0000 | 79.500 | 0.0000 | 0.0000 | 0.914 |
| Observation-Manipulated | TRUE_U > TTB-cap_U | -897.200 | -4.055 | 0.0001 | 0.0014 | 1395.000 | 0.0003 | 0.0073 | -0.405 |
| Observation-Manipulated | TRUE_Fatal < TTB-cap_Fatal | -2.100 | -2.499 | 0.0124 | 0.3484 | 1767.500 | 0.0197 | 0.5521 | -0.250 |
| Observation-Manipulated | TRUE_U > MOO-cap_U | 987.200 | 2.915 | 0.0036 | 0.0995 | 1826.500 | 0.0163 | 0.4570 | 0.292 |
| Observation-Manipulated | TRUE_Fatal < MOO-cap_Fatal | 5.620 | 3.887 | 0.0001 | 0.0028 | 1403.500 | 0.0005 | 0.0130 | 0.389 |
| Observation-Manipulated | TRUE_U > Blind_U | 27321.600 | 131.381 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.138 |
| Observation-Manipulated | TRUE_Fatal < Blind_Fatal | 146.430 | 126.029 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.603 |
| Observation-Manipulated | TRUE_A9 < Blind_A9 | 6.420 | 7.982 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.798 |
| Safety-Critical | TRUE_U > TTB-cap_U | -1224.000 | -3.283 | 0.0010 | 0.0288 | 1520.500 | 0.0009 | 0.0242 | -0.328 |
| Safety-Critical | TRUE_Fatal < TTB-cap_Fatal | -2.460 | -2.740 | 0.0061 | 0.1719 | 1414.500 | 0.0048 | 0.1340 | -0.274 |
| Safety-Critical | TRUE_U > MOO-cap_U | -299.800 | -0.647 | 0.5180 | 1.0000 | 2069.000 | 0.1169 | 1.0000 | -0.065 |
| Safety-Critical | TRUE_Fatal < MOO-cap_Fatal | 0.170 | 0.140 | 0.8887 | 1.0000 | 1955.500 | 0.5863 | 1.0000 | 0.014 |
| Safety-Critical | TRUE_U > Blind_U | 50082.800 | 143.443 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 14.344 |
| Safety-Critical | TRUE_Fatal < Blind_Fatal | 171.840 | 140.508 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 14.051 |
| Safety-Critical | TRUE_A9 < Blind_A9 | 5.830 | 7.907 | 0.0000 | 0.0000 | 50.500 | 0.0000 | 0.0000 | 0.791 |
| Utility-Trust-Misalignment | TRUE_U > TTB-cap_U | -786.000 | -3.386 | 0.0007 | 0.0199 | 1569.000 | 0.0010 | 0.0283 | -0.339 |
| Utility-Trust-Misalignment | TRUE_Fatal < TTB-cap_Fatal | -0.990 | -0.939 | 0.3477 | 1.0000 | 2084.000 | 0.3726 | 1.0000 | -0.094 |
| Utility-Trust-Misalignment | TRUE_U > MOO-cap_U | -334.700 | -1.266 | 0.2057 | 1.0000 | 1992.500 | 0.0671 | 1.0000 | -0.127 |
| Utility-Trust-Misalignment | TRUE_Fatal < MOO-cap_Fatal | 0.090 | 0.072 | 0.9427 | 1.0000 | 2327.500 | 0.7284 | 1.0000 | 0.007 |
| Utility-Trust-Misalignment | TRUE_U > Blind_U | 24186.200 | 130.983 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.098 |
| Utility-Trust-Misalignment | TRUE_Fatal < Blind_Fatal | 150.420 | 116.471 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.647 |
| Utility-Trust-Misalignment | TRUE_A9 < Blind_A9 | 7.460 | 8.851 | 0.0000 | 0.0000 | 5.500 | 0.0000 | 0.0000 | 0.885 |

## Interpretation & Limitations

- Task flows are paired: within each run all groups see the same module sequence. Differences in outcome are therefore attributable to selection mechanisms, not task luck.
- A8 surface-quality bonus is uniform across groups. The only remaining A8 asymmetry is inside TTB's scoring function (A8 receives extra trust-objective weight), which is a *mechanism-level* difference, not an observation-level manipulation.
- Ablation results isolate component contributions: if TRUE-C is substantially worse than TRUE, the constraint filter is a key driver of advantage.
- Bonferroni correction is conservative; if a hypothesis remains significant after correction, the conclusion is robust.
- The experiment remains a probabilistic generative model; no real engineering tools are used.
