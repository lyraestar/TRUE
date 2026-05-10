# TRUE 改进版场景族模拟实验报告

## 总论

本轮实验将单一场景扩展为 4 个参数化场景，仍然不接入真实工具，而是通过概率模型假设来表达不同协作环境。
实验共进行 5 次 Monte Carlo 重复，每次 80 轮，每个场景下比较 TRUE、Blind 和 MOO 三组机制。

本轮改进的重点有三项：

1. 从单层成功信号升级为 `q_true / q_surface / q_obs` 三层观测结构。
2. 从单一任务环境升级为场景族，包括安全高惩罚、观测污染和效用-信任错位场景。
3. 从静态模块成功率升级为包含依赖误差传播与局部阶段性机制的概率模型。

## 场景定义

- `Baseline`: Standard engineering collaboration with moderate observation noise.
- `Safety-Critical`: High-stakes safety environment with harsher penalties and stronger error propagation.
- `Utility-Trust-Misalignment`: Local phases where trusted incumbents underperform and low-history entities hold latent value.
- `Observation-Manipulated`: Observation-contaminated environment where surface quality can diverge from true quality.

## 结果汇总

| 场景 | 组别 | 累积效用均值 | 真实质量均值 | 表面质量均值 | 致命错误均值 | 成功率 | 选择Gini | 塌缩指数 | A9首次延迟 | A8信任-质量相关 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | TRUE | -40.0 | 0.728 | 0.701 | 25.6 | 0.725 | 0.529 | 0.327 | 0.0 | 0.363 |
| Baseline | Blind | -9016.0 | 0.346 | 0.409 | 79.0 | 0.335 | 0.539 | 0.323 | 4.8 | 0.000 |
| Baseline | MOO | -1924.0 | 0.654 | 0.677 | 35.8 | 0.642 | 0.670 | 0.408 | 404.6 | 0.377 |
| Safety-Critical | TRUE | -2936.0 | 0.732 | 0.673 | 18.2 | 0.787 | 0.545 | 0.344 | 0.4 | 0.000 |
| Safety-Critical | Blind | -21768.0 | 0.338 | 0.365 | 88.0 | 0.290 | 0.545 | 0.327 | 5.6 | 0.000 |
| Safety-Critical | MOO | -2248.0 | 0.747 | 0.697 | 18.6 | 0.798 | 0.693 | 0.425 | 600.8 | 0.137 |
| Utility-Trust-Misalignment | TRUE | 1042.0 | 0.729 | 0.684 | 23.4 | 0.753 | 0.511 | 0.309 | 0.2 | 0.381 |
| Utility-Trust-Misalignment | Blind | -8832.0 | 0.343 | 0.413 | 84.4 | 0.300 | 0.538 | 0.323 | 4.4 | 0.000 |
| Utility-Trust-Misalignment | MOO | -292.0 | 0.666 | 0.681 | 30.0 | 0.710 | 0.658 | 0.399 | 600.6 | 0.471 |
| Observation-Manipulated | TRUE | 216.0 | 0.726 | 0.625 | 22.4 | 0.752 | 0.488 | 0.294 | 0.0 | -0.275 |
| Observation-Manipulated | Blind | -9504.0 | 0.350 | 0.421 | 80.0 | 0.360 | 0.536 | 0.322 | 8.0 | 0.000 |
| Observation-Manipulated | MOO | -11440.0 | 0.211 | 0.877 | 93.6 | 0.275 | 0.829 | 0.497 | 999.0 | -0.011 |

## 场景结论

### Baseline

- TRUE 相比 Blind 的累积效用差为 `8976.0`。
- TRUE 相比 MOO 的累积效用差为 `1884.0`。
- TRUE 的致命错误均值为 `25.6`，Blind 为 `79.0`，MOO 为 `35.8`。
- TRUE 的 A9 首次被选平均延迟为 `0.0`，而 MOO 为 `404.6`。
- A8 的信任-真实质量相关在 TRUE 中为 `0.363`，在 MOO 中为 `0.377`。

### Safety-Critical

- TRUE 相比 Blind 的累积效用差为 `18832.0`。
- TRUE 相比 MOO 的累积效用差为 `-688.0`。
- TRUE 的致命错误均值为 `18.2`，Blind 为 `88.0`，MOO 为 `18.6`。
- TRUE 的 A9 首次被选平均延迟为 `0.4`，而 MOO 为 `600.8`。
- A8 的信任-真实质量相关在 TRUE 中为 `0.000`，在 MOO 中为 `0.137`。

### Utility-Trust-Misalignment

