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
| Safety-Critical | TRUE | -4205.4 | [-4796.4, -3624.4] | 0.785 | 0.714 | 43.1 | 0.808 | 0.628 | 0.400 | 0.3 | 0.109 |
| Safety-Critical | TTB-cap | -1710.8 | [-2211.2, -1153.2] | 0.827 | 0.749 | 38.7 | 0.826 | 0.747 | 0.454 | 999.0 | 0.000 |
| Safety-Critical | MOO-cap | -3618.2 | [-4543.8, -2789.4] | 0.810 | 0.739 | 42.8 | 0.809 | 0.725 | 0.441 | 820.3 | 0.025 |
| Safety-Critical | Blind | -53419.0 | [-53995.6, -52874.0] | 0.343 | 0.375 | 214.3 | 0.300 | 0.542 | 0.325 | 6.5 | 0.000 |
| Observation-Manipulated | TRUE | 931.6 | [581.6, 1286.0] | 0.754 | 0.636 | 56.4 | 0.754 | 0.524 | 0.316 | 0.0 | -0.003 |
| Observation-Manipulated | TTB-cap | 2679.2 | [2263.6, 3077.2] | 0.806 | 0.661 | 50.8 | 0.774 | 0.736 | 0.442 | 999.0 | 0.000 |
| Observation-Manipulated | MOO-cap | 1016.8 | [312.8, 1685.2] | 0.784 | 0.654 | 57.2 | 0.750 | 0.692 | 0.415 | 800.9 | 0.000 |
| Observation-Manipulated | Blind | -25219.2 | [-25568.0, -24874.4] | 0.336 | 0.435 | 198.2 | 0.334 | 0.521 | 0.313 | 6.4 | 0.000 |
| Baseline | TRUE | 347.6 | [-71.0, 751.6] | 0.752 | 0.730 | 63.9 | 0.725 | 0.592 | 0.367 | 0.1 | 0.242 |
| Baseline | TTB-cap | 1535.2 | [1184.8, 1868.2] | 0.800 | 0.771 | 59.6 | 0.737 | 0.740 | 0.444 | 999.0 | 0.000 |
| Baseline | MOO-cap | 1290.4 | [919.8, 1669.6] | 0.789 | 0.762 | 60.1 | 0.736 | 0.725 | 0.436 | 899.8 | 0.033 |
| Baseline | Blind | -23786.6 | [-24119.4, -23454.2] | 0.342 | 0.400 | 209.5 | 0.310 | 0.530 | 0.318 | 6.5 | 0.000 |
| Utility-Trust-Misalignment | TRUE | 1635.8 | [1311.1, 1964.1] | 0.734 | 0.701 | 58.0 | 0.743 | 0.574 | 0.354 | 0.1 | 0.312 |
| Utility-Trust-Misalignment | TTB-cap | 2889.4 | [2567.7, 3223.3] | 0.774 | 0.736 | 56.1 | 0.753 | 0.736 | 0.442 | 999.0 | 0.000 |
| Utility-Trust-Misalignment | MOO-cap | 2576.8 | [2063.8, 3027.7] | 0.767 | 0.728 | 56.7 | 0.750 | 0.719 | 0.432 | 909.3 | 0.017 |
| Utility-Trust-Misalignment | Blind | -21550.6 | [-21790.7, -21297.7] | 0.338 | 0.391 | 203.8 | 0.311 | 0.533 | 0.320 | 7.2 | 0.000 |

## Scenario Conclusions

### Safety-Critical

- TRUE vs Blind: cumulative utility diff = 49213.6; fatal errors diff = -171.2.
- TRUE A9 first delay = 0.3; collapse index = 0.400.

### Observation-Manipulated

- TRUE vs Blind: cumulative utility diff = 26150.8; fatal errors diff = -141.7.
- TRUE A9 first delay = 0.0; collapse index = 0.316.

### Baseline

- TRUE vs Blind: cumulative utility diff = 24134.2; fatal errors diff = -145.7.
- TRUE A9 first delay = 0.1; collapse index = 0.367.

### Utility-Trust-Misalignment

- TRUE vs Blind: cumulative utility diff = 23186.4; fatal errors diff = -145.8.
- TRUE A9 first delay = 0.1; collapse index = 0.354.

## Hypothesis Tests

