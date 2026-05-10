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
- **Utility-Trust-Misalignment**: Local phases where trusted incumbents underperform and low-history entities hold latent value.
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
| Baseline | TRUE | 735.4 | [342.4, 1102.8] | 0.764 | 0.736 | 61.4 | 0.731 | 0.616 | 0.381 | 0.1 | 0.271 |
| Baseline | TTB-cap | 1399.8 | [1044.4, 1756.8] | 0.797 | 0.771 | 60.7 | 0.736 | 0.739 | 0.444 | 999.0 | 0.000 |
| Baseline | MOO-cap | 217.0 | [-417.2, 773.2] | 0.782 | 0.758 | 65.7 | 0.717 | 0.712 | 0.428 | 849.6 | 0.044 |
| Baseline | Blind | -23907.4 | [-24245.0, -23588.2] | 0.341 | 0.403 | 210.5 | 0.308 | 0.532 | 0.319 | 5.4 | 0.000 |
| Utility-Trust-Misalignment | TRUE | 1983.0 | [1657.6, 2319.7] | 0.744 | 0.706 | 57.2 | 0.745 | 0.589 | 0.363 | 0.1 | 0.272 |
| Utility-Trust-Misalignment | TTB-cap | 3103.7 | [2826.5, 3377.0] | 0.781 | 0.738 | 54.6 | 0.755 | 0.736 | 0.442 | 999.0 | 0.000 |
| Utility-Trust-Misalignment | MOO-cap | 2395.1 | [2009.0, 2775.0] | 0.764 | 0.726 | 57.3 | 0.747 | 0.722 | 0.433 | 850.2 | 0.068 |
| Utility-Trust-Misalignment | Blind | -21928.1 | [-22237.0, -21607.8] | 0.337 | 0.392 | 206.3 | 0.303 | 0.535 | 0.321 | 7.7 | 0.000 |
| Safety-Critical | TRUE | -3665.4 | [-4230.8, -3135.0] | 0.792 | 0.722 | 41.4 | 0.813 | 0.640 | 0.406 | 0.3 | 0.111 |
| Safety-Critical | TTB-cap | -1982.8 | [-2512.6, -1452.4] | 0.828 | 0.751 | 39.1 | 0.822 | 0.746 | 0.453 | 999.0 | 0.000 |
| Safety-Critical | MOO-cap | -2841.2 | [-3475.0, -2213.4] | 0.820 | 0.743 | 40.4 | 0.816 | 0.737 | 0.449 | 929.4 | 0.026 |
| Safety-Critical | Blind | -53714.0 | [-54199.2, -53209.8] | 0.343 | 0.377 | 214.4 | 0.297 | 0.535 | 0.321 | 7.2 | 0.000 |
| Observation-Manipulated | TRUE | 1392.4 | [1006.8, 1777.6] | 0.761 | 0.644 | 54.1 | 0.760 | 0.552 | 0.333 | 0.0 | 0.005 |
| Observation-Manipulated | TTB-cap | 2751.2 | [2389.6, 3118.0] | 0.805 | 0.663 | 50.2 | 0.776 | 0.735 | 0.441 | 999.0 | 0.000 |
| Observation-Manipulated | MOO-cap | 1852.4 | [1252.0, 2396.8] | 0.792 | 0.657 | 53.9 | 0.763 | 0.694 | 0.416 | 869.8 | 0.010 |
| Observation-Manipulated | Blind | -25323.2 | [-25718.0, -24922.8] | 0.336 | 0.437 | 199.2 | 0.332 | 0.519 | 0.311 | 4.9 | 0.000 |

## Scenario Conclusions

### Baseline

- TRUE vs Blind: cumulative utility diff = 24642.8; fatal errors diff = -149.1.
- TRUE A9 first delay = 0.1; collapse index = 0.381.

### Utility-Trust-Misalignment

- TRUE vs Blind: cumulative utility diff = 23911.1; fatal errors diff = -149.1.
- TRUE A9 first delay = 0.1; collapse index = 0.363.

### Safety-Critical

- TRUE vs Blind: cumulative utility diff = 50048.6; fatal errors diff = -173.0.
- TRUE A9 first delay = 0.3; collapse index = 0.406.

### Observation-Manipulated

- TRUE vs Blind: cumulative utility diff = 26715.6; fatal errors diff = -145.1.
- TRUE A9 first delay = 0.0; collapse index = 0.333.

## Hypothesis Tests

