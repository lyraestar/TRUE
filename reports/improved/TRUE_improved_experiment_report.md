# TRUE 改进版场景族模拟实验报告

## 总论

本轮实验将单一场景扩展为 4 个参数化场景，仍然不接入真实工具，而是通过概率模型假设来表达不同协作环境。
实验共进行 60 次 Monte Carlo 重复，每次 200 轮，每个场景下比较 TRUE、Blind 和 MOO 三组机制。

本轮改进的重点有三项：

1. 从单层成功信号升级为 `q_true / q_surface / q_obs` 三层观测结构。
2. 从单一任务环境升级为场景族，包括安全高惩罚、观测污染和效用-信任错位场景。
3. 从静态模块成功率升级为包含依赖误差传播与局部阶段性机制的概率模型。

## 场景定义

- `Utility-Trust-Misalignment`: Local phases where trusted incumbents underperform and low-history entities hold latent value.
- `Safety-Critical`: High-stakes safety environment with harsher penalties and stronger error propagation.
- `Baseline`: Standard engineering collaboration with moderate observation noise.
- `Observation-Manipulated`: Observation-contaminated environment where surface quality can diverge from true quality.

## 结果汇总

| 场景 | 组别 | 累积效用均值 | 真实质量均值 | 表面质量均值 | 致命错误均值 | 成功率 | 选择Gini | 塌缩指数 | A9首次延迟 | A8信任-质量相关 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Utility-Trust-Misalignment | TRUE | 2885.8 | 0.751 | 0.708 | 53.8 | 0.762 | 0.608 | 0.375 | 0.4 | 0.286 |
| Utility-Trust-Misalignment | Blind | -21554.3 | 0.336 | 0.390 | 204.1 | 0.311 | 0.530 | 0.318 | 6.8 | 0.000 |
| Utility-Trust-Misalignment | MOO | -1233.3 | 0.713 | 0.701 | 74.9 | 0.685 | 0.728 | 0.439 | 654.0 | 0.305 |
| Safety-Critical | TRUE | -3530.0 | 0.794 | 0.722 | 41.8 | 0.813 | 0.655 | 0.415 | 0.5 | 0.107 |
| Safety-Critical | Blind | -53549.0 | 0.345 | 0.380 | 214.0 | 0.299 | 0.533 | 0.320 | 6.5 | 0.000 |
| Safety-Critical | MOO | -5460.3 | 0.780 | 0.720 | 47.0 | 0.795 | 0.738 | 0.449 | 701.1 | 0.216 |
| Baseline | TRUE | 949.0 | 0.765 | 0.740 | 60.4 | 0.734 | 0.637 | 0.393 | 0.2 | 0.263 |
| Baseline | Blind | -23558.3 | 0.341 | 0.404 | 209.1 | 0.315 | 0.528 | 0.317 | 5.8 | 0.000 |
| Baseline | MOO | -2310.3 | 0.735 | 0.724 | 76.3 | 0.679 | 0.727 | 0.440 | 686.2 | 0.243 |
| Observation-Manipulated | TRUE | 1909.3 | 0.768 | 0.642 | 52.4 | 0.767 | 0.605 | 0.365 | 0.0 | -0.023 |
| Observation-Manipulated | Blind | -24976.0 | 0.338 | 0.435 | 197.3 | 0.338 | 0.516 | 0.310 | 5.3 | 0.000 |
| Observation-Manipulated | MOO | -28912.0 | 0.218 | 0.876 | 224.7 | 0.269 | 0.858 | 0.515 | 999.0 | 0.003 |

## 场景结论

### Utility-Trust-Misalignment

- TRUE 相比 Blind 的累积效用差为 `24440.2`。
- TRUE 相比 MOO 的累积效用差为 `4119.2`。
- TRUE 的致命错误均值为 `53.8`，Blind 为 `204.1`，MOO 为 `74.9`。
- TRUE 的 A9 首次被选平均延迟为 `0.4`，而 MOO 为 `654.0`。
- A8 的信任-真实质量相关在 TRUE 中为 `0.286`，在 MOO 中为 `0.305`。

### Safety-Critical

- TRUE 相比 Blind 的累积效用差为 `50019.0`。
- TRUE 相比 MOO 的累积效用差为 `1930.3`。
- TRUE 的致命错误均值为 `41.8`，Blind 为 `214.0`，MOO 为 `47.0`。
- TRUE 的 A9 首次被选平均延迟为 `0.5`，而 MOO 为 `701.1`。
- A8 的信任-真实质量相关在 TRUE 中为 `0.107`，在 MOO 中为 `0.216`。

### Baseline