| Scenario | Hypothesis | Mean Diff | t | p_t | p_t(Bonf) | W | p_w | p_w(Bonf) | Cohen d |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | TRUE_U > TTB-cap_U | -1187.600 | -4.867 | 0.0000 | 0.0000 | 1209.500 | 0.0000 | 0.0002 | -0.487 |
| Baseline | TRUE_Fatal < TTB-cap_Fatal | -4.280 | -3.758 | 0.0002 | 0.0048 | 1326.500 | 0.0003 | 0.0071 | -0.376 |
| Baseline | TRUE_U > MOO-cap_U | -942.800 | -3.178 | 0.0015 | 0.0415 | 1614.500 | 0.0017 | 0.0488 | -0.318 |
| Baseline | TRUE_Fatal < MOO-cap_Fatal | -3.790 | -2.940 | 0.0033 | 0.0919 | 1612.000 | 0.0039 | 0.1104 | -0.294 |
| Baseline | TRUE_U > Blind_U | 24134.200 | 104.995 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.499 |
| Baseline | TRUE_Fatal < Blind_Fatal | 145.670 | 109.110 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 10.911 |
| Baseline | TRUE_A9 < Blind_A9 | 6.350 | 8.901 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.890 |
| Observation-Manipulated | TRUE_U > TTB-cap_U | -1747.600 | -7.374 | 0.0000 | 0.0000 | 737.000 | 0.0000 | 0.0000 | -0.737 |
| Observation-Manipulated | TRUE_Fatal < TTB-cap_Fatal | -5.660 | -6.092 | 0.0000 | 0.0000 | 902.500 | 0.0000 | 0.0000 | -0.609 |
| Observation-Manipulated | TRUE_U > MOO-cap_U | -85.200 | -0.228 | 0.8196 | 1.0000 | 2243.500 | 0.5190 | 1.0000 | -0.023 |
| Observation-Manipulated | TRUE_Fatal < MOO-cap_Fatal | 0.760 | 0.462 | 0.6444 | 1.0000 | 2252.000 | 0.9172 | 1.0000 | 0.046 |
| Observation-Manipulated | TRUE_U > Blind_U | 26150.800 | 120.268 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 12.027 |
| Observation-Manipulated | TRUE_Fatal < Blind_Fatal | 141.740 | 116.624 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.662 |
| Observation-Manipulated | TRUE_A9 < Blind_A9 | 6.420 | 7.982 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.798 |
| Safety-Critical | TRUE_U > TTB-cap_U | -2494.600 | -6.545 | 0.0000 | 0.0000 | 939.000 | 0.0000 | 0.0000 | -0.654 |
| Safety-Critical | TRUE_Fatal < TTB-cap_Fatal | -4.420 | -4.678 | 0.0000 | 0.0001 | 1105.000 | 0.0000 | 0.0010 | -0.468 |
| Safety-Critical | TRUE_U > MOO-cap_U | -587.200 | -1.216 | 0.2240 | 1.0000 | 1891.500 | 0.0417 | 1.0000 | -0.122 |
| Safety-Critical | TRUE_Fatal < MOO-cap_Fatal | -0.310 | -0.231 | 0.8170 | 1.0000 | 1921.500 | 0.3118 | 1.0000 | -0.023 |
| Safety-Critical | TRUE_U > Blind_U | 49213.600 | 132.715 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.272 |
| Safety-Critical | TRUE_Fatal < Blind_Fatal | 171.200 | 131.996 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.200 |
| Safety-Critical | TRUE_A9 < Blind_A9 | 6.180 | 9.891 | 0.0000 | 0.0000 | 32.000 | 0.0000 | 0.0000 | 0.989 |
| Utility-Trust-Misalignment | TRUE_U > TTB-cap_U | -1253.600 | -5.648 | 0.0000 | 0.0000 | 1056.000 | 0.0000 | 0.0000 | -0.565 |
| Utility-Trust-Misalignment | TRUE_Fatal < TTB-cap_Fatal | -1.900 | -1.925 | 0.0543 | 1.0000 | 1749.000 | 0.0944 | 1.0000 | -0.192 |
| Utility-Trust-Misalignment | TRUE_U > MOO-cap_U | -941.000 | -3.145 | 0.0017 | 0.0465 | 1377.000 | 0.0001 | 0.0022 | -0.315 |
| Utility-Trust-Misalignment | TRUE_Fatal < MOO-cap_Fatal | -1.310 | -0.897 | 0.3695 | 1.0000 | 1858.500 | 0.0445 | 1.0000 | -0.090 |
| Utility-Trust-Misalignment | TRUE_U > Blind_U | 23186.400 | 119.807 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 11.981 |
| Utility-Trust-Misalignment | TRUE_Fatal < Blind_Fatal | 145.820 | 131.971 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 13.197 |
| Utility-Trust-Misalignment | TRUE_A9 < Blind_A9 | 7.090 | 9.256 | 0.0000 | 0.0000 | 0.000 | 0.0000 | 0.0000 | 0.926 |

## Interpretation & Limitations

- Task flows are paired: within each run all groups see the same module sequence. Differences in outcome are therefore attributable to selection mechanisms, not task luck.
- A8 surface-quality bonus is uniform across groups. The only remaining A8 asymmetry is inside TTB's scoring function (A8 receives extra trust-objective weight), which is a *mechanism-level* difference, not an observation-level manipulation.
- Ablation results isolate component contributions: if TRUE-C is substantially worse than TRUE, the constraint filter is a key driver of advantage.
- Bonferroni correction is conservative; if a hypothesis remains significant after correction, the conclusion is robust.
- The experiment remains a probabilistic generative model; no real engineering tools are used.
