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

- **Observation-Manipulated**: Observation-contaminated environment where surface quality can diverge from true quality.
- **Utility-Trust-Misalignment**: Local phases where trusted incumbents underperform and low-history entities hold latent value.
- **Baseline**: Standard engineering collaboration with moderate observation noise.
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
| Observation-Manipulated | TRUE | 2472.4 | [2116.8, 2797.6] | 0.775 | 0.643 | 50.5 | 0.776 | 0.649 | 0.391 | 0.0 | -0.035 |
| Observation-Manipulated | TTB-cap | 3069.2 | [2741.2, 3373.6] | 0.808 | 0.657 | 49.6 | 0.780 | 0.734 | 0.441 | 999.0 | 0.000 |
| Observation-Manipulated | MOO-cap | 945.2 | [254.0, 1588.0] | 0.784 | 0.656 | 57.6 | 0.749 | 0.681 | 0.408 | 820.0 | -0.011 |
| Observation-Manipulated | Blind | -25584.8 | [-25971.2, -25198.4] | 0.335 | 0.439 | 199.9 | 0.327 | 0.521 | 0.313 | 6.8 | 0.000 |
| Utility-Trust-Misalignment | TRUE | 2410.6 | [2142.1, 2673.9] | 0.751 | 0.711 | 55.8 | 0.751 | 0.643 | 0.396 | 0.1 | 0.368 |
| Utility-Trust-Misalignment | TTB-cap | 2944.5 | [2650.3, 3244.7] | 0.780 | 0.736 | 55.8 | 0.753 | 0.737 | 0.442 | 999.0 | 0.000 |
| Utility-Trust-Misalignment | MOO-cap | 2217.8 | [1764.1, 2669.3] | 0.764 | 0.724 | 58.1 | 0.743 | 0.719 | 0.432 | 879.4 | 0.069 |
| Utility-Trust-Misalignment | Blind | -21928.1 | [-22237.0, -21607.8] | 0.337 | 0.392 | 206.3 | 0.303 | 0.535 | 0.321 | 7.7 | 0.000 |
| Baseline | TRUE | 1186.4 | [826.4, 1557.4] | 0.769 | 0.737 | 60.2 | 0.738 | 0.655 | 0.404 | 0.1 | 0.225 |
| Baseline | TTB-cap | 1745.2 | [1412.8, 2094.4] | 0.802 | 0.764 | 59.0 | 0.741 | 0.738 | 0.443 | 999.0 | 0.000 |
| Baseline | MOO-cap | 943.4 | [447.4, 1434.0] | 0.786 | 0.751 | 61.6 | 0.730 | 0.722 | 0.433 | 889.8 | 0.033 |
| Baseline | Blind | -23786.6 | [-24119.4, -23454.2] | 0.342 | 0.400 | 209.5 | 0.310 | 0.530 | 0.318 | 6.5 | 0.000 |
| Safety-Critical | TRUE | -2829.2 | [-3384.6, -2266.0] | 0.799 | 0.720 | 40.2 | 0.820 | 0.666 | 0.420 | 0.1 | 0.105 |
| Safety-Critical | TTB-cap | -2041.0 | [-2560.6, -1559.0] | 0.828 | 0.744 | 38.9 | 0.822 | 0.744 | 0.452 | 999.0 | 0.000 |
| Safety-Critical | MOO-cap | -3140.4 | [-4040.8, -2319.2] | 0.816 | 0.736 | 41.9 | 0.813 | 0.733 | 0.446 | 929.6 | 0.026 |
| Safety-Critical | Blind | -53395.8 | [-53891.0, -52908.2] | 0.343 | 0.377 | 213.3 | 0.300 | 0.537 | 0.322 | 6.2 | 0.000 |

## Scenario Conclusions

### Observation-Manipulated

- TRUE vs Blind: cumulative utility diff = 28057.2; fatal errors diff = -149.4.
- TRUE A9 first delay = 0.0; collapse index = 0.391.

### Utility-Trust-Misalignment

- TRUE vs Blind: cumulative utility diff = 24338.7; fatal errors diff = -150.5.
- TRUE A9 first delay = 0.1; collapse index = 0.396.

### Baseline

- TRUE vs Blind: cumulative utility diff = 24973.0; fatal errors diff = -149.3.
- TRUE A9 first delay = 0.1; collapse index = 0.404.

### Safety-Critical

- TRUE vs Blind: cumulative utility diff = 50566.6; fatal errors diff = -173.1.
- TRUE A9 first delay = 0.1; collapse index = 0.420.

## Hypothesis Tests