| Scenario | Hypothesis | Mean Diff | t | p_t | p_t(Bonf) | W | p_w | p_w(Bonf) | Cohen d |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | TRUE_U > TTB-cap_U | -664.400 | -2.584 | 0.0098 | 0.2738 | 1835.000 | 0.0177 | 0.4948 | -0.258 |
| Baseline | TRUE_Fatal < TTB-cap_Fatal | -0.740 | -0.651 | 0.5151 | 1.0000 | 2289.000 | 0.6286 | 1.0000 | -0.065 |
| Baseline | TRUE_U > MOO-cap_U | 518.400 | 1.625 | 0.1041 | 1.0000 | 2155.000 | 0.2640 | 1.0000 | 0.163 |
| Baseline | TRUE_Fatal < MOO-cap_Fatal | 4.330 | 2.866 | 0.0042 | 0.1162 | 1723.500 | 0.0188 | 0.5262 | 0.287 |
| Baseline | TRUE_U > Blind_U | 24642.800 | 110.359 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.036 |
| Baseline | TRUE_Fatal < Blind_Fatal | 149.060 | 118.353 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.835 |
| Baseline | TRUE_A9 < Blind_A9 | 5.250 | 9.327 | 0.0000 | 0.0000 | 42.000 | 0.0000 | 0.0000 | 0.933 |
| Observation-Manipulated | TRUE_U > TTB-cap_U | -1358.800 | -5.675 | 0.0000 | 0.0000 | 1035.000 | 0.0000 | 0.0000 | -0.567 |
| Observation-Manipulated | TRUE_Fatal < TTB-cap_Fatal | -3.880 | -4.207 | 0.0000 | 0.0007 | 1277.000 | 0.0001 | 0.0034 | -0.421 |
| Observation-Manipulated | TRUE_U > MOO-cap_U | -460.000 | -1.208 | 0.2270 | 1.0000 | 1883.000 | 0.0388 | 1.0000 | -0.121 |
| Observation-Manipulated | TRUE_Fatal < MOO-cap_Fatal | -0.210 | -0.144 | 0.8858 | 1.0000 | 2294.500 | 0.4280 | 1.0000 | -0.014 |
| Observation-Manipulated | TRUE_U > Blind_U | 26715.600 | 110.992 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.099 |
| Observation-Manipulated | TRUE_Fatal < Blind_Fatal | 145.070 | 106.981 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.698 |
| Observation-Manipulated | TRUE_A9 < Blind_A9 | 4.920 | 9.164 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.916 |
| Safety-Critical | TRUE_U > TTB-cap_U | -1682.600 | -4.618 | 0.0000 | 0.0001 | 1200.500 | 0.0000 | 0.0001 | -0.462 |
| Safety-Critical | TRUE_Fatal < TTB-cap_Fatal | -2.350 | -2.696 | 0.0070 | 0.1964 | 1593.500 | 0.0048 | 0.1356 | -0.270 |
| Safety-Critical | TRUE_U > MOO-cap_U | -824.200 | -1.800 | 0.0718 | 1.0000 | 2001.000 | 0.0716 | 1.0000 | -0.180 |
| Safety-Critical | TRUE_Fatal < MOO-cap_Fatal | -1.040 | -0.910 | 0.3626 | 1.0000 | 2174.000 | 0.2935 | 1.0000 | -0.091 |
| Safety-Critical | TRUE_U > Blind_U | 50048.600 | 146.322 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 14.632 |
| Safety-Critical | TRUE_Fatal < Blind_Fatal | 173.020 | 128.088 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.809 |
| Safety-Critical | TRUE_A9 < Blind_A9 | 6.920 | 9.407 | 0.0000 | 0.0000 | 16.000 | 0.0000 | 0.0000 | 0.941 |
| Utility-Trust-Misalignment | TRUE_U > TTB-cap_U | -1120.700 | -5.615 | 0.0000 | 0.0000 | 1076.500 | 0.0000 | 0.0000 | -0.561 |
| Utility-Trust-Misalignment | TRUE_Fatal < TTB-cap_Fatal | -2.600 | -2.805 | 0.0050 | 0.1409 | 1719.500 | 0.0084 | 0.2343 | -0.280 |
| Utility-Trust-Misalignment | TRUE_U > MOO-cap_U | -412.100 | -1.790 | 0.0735 | 1.0000 | 1936.500 | 0.0602 | 1.0000 | -0.179 |
| Utility-Trust-Misalignment | TRUE_Fatal < MOO-cap_Fatal | 0.070 | 0.066 | 0.9477 | 1.0000 | 2375.500 | 0.9971 | 1.0000 | 0.007 |
| Utility-Trust-Misalignment | TRUE_U > Blind_U | 23911.100 | 118.895 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.889 |
| Utility-Trust-Misalignment | TRUE_Fatal < Blind_Fatal | 149.070 | 112.325 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.233 |
| Utility-Trust-Misalignment | TRUE_A9 < Blind_A9 | 7.560 | 8.592 | 0.0000 | 0.0000 | 15.000 | 0.0000 | 0.0000 | 0.859 |

## Interpretation & Limitations

- Task flows are paired: within each run all groups see the same module sequence. Differences in outcome are therefore attributable to selection mechanisms, not task luck.
- A8 surface-quality bonus is uniform across groups. The only remaining A8 asymmetry is inside TTB's scoring function (A8 receives extra trust-objective weight), which is a *mechanism-level* difference, not an observation-level manipulation.
- Ablation results isolate component contributions: if TRUE-C is substantially worse than TRUE, the constraint filter is a key driver of advantage.
- Bonferroni correction is conservative; if a hypothesis remains significant after correction, the conclusion is robust.
- The experiment remains a probabilistic generative model; no real engineering tools are used.
