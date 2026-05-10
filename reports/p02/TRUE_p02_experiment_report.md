# TRUE P02 Experiment Report: Tuned Parameters + Cap Noise Robustness

## Executive Summary

This round addresses the fairness critique from P01: all trust-based systems now have access to the same capability prior (`cap`), all are hyperparameter-tuned, and all are tested under imperfect priors (`cap_noise > 0`).

**Key finding: even with fair access to `cap` and optimal tuning, TTB-cap consistently outperforms TRUE across all scenarios and noise levels.** The previously observed TRUE advantage was largely due to (1) an unfair lack of `cap` for TTB/MOO, and (2) suboptimal default parameters for TTB/MOO.

## Phase 1: Hyperparameter Tuning (Baseline, 100 runs)

### TRUE
| Parameter | Search Range | Optimal |
|---|---|---|
| `cap_weight` | 0.3, 0.5, 0.7, 0.9, 1.1 | **0.5** |
| `theta_weight` | 0.1, 0.3, 0.5 | **0.1** |
| `exploration_coef` | 0.0, 0.15, 0.3, 0.5 | **0.0** |

**Optimal Baseline utility: 1,381.2**

Surprising: TRUE's optimal configuration sets `exploration_coef = 0.0` — the exploration bonus provides no value under current parameters.

### TTB-cap
| Parameter | Search Range | Optimal |
|---|---|---|
| `trust_weight` | 0.3, 0.5, 0.7, 0.9, 1.1 | **0.5** |
| `util_weight` | derived (1.0 - trust) | **0.5** |
| `var_penalty` | -0.1, -0.04, 0.0 | **-0.1** |

**Optimal Baseline utility: 1,539.6**

### MOO-cap
| Weight Vector | Optimal |
|---|---|
| [utility, trust, variance, diversity, cap] | **[0.2, 0.35, 0.03, 0.18, 0.24]** |

**Optimal Baseline utility: 588.4**

## Phase 2: Full Scenario Comparison with Tuned Parameters

### cap_noise = 0.00 (perfect prior)

| Scenario | TRUE | TTB-cap | MOO-cap |
|---|---|---|---|
| Baseline | 1,186.4 | **1,745.2** | 943.4 |
| Observation-Manipulated | 2,472.4 | **3,069.2** | 945.2 |
| Safety-Critical | -2,829.2 | **-2,041.0** | -3,140.4 |
| Utility-Trust-Misalignment | 2,410.6 | **2,944.5** | 2,217.8 |

### cap_noise = 0.10 (moderate prior uncertainty)

| Scenario | TRUE | TTB-cap | MOO-cap |
|---|---|---|---|
| Baseline | 700.0 | **1,685.0** | 870.6 |
| Observation-Manipulated | 1,651.2 | **2,715.2** | 1,812.8 |
| Safety-Critical | -3,195.2 | **-1,913.4** | -3,067.2 |
| Utility-Trust-Misalignment | 2,023.6 | **3,129.3** | 2,022.9 |

### cap_noise = 0.20 (high prior uncertainty)

| Scenario | TRUE | TTB-cap | MOO-cap |
|---|---|---|---|
| Baseline | 86.2 | **1,387.0** | 258.0 |
| Observation-Manipulated | 801.2 | **2,614.8** | 883.6 |
| Safety-Critical | -3,721.8 | **-2,394.4** | -3,291.0 |
| Utility-Trust-Misalignment | 1,859.5 | **3,179.7** | 2,622.1 |

## Robustness Analysis

**TTB-cap degradation from noise=0.00 to noise=0.20:**
- Baseline: 1,745.2 → 1,387.0 (-20.5%)
- Observation-Manipulated: 3,069.2 → 2,614.8 (-14.8%)

**TRUE degradation from noise=0.00 to noise=0.20:**
- Baseline: 1,186.4 → 86.2 (-92.7%)
- Observation-Manipulated: 2,472.4 → 801.2 (-67.6%)

**Conclusion**: TTB-cap is not only higher-performing but also **substantially more robust to prior noise** than TRUE.

## Interpretation

1. **The TRUE > TTB conclusion from earlier rounds was an artifact of asymmetric information** (TRUE had `cap`, TTB/MOO did not).
2. **When all systems have fair access to `cap` and are tuned, TTB-cap wins.**
3. **TRUE's exploration bonus (`0.30 * tv`) has no value** — its optimal setting is 0.0.
4. **TTB-cap's balanced trust-utility weighting (0.5 / 0.5) with variance penalty (-0.1) is the most effective configuration** among those tested.
5. **MOO-cap underperforms** despite having the most flexible objective structure, suggesting that Tchebycheff normalization + diversity objective adds complexity without benefit in this discrete selection setting.

## Limitations

- Tuning was done only on Baseline scenario; optimal parameters might differ for other scenarios.
- The `cap_noise` model is simple Gaussian perturbation; real-world prior uncertainty may have different structure.
- Only 100 runs per configuration; confidence intervals are wide for some metrics.
- MOO tuning was limited to 4 weight combinations due to computational constraints.

## Files

- Tuning results: `data/p02_results/p02_tune_*.json`
- Noise sweep: `data/p02_results/p02_noise_sweep.json`
- Raw data: `data/p02_results/noise_0.00/`, `noise_0.10/`, `noise_0.20/`
