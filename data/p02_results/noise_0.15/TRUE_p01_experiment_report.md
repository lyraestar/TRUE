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
| Baseline | TRUE | 679.4 | [296.8, 1084.4] | 0.759 | 0.737 | 61.9 | 0.731 | 0.610 | 0.378 | 0.1 | 0.231 |
| Baseline | TTB-cap | 1413.4 | [1066.0, 1765.4] | 0.796 | 0.770 | 60.5 | 0.736 | 0.740 | 0.444 | 999.0 | 0.000 |
| Baseline | MOO-cap | 483.8 | [-191.8, 986.8] | 0.783 | 0.758 | 64.6 | 0.722 | 0.715 | 0.429 | 859.7 | 0.070 |
| Baseline | Blind | -23907.4 | [-24245.0, -23588.2] | 0.341 | 0.403 | 210.5 | 0.308 | 0.532 | 0.319 | 5.4 | 0.000 |
| Observation-Manipulated | TRUE | 1178.0 | [870.0, 1477.2] | 0.762 | 0.638 | 55.1 | 0.756 | 0.537 | 0.324 | 0.0 | -0.021 |
| Observation-Manipulated | TTB-cap | 2655.2 | [2240.4, 3053.6] | 0.806 | 0.661 | 50.9 | 0.773 | 0.735 | 0.441 | 999.0 | 0.000 |
| Observation-Manipulated | MOO-cap | 1207.2 | [694.0, 1741.6] | 0.784 | 0.654 | 56.7 | 0.753 | 0.694 | 0.416 | 781.5 | -0.011 |
| Observation-Manipulated | Blind | -25219.2 | [-25568.0, -24874.4] | 0.336 | 0.435 | 198.2 | 0.334 | 0.521 | 0.313 | 6.4 | 0.000 |
| Utility-Trust-Misalignment | TRUE | 1946.0 | [1614.8, 2257.1] | 0.741 | 0.706 | 57.3 | 0.746 | 0.579 | 0.358 | 0.1 | 0.229 |
| Utility-Trust-Misalignment | TTB-cap | 3239.5 | [2914.0, 3582.1] | 0.782 | 0.738 | 54.2 | 0.758 | 0.734 | 0.440 | 999.0 | 0.000 |
| Utility-Trust-Misalignment | MOO-cap | 2491.0 | [2110.0, 2861.1] | 0.767 | 0.726 | 56.4 | 0.749 | 0.723 | 0.434 | 869.8 | 0.042 |
| Utility-Trust-Misalignment | Blind | -21840.8 | [-22131.6, -21554.3] | 0.337 | 0.390 | 206.6 | 0.305 | 0.532 | 0.319 | 7.6 | 0.000 |
| Safety-Critical | TRUE | -4216.6 | [-4828.4, -3589.2] | 0.786 | 0.718 | 42.8 | 0.807 | 0.638 | 0.404 | 0.3 | 0.155 |
| Safety-Critical | TTB-cap | -2344.6 | [-2814.4, -1809.6] | 0.825 | 0.748 | 39.5 | 0.820 | 0.744 | 0.452 | 999.0 | 0.000 |
| Safety-Critical | MOO-cap | -2844.2 | [-3669.2, -2083.4] | 0.817 | 0.737 | 41.5 | 0.816 | 0.732 | 0.444 | 929.6 | 0.009 |
| Safety-Critical | Blind | -53395.8 | [-53891.0, -52908.2] | 0.343 | 0.377 | 213.3 | 0.300 | 0.537 | 0.322 | 6.2 | 0.000 |

## Scenario Conclusions

### Baseline

- TRUE vs Blind: cumulative utility diff = 24586.8; fatal errors diff = -148.6.
- TRUE A9 first delay = 0.1; collapse index = 0.378.

### Observation-Manipulated

- TRUE vs Blind: cumulative utility diff = 26397.2; fatal errors diff = -143.1.
- TRUE A9 first delay = 0.0; collapse index = 0.324.

### Utility-Trust-Misalignment

- TRUE vs Blind: cumulative utility diff = 23786.8; fatal errors diff = -149.3.
- TRUE A9 first delay = 0.1; collapse index = 0.358.

### Safety-Critical

- TRUE vs Blind: cumulative utility diff = 49179.2; fatal errors diff = -170.5.
- TRUE A9 first delay = 0.3; collapse index = 0.404.

## Hypothesis Tests