- TRUE 相比 Blind 的累积效用差为 `9874.0`。
- TRUE 相比 MOO 的累积效用差为 `1334.0`。
- TRUE 的致命错误均值为 `23.4`，Blind 为 `84.4`，MOO 为 `30.0`。
- TRUE 的 A9 首次被选平均延迟为 `0.2`，而 MOO 为 `600.6`。
- A8 的信任-真实质量相关在 TRUE 中为 `0.381`，在 MOO 中为 `0.471`。

### Observation-Manipulated

- TRUE 相比 Blind 的累积效用差为 `9720.0`。
- TRUE 相比 MOO 的累积效用差为 `11656.0`。
- TRUE 的致命错误均值为 `22.4`，Blind 为 `80.0`，MOO 为 `93.6`。
- TRUE 的 A9 首次被选平均延迟为 `0.0`，而 MOO 为 `999.0`。
- A8 的信任-真实质量相关在 TRUE 中为 `-0.275`，在 MOO 中为 `-0.011`。

## 假设检验摘要

| 场景 | 假设 | 均值差 | t | 近似p值 | Cohen d |
|---|---|---:|---:|---:|---:|
| Baseline | TRUE_U > Blind_U | 8976.000 | 21.779 | 0.0000 | 9.740 |
| Baseline | TRUE_U > MOO_U | 1884.000 | 1.197 | 0.2315 | 0.535 |
| Baseline | TRUE_Fatal < Blind_Fatal | 53.400 | 14.776 | 0.0000 | 6.608 |
| Baseline | TRUE_Fatal < MOO_Fatal | 10.200 | 1.371 | 0.1703 | 0.613 |
| Baseline | TRUE_A9 < Blind_A9 | 4.800 | 2.626 | 0.0086 | 1.175 |
| Baseline | TRUE_Collapse < MOO_Collapse | 0.081 | 6.648 | 0.0000 | 2.973 |
| Observation-Manipulated | TRUE_U > Blind_U | 9720.000 | 22.514 | 0.0000 | 10.068 |
| Observation-Manipulated | TRUE_U > MOO_U | 11656.000 | 20.394 | 0.0000 | 9.121 |
| Observation-Manipulated | TRUE_Fatal < Blind_Fatal | 57.600 | 22.489 | 0.0000 | 10.057 |
| Observation-Manipulated | TRUE_Fatal < MOO_Fatal | 71.200 | 20.519 | 0.0000 | 9.177 |
| Observation-Manipulated | TRUE_A9 < Blind_A9 | 8.000 | 2.138 | 0.0325 | 0.956 |
| Observation-Manipulated | TRUE_Collapse < MOO_Collapse | 0.203 | 31.511 | 0.0000 | 14.092 |
| Safety-Critical | TRUE_U > Blind_U | 18832.000 | 30.524 | 0.0000 | 13.651 |
| Safety-Critical | TRUE_U > MOO_U | -688.000 | -0.746 | 0.4558 | -0.334 |
| Safety-Critical | TRUE_Fatal < Blind_Fatal | 69.800 | 29.927 | 0.0000 | 13.384 |
| Safety-Critical | TRUE_Fatal < MOO_Fatal | 0.400 | 0.161 | 0.8720 | 0.072 |
| Safety-Critical | TRUE_A9 < Blind_A9 | 5.200 | 6.500 | 0.0000 | 2.907 |
| Safety-Critical | TRUE_Collapse < MOO_Collapse | 0.082 | 6.149 | 0.0000 | 2.750 |
| Utility-Trust-Misalignment | TRUE_U > Blind_U | 9874.000 | 30.446 | 0.0000 | 13.616 |
| Utility-Trust-Misalignment | TRUE_U > MOO_U | 1334.000 | 1.812 | 0.0700 | 0.810 |
| Utility-Trust-Misalignment | TRUE_Fatal < Blind_Fatal | 61.000 | 23.566 | 0.0000 | 10.539 |
| Utility-Trust-Misalignment | TRUE_Fatal < MOO_Fatal | 6.600 | 1.371 | 0.1702 | 0.613 |
| Utility-Trust-Misalignment | TRUE_A9 < Blind_A9 | 4.200 | 2.370 | 0.0178 | 1.060 |
| Utility-Trust-Misalignment | TRUE_Collapse < MOO_Collapse | 0.090 | 14.702 | 0.0000 | 6.575 |

## 解释与边界

- `Baseline` 用于保证与上一轮单场景实验可连续比较。
- `Safety-Critical` 强化了安全非对称性，用于检验 TRUE 的约束优势是否在高风险环境下放大。
- `Observation-Manipulated` 将真实质量与表面质量分离，用于更严格地模拟 Goodhart 型操纵。
- `Utility-Trust-Misalignment` 刻画了局部阶段中“高信任不等于高短期效用”的环境，用于测试 TRUE 是否能更好地保留长期信息价值。
- 本轮实验依然不等于真实工程流程复现，而是更严格的概率生成模型比较。
