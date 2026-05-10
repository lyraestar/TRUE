# TRUE 改进版专业实验报告

## 执行摘要

本报告基于参数化场景族，对 TRUE、Blind 与 MOO 三种多人多 Agent 协作机制进行了新一轮模拟对比。实验不引入真实外部工具，而是通过概率模型对任务成功、表面观测、延迟反馈和局部错位现象进行统一建模。

本轮实验表明，TRUE 在四类场景下都显著优于 Blind，并且相对 MOO 也保持稳定优势。其中，Observation-Manipulated 场景最清楚地展示了将信任作为目标函数时可能带来的误导性分配问题，而 Utility-Trust-Misalignment 场景则更直接说明了 TRUE 在保留长期信息价值方面的机制优势。

## 场景结果摘要

Baseline：TRUE 累积效用为 949.0， 相比 Blind 高 24507.3， 相比 MOO 高 3259.3； TRUE 的致命错误均值为 60.4， MOO 为 76.3。

Safety-Critical：TRUE 累积效用为 -3530.0， 相比 Blind 高 50019.0， 相比 MOO 高 1930.3； TRUE 的致命错误均值为 41.8， MOO 为 47.0。

Observation-Manipulated：TRUE 累积效用为 1909.3， 相比 Blind 高 26885.3， 相比 MOO 高 30821.3； TRUE 的致命错误均值为 52.4， MOO 为 224.7。

Utility-Trust-Misalignment：TRUE 累积效用为 2885.8， 相比 Blind 高 24440.2， 相比 MOO 高 4119.2； TRUE 的致命错误均值为 53.8， MOO 为 74.9。

## 结果表与检验

| scenario                   | group   |   cumulative_utility_mean |   cumulative_utility_sd |   mean_quality_true |   mean_quality_surface |   fatal_errors_mean |   success_rate |   final_trust_gini |   final_collapse_index |   mean_trust_var |   a9_first_delay |   a10_first_delay |   a9_first20_rate |   a9_var_convergence |   a8_trust_quality_corr |
|:---------------------------|:--------|--------------------------:|------------------------:|--------------------:|-----------------------:|--------------------:|---------------:|-------------------:|-----------------------:|-----------------:|-----------------:|------------------:|------------------:|---------------------:|------------------------:|
| baseline                   | Blind   |                 -23558.3  |                 1541.19 |            0.341269 |               0.403597 |            209.05   |       0.314583 |           0.528099 |               0.316859 |        0.0833333 |         5.8      |         6.83333   |         0.148333  |            999       |              0          |
| baseline                   | MOO     |                  -2310.33 |                 5591.05 |            0.734517 |               0.723589 |             76.2833 |       0.679083 |           0.727396 |               0.439521 |        0.0700834 |       686.217    |       851.633     |         0.0883333 |            999       |              0.243206   |
| baseline                   | TRUE    |                    949    |                 2094.8  |            0.765339 |               0.73984  |             60.4167 |       0.734417 |           0.637387 |               0.393182 |        0.0673825 |         0.216667 |         1.26667   |         0.384167  |            102.417   |              0.262756   |
| safety_critical            | Blind   |                 -53549    |                 2973.4  |            0.345096 |               0.380144 |            214      |       0.29875  |           0.533351 |               0.32001  |        0.0833333 |         6.46667  |         6.98333   |         0.134167  |            999       |              0          |
| safety_critical            | MOO     |                  -5460.33 |                 4106.85 |            0.780442 |               0.719651 |             47      |       0.795167 |           0.737594 |               0.449473 |        0.0705787 |       701.133    |       883.7       |         0.0516667 |            999       |              0.215591   |
| safety_critical            | TRUE    |                  -3530    |                 2806.79 |            0.794268 |               0.721815 |             41.8167 |       0.813    |           0.654695 |               0.415233 |        0.0679273 |         0.466667 |         2.86667   |         0.296667  |            135.733   |              0.106785   |
| observation_manipulated    | Blind   |                 -24976    |                 1852.9  |            0.338012 |               0.435299 |            197.267  |       0.338083 |           0.516294 |               0.309776 |        0.0833333 |         5.26667  |         7.51667   |         0.163333  |            999       |              0          |
| observation_manipulated    | MOO     |                 -28912    |                 1628.22 |            0.217646 |               0.876099 |            224.7    |       0.269417 |           0.858191 |               0.514914 |        0.076158  |       999        |       999         |         0         |            999       |              0.00316869 |
| observation_manipulated    | TRUE    |                   1909.33 |                 1889.33 |            0.767932 |               0.641828 |             52.3833 |       0.76725  |           0.604892 |               0.364519 |        0.0668228 |         0        |         0.0666667 |         0.388333  |              6.73333 |             -0.0234031  |
| utility_trust_misalignment | Blind   |                 -21554.3  |                 1507.15 |            0.336142 |               0.389811 |            204.1    |       0.310667 |           0.530465 |               0.318279 |        0.0833333 |         6.78333  |         7.75      |         0.144167  |            999       |              0          |
| utility_trust_misalignment | MOO     |                  -1233.33 |                 6594.09 |            0.71319  |               0.700814 |             74.8833 |       0.685167 |           0.727892 |               0.438985 |        0.0704819 |       654.033    |       719.2       |         0.0666667 |            999       |              0.305185   |
| utility_trust_misalignment | TRUE    |                   2885.83 |                 1511.99 |            0.751032 |               0.707721 |             53.7833 |       0.761583 |           0.608229 |               0.374771 |        0.0671889 |         0.383333 |         0.05      |         0.480833  |             34.95    |              0.2862     |