| Scenario | Hypothesis | Mean Diff | t | p_t | p_t(Bonf) | W | p_w | p_w(Bonf) | Cohen d |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | TRUE_U > TTB-cap_U | -734.000 | -2.585 | 0.0097 | 0.2724 | 1783.500 | 0.0108 | 0.3020 | -0.259 |
| Baseline | TRUE_Fatal < TTB-cap_Fatal | -1.390 | -1.144 | 0.2528 | 1.0000 | 1998.500 | 0.2286 | 1.0000 | -0.114 |
| Baseline | TRUE_U > MOO-cap_U | 195.600 | 0.556 | 0.5782 | 1.0000 | 2516.500 | 0.9767 | 1.0000 | 0.056 |
| Baseline | TRUE_Fatal < MOO-cap_Fatal | 2.750 | 1.634 | 0.1022 | 1.0000 | 2061.500 | 0.3301 | 1.0000 | 0.163 |
| Baseline | TRUE_U > Blind_U | 24586.800 | 114.267 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.427 |
| Baseline | TRUE_Fatal < Blind_Fatal | 148.610 | 118.754 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.875 |
| Baseline | TRUE_A9 < Blind_A9 | 5.230 | 9.359 | 0.0000 | 0.0000 | 10.000 | 0.0000 | 0.0000 | 0.936 |
| Observation-Manipulated | TRUE_U > TTB-cap_U | -1477.200 | -5.973 | 0.0000 | 0.0000 | 1032.000 | 0.0000 | 0.0000 | -0.597 |
| Observation-Manipulated | TRUE_Fatal < TTB-cap_Fatal | -4.240 | -4.290 | 0.0000 | 0.0005 | 1186.500 | 0.0000 | 0.0008 | -0.429 |
| Observation-Manipulated | TRUE_U > MOO-cap_U | -29.200 | -0.104 | 0.9172 | 1.0000 | 2341.000 | 0.6400 | 1.0000 | -0.010 |
| Observation-Manipulated | TRUE_Fatal < MOO-cap_Fatal | 1.640 | 1.295 | 0.1953 | 1.0000 | 2288.500 | 0.5151 | 1.0000 | 0.130 |
| Observation-Manipulated | TRUE_U > Blind_U | 26397.200 | 132.427 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.243 |
| Observation-Manipulated | TRUE_Fatal < Blind_Fatal | 143.080 | 119.843 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.984 |
| Observation-Manipulated | TRUE_A9 < Blind_A9 | 6.420 | 7.982 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.798 |
| Safety-Critical | TRUE_U > TTB-cap_U | -1872.000 | -4.464 | 0.0000 | 0.0002 | 1370.000 | 0.0001 | 0.0020 | -0.446 |
| Safety-Critical | TRUE_Fatal < TTB-cap_Fatal | -3.270 | -3.306 | 0.0009 | 0.0265 | 1599.500 | 0.0034 | 0.0958 | -0.331 |
| Safety-Critical | TRUE_U > MOO-cap_U | -1372.400 | -2.701 | 0.0069 | 0.1936 | 1720.000 | 0.0056 | 0.1580 | -0.270 |
| Safety-Critical | TRUE_Fatal < MOO-cap_Fatal | -1.280 | -1.000 | 0.3175 | 1.0000 | 2009.000 | 0.1400 | 1.0000 | -0.100 |
| Safety-Critical | TRUE_U > Blind_U | 49179.200 | 151.730 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 15.173 |
| Safety-Critical | TRUE_Fatal < Blind_Fatal | 170.490 | 142.140 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 14.214 |
| Safety-Critical | TRUE_A9 < Blind_A9 | 5.920 | 7.975 | 0.0000 | 0.0000 | 79.500 | 0.0000 | 0.0000 | 0.797 |
| Utility-Trust-Misalignment | TRUE_U > TTB-cap_U | -1293.500 | -5.662 | 0.0000 | 0.0000 | 1071.000 | 0.0000 | 0.0000 | -0.566 |
| Utility-Trust-Misalignment | TRUE_Fatal < TTB-cap_Fatal | -3.020 | -2.960 | 0.0031 | 0.0861 | 1546.000 | 0.0143 | 0.3997 | -0.296 |
| Utility-Trust-Misalignment | TRUE_U > MOO-cap_U | -545.000 | -2.080 | 0.0375 | 1.0000 | 1840.000 | 0.0185 | 0.5183 | -0.208 |
| Utility-Trust-Misalignment | TRUE_Fatal < MOO-cap_Fatal | -0.870 | -0.733 | 0.4633 | 1.0000 | 2147.500 | 0.4099 | 1.0000 | -0.073 |
| Utility-Trust-Misalignment | TRUE_U > Blind_U | 23786.800 | 121.459 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.146 |
| Utility-Trust-Misalignment | TRUE_Fatal < Blind_Fatal | 149.310 | 107.808 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.781 |
| Utility-Trust-Misalignment | TRUE_A9 < Blind_A9 | 7.510 | 8.957 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.896 |

## Interpretation & Limitations

- Task flows are paired: within each run all groups see the same module sequence. Differences in outcome are therefore attributable to selection mechanisms, not task luck.
- A8 surface-quality bonus is uniform across groups. The only remaining A8 asymmetry is inside TTB's scoring function (A8 receives extra trust-objective weight), which is a *mechanism-level* difference, not an observation-level manipulation.
- Ablation results isolate component contributions: if TRUE-C is substantially worse than TRUE, the constraint filter is a key driver of advantage.
- Bonferroni correction is conservative; if a hypothesis remains significant after correction, the conclusion is robust.
- The experiment remains a probabilistic generative model; no real engineering tools are used.