- TRUE 相比 Blind 的累积效用差为 `24507.3`。
- TRUE 相比 MOO 的累积效用差为 `3259.3`。
- TRUE 的致命错误均值为 `60.4`，Blind 为 `209.1`，MOO 为 `76.3`。
- TRUE 的 A9 首次被选平均延迟为 `0.2`，而 MOO 为 `686.2`。
- A8 的信任-真实质量相关在 TRUE 中为 `0.263`，在 MOO 中为 `0.243`。

### Observation-Manipulated

- TRUE 相比 Blind 的累积效用差为 `26885.3`。
- TRUE 相比 MOO 的累积效用差为 `30821.3`。
- TRUE 的致命错误均值为 `52.4`，Blind 为 `197.3`，MOO 为 `224.7`。
- TRUE 的 A9 首次被选平均延迟为 `0.0`，而 MOO 为 `999.0`。
- A8 的信任-真实质量相关在 TRUE 中为 `-0.023`，在 MOO 中为 `0.003`。

## 假设检验摘要

| 场景 | 假设 | 均值差 | t | 近似p值 | Cohen d |
|---|---|---:|---:|---:|---:|
| Baseline | TRUE_U > Blind_U | 24507.333 | 69.762 | 0.0000 | 9.006 |
| Baseline | TRUE_U > MOO_U | 3259.333 | 4.310 | 0.0000 | 0.556 |
| Baseline | TRUE_Fatal < Blind_Fatal | 148.633 | 82.088 | 0.0000 | 10.597 |
| Baseline | TRUE_Fatal < MOO_Fatal | 15.867 | 4.560 | 0.0000 | 0.589 |
| Baseline | TRUE_A9 < Blind_A9 | 5.583 | 8.777 | 0.0000 | 1.133 |
| Baseline | TRUE_Collapse < MOO_Collapse | 0.046 | 14.484 | 0.0000 | 1.870 |
| Observation-Manipulated | TRUE_U > Blind_U | 26885.333 | 74.278 | 0.0000 | 9.589 |
| Observation-Manipulated | TRUE_U > MOO_U | 30821.333 | 97.182 | 0.0000 | 12.546 |
| Observation-Manipulated | TRUE_Fatal < Blind_Fatal | 144.883 | 74.618 | 0.0000 | 9.633 |
| Observation-Manipulated | TRUE_Fatal < MOO_Fatal | 172.317 | 65.255 | 0.0000 | 8.424 |
| Observation-Manipulated | TRUE_A9 < Blind_A9 | 5.267 | 7.144 | 0.0000 | 0.922 |
| Observation-Manipulated | TRUE_Collapse < MOO_Collapse | 0.150 | 106.758 | 0.0000 | 13.782 |
| Safety-Critical | TRUE_U > Blind_U | 50019.000 | 87.410 | 0.0000 | 11.285 |
| Safety-Critical | TRUE_U > MOO_U | 1930.333 | 2.970 | 0.0030 | 0.383 |
| Safety-Critical | TRUE_Fatal < Blind_Fatal | 172.183 | 100.781 | 0.0000 | 13.011 |
| Safety-Critical | TRUE_Fatal < MOO_Fatal | 5.183 | 3.368 | 0.0008 | 0.435 |
| Safety-Critical | TRUE_A9 < Blind_A9 | 6.000 | 6.906 | 0.0000 | 0.892 |
| Safety-Critical | TRUE_Collapse < MOO_Collapse | 0.034 | 10.841 | 0.0000 | 1.400 |
| Utility-Trust-Misalignment | TRUE_U > Blind_U | 24440.167 | 87.282 | 0.0000 | 11.268 |
| Utility-Trust-Misalignment | TRUE_U > MOO_U | 4119.167 | 4.902 | 0.0000 | 0.633 |
| Utility-Trust-Misalignment | TRUE_Fatal < Blind_Fatal | 150.317 | 82.475 | 0.0000 | 10.648 |
| Utility-Trust-Misalignment | TRUE_Fatal < MOO_Fatal | 21.100 | 4.562 | 0.0000 | 0.589 |
| Utility-Trust-Misalignment | TRUE_A9 < Blind_A9 | 6.400 | 6.926 | 0.0000 | 0.894 |
| Utility-Trust-Misalignment | TRUE_Collapse < MOO_Collapse | 0.064 | 19.126 | 0.0000 | 2.469 |

## 解释与边界

- `Baseline` 用于保证与上一轮单场景实验可连续比较。
- `Safety-Critical` 强化了安全非对称性，用于检验 TRUE 的约束优势是否在高风险环境下放大。
- `Observation-Manipulated` 将真实质量与表面质量分离，用于更严格地模拟 Goodhart 型操纵。
- `Utility-Trust-Misalignment` 刻画了局部阶段中“高信任不等于高短期效用”的环境，用于测试 TRUE 是否能更好地保留长期信息价值。
- 本轮实验依然不等于真实工程流程复现，而是更严格的概率生成模型比较。