| Scenario | Hypothesis | Mean Diff | t | p_t | p_t(Bonf) | W | p_w | p_w(Bonf) | Cohen d |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | TRUE_U > TTB-cap_U | -558.800 | -2.733 | 0.0063 | 0.1759 | 1825.500 | 0.0162 | 0.4527 | -0.273 |
| Baseline | TRUE_Fatal < TTB-cap_Fatal | -1.170 | -1.309 | 0.1905 | 1.0000 | 1828.500 | 0.2266 | 1.0000 | -0.131 |
| Baseline | TRUE_U > MOO-cap_U | 243.000 | 0.764 | 0.4447 | 1.0000 | 2498.500 | 0.9274 | 1.0000 | 0.076 |
| Baseline | TRUE_Fatal < MOO-cap_Fatal | 1.430 | 1.085 | 0.2777 | 1.0000 | 2245.500 | 0.5236 | 1.0000 | 0.109 |
| Baseline | TRUE_U > Blind_U | 24973.000 | 111.816 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.182 |
| Baseline | TRUE_Fatal < Blind_Fatal | 149.310 | 114.538 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.454 |
| Baseline | TRUE_A9 < Blind_A9 | 6.400 | 8.924 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.892 |
| Observation-Manipulated | TRUE_U > TTB-cap_U | -596.800 | -2.672 | 0.0075 | 0.2113 | 1778.500 | 0.0103 | 0.2875 | -0.267 |
| Observation-Manipulated | TRUE_Fatal < TTB-cap_Fatal | -0.940 | -1.087 | 0.2769 | 1.0000 | 1910.000 | 0.2239 | 1.0000 | -0.109 |
| Observation-Manipulated | TRUE_U > MOO-cap_U | 1527.200 | 4.130 | 0.0000 | 0.0010 | 1240.500 | 0.0000 | 0.0005 | 0.413 |
| Observation-Manipulated | TRUE_Fatal < MOO-cap_Fatal | 7.070 | 4.729 | 0.0000 | 0.0001 | 1094.500 | 0.0000 | 0.0001 | 0.473 |
| Observation-Manipulated | TRUE_U > Blind_U | 28057.200 | 125.526 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.553 |
| Observation-Manipulated | TRUE_Fatal < Blind_Fatal | 149.390 | 116.326 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.633 |
| Observation-Manipulated | TRUE_A9 < Blind_A9 | 6.840 | 8.926 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.893 |
| Safety-Critical | TRUE_U > TTB-cap_U | -788.200 | -2.067 | 0.0388 | 1.0000 | 1988.000 | 0.0648 | 1.0000 | -0.207 |
| Safety-Critical | TRUE_Fatal < TTB-cap_Fatal | -1.370 | -1.436 | 0.1510 | 1.0000 | 2077.000 | 0.2812 | 1.0000 | -0.144 |
| Safety-Critical | TRUE_U > MOO-cap_U | 311.200 | 0.594 | 0.5523 | 1.0000 | 2470.500 | 0.9875 | 1.0000 | 0.059 |
| Safety-Critical | TRUE_Fatal < MOO-cap_Fatal | 1.670 | 1.247 | 0.2125 | 1.0000 | 2219.000 | 0.4643 | 1.0000 | 0.125 |
| Safety-Critical | TRUE_U > Blind_U | 50566.600 | 145.551 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 14.555 |
| Safety-Critical | TRUE_Fatal < Blind_Fatal | 173.060 | 134.453 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.445 |
| Safety-Critical | TRUE_A9 < Blind_A9 | 6.090 | 8.231 | 0.0000 | 0.0000 | 28.500 | 0.0000 | 0.0000 | 0.823 |
| Utility-Trust-Misalignment | TRUE_U > TTB-cap_U | -533.900 | -2.609 | 0.0091 | 0.2543 | 1844.500 | 0.0278 | 0.7773 | -0.261 |
| Utility-Trust-Misalignment | TRUE_Fatal < TTB-cap_Fatal | -0.080 | -0.091 | 0.9276 | 1.0000 | 2395.500 | 0.7814 | 1.0000 | -0.009 |
| Utility-Trust-Misalignment | TRUE_U > MOO-cap_U | 192.800 | 0.769 | 0.4421 | 1.0000 | 2374.000 | 0.7244 | 1.0000 | 0.077 |
| Utility-Trust-Misalignment | TRUE_Fatal < MOO-cap_Fatal | 2.240 | 2.011 | 0.0444 | 1.0000 | 1918.500 | 0.1796 | 1.0000 | 0.201 |
| Utility-Trust-Misalignment | TRUE_U > Blind_U | 24338.700 | 113.805 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.380 |
| Utility-Trust-Misalignment | TRUE_Fatal < Blind_Fatal | 150.470 | 104.365 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.437 |
| Utility-Trust-Misalignment | TRUE_A9 < Blind_A9 | 7.620 | 8.568 | 0.0000 | 0.0000 | 10.000 | 0.0000 | 0.0000 | 0.857 |

## Interpretation & Limitations

- Task flows are paired: within each run all groups see the same module sequence. Differences in outcome are therefore attributable to selection mechanisms, not task luck.
- A8 surface-quality bonus is uniform across groups. The only remaining A8 asymmetry is inside TTB's scoring function (A8 receives extra trust-objective weight), which is a *mechanism-level* difference, not an observation-level manipulation.
- Ablation results isolate component contributions: if TRUE-C is substantially worse than TRUE, the constraint filter is a key driver of advantage.
- Bonferroni correction is conservative; if a hypothesis remains significant after correction, the conclusion is robust.
- The experiment remains a probabilistic generative model; no real engineering tools are used.