| scenario                   | hypothesis                   | metric                  |     mean_diff |         t |    p_approx |   cohens_d |
|:---------------------------|:-----------------------------|:------------------------|--------------:|----------:|------------:|-----------:|
| baseline                   | TRUE_A9 < Blind_A9           | A9 first selected delay |     5.58333   |   8.77678 | 0           |   1.13308  |
| baseline                   | TRUE_Collapse < MOO_Collapse | collapse index          |     0.0463385 |  14.4844  | 0           |   1.86993  |
| baseline                   | TRUE_Fatal < Blind_Fatal     | fatal errors            |   148.633     |  82.0876  | 0           |  10.5975   |
| baseline                   | TRUE_Fatal < MOO_Fatal       | fatal errors            |    15.8667    |   4.56034 | 5.10713e-06 |   0.588737 |
| baseline                   | TRUE_U > Blind_U             | cumulative utility      | 24507.3       |  69.7623  | 0           |   9.00627  |
| baseline                   | TRUE_U > MOO_U               | cumulative utility      |  3259.33      |   4.30953 | 1.63602e-05 |   0.556358 |
| safety_critical            | TRUE_A9 < Blind_A9           | A9 first selected delay |     6         |   6.90613 | 4.98046e-12 |   0.891577 |
| safety_critical            | TRUE_Collapse < MOO_Collapse | collapse index          |     0.0342398 |  10.8406  | 0           |   1.39951  |
| safety_critical            | TRUE_Fatal < Blind_Fatal     | fatal errors            |   172.183     | 100.781   | 0           |  13.0108   |
| safety_critical            | TRUE_Fatal < MOO_Fatal       | fatal errors            |     5.18333   |   3.36831 | 0.000756318 |   0.434846 |
| safety_critical            | TRUE_U > Blind_U             | cumulative utility      | 50019         |  87.4095  | 0           |  11.2845   |
| safety_critical            | TRUE_U > MOO_U               | cumulative utility      |  1930.33      |   2.97022 | 0.0029759   |   0.383453 |
| observation_manipulated    | TRUE_A9 < Blind_A9           | A9 first selected delay |     5.26667   |   7.14439 | 9.03944e-13 |   0.922337 |
| observation_manipulated    | TRUE_Collapse < MOO_Collapse | collapse index          |     0.150396  | 106.758   | 0           |  13.7825   |
| observation_manipulated    | TRUE_Fatal < Blind_Fatal     | fatal errors            |   144.883     |  74.6176  | 0           |   9.6331   |
| observation_manipulated    | TRUE_Fatal < MOO_Fatal       | fatal errors            |   172.317     |  65.2548  | 0           |   8.42436  |
| observation_manipulated    | TRUE_U > Blind_U             | cumulative utility      | 26885.3       |  74.2781  | 0           |   9.58926  |
| observation_manipulated    | TRUE_U > MOO_U               | cumulative utility      | 30821.3       |  97.1816  | 0           |  12.5461   |
| utility_trust_misalignment | TRUE_A9 < Blind_A9           | A9 first selected delay |     6.4       |   6.92637 | 4.31788e-12 |   0.89419  |
| utility_trust_misalignment | TRUE_Collapse < MOO_Collapse | collapse index          |     0.0642141 |  19.1265  | 0           |   2.46922  |
| utility_trust_misalignment | TRUE_Fatal < Blind_Fatal     | fatal errors            |   150.317     |  82.4753  | 0           |  10.6475   |
| utility_trust_misalignment | TRUE_Fatal < MOO_Fatal       | fatal errors            |    21.1       |   4.56184 | 5.07065e-06 |   0.588931 |
| utility_trust_misalignment | TRUE_U > Blind_U             | cumulative utility      | 24440.2       |  87.282   | 0           |  11.2681   |
| utility_trust_misalignment | TRUE_U > MOO_U               | cumulative utility      |  4119.17      |   4.90156 | 9.5079e-07  |   0.632789 |
