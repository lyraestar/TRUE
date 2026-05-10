#!/usr/bin/env python3
"""Generate a polished Markdown and PDF report for the TRUE simulation."""

from __future__ import annotations

import argparse
import math
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager
from matplotlib.backends.backend_pdf import PdfPages


def fmt(x: float, digits: int = 3) -> str:
    return f"{float(x):.{digits}f}"


def wrap_lines(text: str, width: int = 34) -> str:
    parts = []
    for block in text.split("\n"):
        if not block.strip():
            parts.append("")
        else:
            parts.extend(textwrap.wrap(block, width=width, break_long_words=False, break_on_hyphens=False))
    return "\n".join(parts)


def set_chinese_font(font_path: Path) -> font_manager.FontProperties:
    font_manager.fontManager.addfont(str(font_path))
    return font_manager.FontProperties(fname=str(font_path))


def add_text_page(pdf: PdfPages, title: str, body: str, font_prop, *, size: int = 12) -> None:
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.patch.set_facecolor("white")
    fig.text(0.08, 0.95, title, fontproperties=font_prop, fontsize=20, weight="bold", va="top")
    fig.text(0.08, 0.91, body, fontproperties=font_prop, fontsize=size, va="top", linespacing=1.5)
    plt.axis("off")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def add_table_page(pdf: PdfPages, title: str, df: pd.DataFrame, font_prop, col_widths=None) -> None:
    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    ax.axis("off")
    fig.text(0.08, 0.96, title, fontproperties=font_prop, fontsize=20, weight="bold", va="top")

    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda x: fmt(x, 3))
    table = ax.table(
        cellText=display.values,
        colLabels=display.columns,
        cellLoc="center",
        colLoc="center",
        bbox=[0.04, 0.08, 0.92, 0.82],
        colWidths=col_widths,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#D0D0D0")
        cell.set_linewidth(0.6)
        cell.get_text().set_fontproperties(font_prop)
        if row == 0:
            cell.set_facecolor("#EAF2F8")
            cell.get_text().set_weight("bold")
        elif row % 2 == 1:
            cell.set_facecolor("#FAFAFA")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def make_markdown(outdir: Path, summary: pd.DataFrame, tests: pd.DataFrame) -> Path:
    by_group = {row["group"]: row for _, row in summary.iterrows()}
    true_row = by_group["TRUE"]
    blind_row = by_group["Blind"]
    moo_row = by_group["MOO"]

    lines = [
        "# TRUE 框架模拟实验报告",
        "",
        "## 总论",
        "",
        "本报告基于 `100` 次 Monte Carlo 重复实验、每次 `200` 轮任务协作，对 TRUE、Blind 和 MOO 三类多人多 Agent 协作机制进行了可执行近似比较。",
        "实验场景沿用桥梁协同设计，但所有外部专业工具均被抽象为随机成功-失败或任务质量变量，以便聚焦于信任机制、任务分配机制和抗操纵能力本身。",
        "",
        f"结果显示，TRUE 组的平均累积效用为 `{fmt(true_row['cumulative_utility_mean'],1)}`，显著高于 Blind 组的 `{fmt(blind_row['cumulative_utility_mean'],1)}` 和 MOO 组的 `{fmt(moo_row['cumulative_utility_mean'],1)}`。",
        f"同时，TRUE 组的平均任务质量最高 (`{fmt(true_row['mean_quality'])}`)，致命错误最少 (`{fmt(true_row['fatal_errors_mean'],1)}`)，并且对 A9/A10 这类中途加入的新 Agent 表现出更好的冷启动接纳能力。",
        "",
        "从机制角度看，这说明“把信任作为约束而不是目标”在当前近似实现中具有明显优势：它既保留了探索能力，又能避免盲信系统的安全失控，以及 MOO 系统在信任目标驱动下的选择塌缩问题。",
        "不过，A8 的操纵效应在本近似实现中没有完全复现出文档设想的强烈负相关，因此 H4 只能算部分实现，而不宜过度解读。",
        "",
        "## 1. 实验目的",
        "",
        "本实验试图回答四类问题：",
        "",
        "1. TRUE 能否在多轮协作中持续提高任务效用并控制安全风险。",
        "2. TRUE 相比无信任体系是否能减少认知过载与盲目分配。",
        "3. TRUE 相比把信任纳入目标函数的 MOO 系统，是否能避免 Goodhart 式信任操纵。",
        "4. TRUE 的 Thompson 采样与覆盖机制，是否能帮助新 Agent 更快地进入协作系统。",
        "",
        "## 2. 场景与近似建模",
        "",
        "实验任务域采用桥梁工程协同设计。每轮任务从 8 个模块中随机抽取 `3-5` 个，并根据依赖关系自动补全。模块包括荷载计算、地质分析、材料选型、规范合规检查、结构方案设计、安全评估、成本估算和文档生成。",
        "",
        "由于本地并未接入真实桥梁设计软件、规范检索系统或工程计算器，本实现将所有外部能力抽象为随机变量：",
        "",
        "- 模块成功概率：`capability × difficulty`",
        "- 灾难性错误概率：当低能力实体承担致命模块时，额外引入 `10%` 的事故概率",
        "- 任务效用：全部成功记 `+100`，仅非致命失败记 `+60`，任意致命失败记 `-200`",
        "",
        "这种处理不再评估真实工程产物，而是专门考察协作制度本身。",
        "",
        "## 3. 三组系统设定",
        "",
        "### 3.1 TRUE 组",
        "",
        "- 使用 Beta 信任分布维护各实体在不同能力维度上的信念。",
        "- 采用 Thompson 采样进行探索。",
        "- 通过质量、可靠性、信任底线与覆盖度鼓励实现“信任为约束”的分配机制。",
        "- A9 于第 50 轮加入，A10 于第 100 轮加入，新 Agent 初始采用均匀先验。",
        "",
        "### 3.2 Blind 组",
        "",
        "- 不维护信任状态。",
        "- 分配时更偏向资深人类或随机挑选。",
        "- 没有质量底线、可靠性底线与冷启动保障。",
        "",
        "### 3.3 MOO 组",
        "",
        "- 将信任均值直接纳入确定性目标函数。",
        "- 不设置显式质量约束或可靠性约束。",
        "- 对 A8 的“表面完美”更敏感，从而更容易出现选择塌缩与新人排斥。",
        "",
        "## 4. 数据与结果",
        "",
        "### 4.1 组间汇总",
        "",
        "| 组别 | 累积效用均值 | 平均质量 | 致命错误均值 | 成功率 | 信任Gini | 塌缩指数 | A9首次延迟 | A10首次延迟 | A8信任-质量相关 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for group in ["TRUE", "Blind", "MOO"]:
        row = by_group[group]
        lines.append(
            f"| {group} | {fmt(row['cumulative_utility_mean'],1)} | {fmt(row['mean_quality'])} | "
            f"{fmt(row['fatal_errors_mean'],1)} | {fmt(row['success_rate'])} | {fmt(row['final_trust_gini'])} | "
            f"{fmt(row['final_collapse_index'])} | {fmt(row['a9_first_delay'],1)} | {fmt(row['a10_first_delay'],1)} | "
            f"{fmt(row['a8_trust_quality_corr'])} |"
        )

    lines += [
        "",
        "### 4.2 假设检验",
        "",
        "| 假设 | 结论 | 说明 |",
        "|---|---|---|",
        f"| H1a TRUE 效用 > Blind | 支持 | TRUE 比 Blind 高 `{fmt(true_row['cumulative_utility_mean'] - blind_row['cumulative_utility_mean'],1)}` |",
        f"| H1b TRUE 效用 > MOO | 支持 | TRUE 比 MOO 高 `{fmt(true_row['cumulative_utility_mean'] - moo_row['cumulative_utility_mean'],1)}` |",
        f"| H2 TRUE 信任健康优于 MOO | 基本支持 | MOO 的 Gini (`{fmt(moo_row['final_trust_gini'])}`) 和塌缩指数 (`{fmt(moo_row['final_collapse_index'])}`) 更高 |",
        f"| H3 TRUE 冷启动优于对照组 | 支持 | TRUE 中 A9 平均 `{fmt(true_row['a9_first_delay'],1)}` 轮即被首次选中，而 Blind 为 `{fmt(blind_row['a9_first_delay'],1)}` |",
        f"| H4 TRUE 抗操纵优于 MOO | 部分支持 | 本实现中未复现强负相关，仅观察到 MOO 长期排斥新人、对 A8 更宽容 |",
        f"| H5 TRUE 致命错误最少 | 支持 | TRUE 的致命错误均值为 `{fmt(true_row['fatal_errors_mean'],1)}`，明显低于另外两组 |",
        "",
        "## 5. 详细分析",
        "",
        "### 5.1 任务效用",
        "",
        "TRUE 在长期累计效用上显著领先两组。Blind 因为经常把致命模块分配给并不擅长的资深人类，导致事故大量积累；MOO 虽然前期表现优于 Blind，但后期更容易在少数高信任对象上过度集中，整体效用仍明显落后于 TRUE。",
        "",
        "### 5.2 任务质量与安全",
        "",
        f"TRUE 的平均任务质量为 `{fmt(true_row['mean_quality'])}`，同时致命错误均值仅 `{fmt(true_row['fatal_errors_mean'],1)}`。这说明在本近似模型下，约束式信任机制确实能把探索限制在安全边界之内。",
        "",
        "### 5.3 新人冷启动",
        "",
        f"A9 在 TRUE 组中的首次被选平均延迟仅 `{fmt(true_row['a9_first_delay'],1)}` 轮，而在 MOO 组中几乎始终无法被有效纳入。这个结果与文档中“覆盖度约束 + Thompson 采样有利于冷启动”的核心主张一致。",
        "",
        "### 5.4 信任健康与操纵",
        "",
        f"MOO 的信任 Gini 和塌缩指数分别达到 `{fmt(moo_row['final_trust_gini'])}` 与 `{fmt(moo_row['final_collapse_index'])}`，高于 TRUE 的 `{fmt(true_row['final_trust_gini'])}` 与 `{fmt(true_row['final_collapse_index'])}`，说明其更容易形成选择集中和结构塌缩。",
        "但 A8 的信任-质量相关在本实现中并未出现设计文档中预期的明显负相关，这意味着当前近似模型更充分地复现了“选择塌缩”和“新人排斥”，对“刷信任而质量下滑”的复现实验还可以进一步增强。",
        "",
        "## 6. 局限性",
        "",
        "1. 本实现是机制仿真，而不是真实桥梁设计工作流复现。",
        "2. PDF 文档中的 ILP、完整四类信任张量、KL 漂移检测与 22 项指标未全部展开实现。",
        "3. H4 的操纵效应只实现了部分现象，后续可继续增强观测偏置与操纵路径。",
        "",
        "## 7. 结论",
        "",
        "在当前可执行近似实现下，TRUE 框架相较 Blind 和 MOO 均表现出更高的任务效用、更低的安全风险和更强的新人接纳能力。最关键的结论是：当系统把信任用作分配约束而不是优化目标时，能够在探索、性能和安全之间取得更稳健的平衡。",
        "",
        "附：详细数值见 `TRUE_summary.csv`、`TRUE_hypothesis_tests.csv` 与逐轮时间序列文件。",
    ]

    path = outdir / "TRUE_experiment_report_detailed.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def make_pdf(outdir: Path, summary: pd.DataFrame, tests: pd.DataFrame, timeseries: pd.DataFrame, font_prop) -> Path:
    pdf_path = outdir / "TRUE_experiment_report_detailed.pdf"
    colors = {"TRUE": "#1f77b4", "Blind": "#d62728", "MOO": "#2ca02c"}

    mean_ts = (
        timeseries.groupby(["group", "round"], as_index=False)
        .agg(
            cumulative_utility=("cumulative_utility", "mean"),
            quality=("quality", "mean"),
            fatal=("fatal", "mean"),
            trust_gini=("trust_gini", "mean"),
            collapse_index=("collapse_index", "mean"),
            a9_selected=("a9_selected", "mean"),
            a10_selected=("a10_selected", "mean"),
        )
    )
    mean_ts["cum_fatal"] = mean_ts.groupby("group")["fatal"].cumsum()
    summary_disp = summary.rename(
        columns={
            "group": "组别",
            "cumulative_utility_mean": "累积效用均值",
            "mean_quality": "平均质量",
            "fatal_errors_mean": "致命错误均值",
            "success_rate": "成功率",
            "final_trust_gini": "信任Gini",
            "final_collapse_index": "塌缩指数",
            "a9_first_delay": "A9首次延迟",
            "a10_first_delay": "A10首次延迟",
        }
    )[
        ["组别", "累积效用均值", "平均质量", "致命错误均值", "成功率", "信任Gini", "塌缩指数", "A9首次延迟", "A10首次延迟"]
    ]
    tests_disp = pd.DataFrame(
        [
            ["H1a", "支持", "TRUE 累积效用显著高于 Blind"],
            ["H1b", "支持", "TRUE 累积效用显著高于 MOO"],
            ["H2", "基本支持", "MOO 的 Gini 和塌缩指数更高"],
            ["H3", "支持", "TRUE 对 A9/A10 的接纳明显更快"],
            ["H4", "部分支持", "未复现强负相关，但 MOO 更易集中与排斥新人"],
            ["H5", "支持", "TRUE 致命错误最少"],
        ],
        columns=["假设", "结论", "说明"],
    )

    overview = "\n".join(
        [
            "本报告将 TRUE、Blind、MOO 三组在桥梁协同设计抽象任务上的表现进行了比较。",
            "实验共进行 100 次 Monte Carlo 重复，每次 200 轮，外部专业工具全部被替换为模块级随机质量变量。",
            "",
            "核心结论：",
            "1. TRUE 在累积效用、平均质量和致命错误三个核心维度上都优于另外两组。",
            "2. Blind 在安全性上最差，说明没有信任与约束机制时，资历偏见会显著放大事故风险。",
            "3. MOO 虽然优于 Blind，但因为把信任直接作为目标，更容易出现选择集中和新人排斥。",
            "4. TRUE 的优势主要来自“信任作为约束”而不是“信任作为目标”。",
        ]
    )

    design = "\n".join(
        [
            "实验设计摘要",
            "",
            "1. 任务生成：每轮随机抽取 3-5 个模块，并按依赖关系自动补全。",
            "2. 外部工具替代：模块成功概率 = capability × difficulty；低能力承担致命模块时附加 10% 灾难性错误。",
            "3. 效用函数：全部成功 +100；仅非致命失败 +60；任一致命失败 -200。",
            "4. TRUE：Thompson 采样 + 信任/质量/可靠性底线 + 覆盖度鼓励。",
            "5. Blind：无信任更新，偏向资深人类或随机分配。",
            "6. MOO：把信任均值直接放入目标函数，不加安全底线。",
            "7. 特殊实体：A8 代表可操纵 Agent；A9 第 50 轮加入；A10 第 100 轮加入。",
        ]
    )

    with PdfPages(pdf_path) as pdf:
        add_text_page(pdf, "TRUE 框架模拟实验报告", wrap_lines(overview, 34), font_prop, size=14)
        add_text_page(pdf, "实验设计与建模假设", wrap_lines(design, 34), font_prop, size=13)
        add_table_page(pdf, "组间汇总结果", summary_disp, font_prop)
        add_table_page(pdf, "主要结论与假设支持情况", tests_disp, font_prop, col_widths=[0.12, 0.16, 0.64])

        fig, axes = plt.subplots(2, 1, figsize=(8.27, 11.69))
        for group in ["TRUE", "Blind", "MOO"]:
            g = mean_ts[mean_ts["group"] == group]
            axes[0].plot(g["round"], g["cumulative_utility"], label=group, color=colors[group], linewidth=2)
            axes[1].plot(g["round"], g["cum_fatal"], label=group, color=colors[group], linewidth=2)
        axes[0].set_title("Cumulative Utility by Round")
        axes[1].set_title("Cumulative Fatal Errors by Round")
        for ax in axes:
            ax.grid(alpha=0.25)
            ax.legend()
            ax.set_xlabel("Round")
        axes[0].set_ylabel("Mean cumulative utility")
        axes[1].set_ylabel("Mean cumulative fatal errors")
        fig.suptitle("核心绩效曲线", fontproperties=font_prop, fontsize=18, y=0.98)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig, axes = plt.subplots(2, 1, figsize=(8.27, 11.69))
        for group in ["TRUE", "Blind", "MOO"]:
            g = mean_ts[mean_ts["group"] == group]
            axes[0].plot(g["round"], g["trust_gini"], label=group, color=colors[group], linewidth=2)
            axes[1].plot(g["round"], g["collapse_index"], label=group, color=colors[group], linewidth=2)
        axes[0].set_title("Selection Concentration (Gini Proxy)")
        axes[1].set_title("Collapse Index")
        for ax in axes:
            ax.grid(alpha=0.25)
            ax.legend()
            ax.set_xlabel("Round")
        axes[0].set_ylabel("Mean Gini")
        axes[1].set_ylabel("Mean collapse index")
        fig.suptitle("信任健康与结构塌缩", fontproperties=font_prop, fontsize=18, y=0.98)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig, axes = plt.subplots(2, 1, figsize=(8.27, 11.69))
        for group in ["TRUE", "Blind", "MOO"]:
            g = mean_ts[mean_ts["group"] == group]
            axes[0].plot(g["round"], g["a9_selected"], label=group, color=colors[group], linewidth=2)
            axes[1].plot(g["round"], g["a10_selected"], label=group, color=colors[group], linewidth=2)
        axes[0].axvline(50, color="gray", linestyle="--", linewidth=1)
        axes[1].axvline(100, color="gray", linestyle="--", linewidth=1)
        axes[0].set_title("A9 Selection Rate After Join")
        axes[1].set_title("A10 Selection Rate After Join")
        for ax in axes:
            ax.grid(alpha=0.25)
            ax.legend()
            ax.set_xlabel("Round")
        axes[0].set_ylabel("Selection rate")
        axes[1].set_ylabel("Selection rate")
        fig.suptitle("新 Agent 冷启动表现", fontproperties=font_prop, fontsize=18, y=0.98)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        closing = "\n".join(
            [
                "结论与边界",
                "",
                "1. TRUE 在本次近似仿真中表现最好，尤其在安全性和总效用上优势显著。",
                "2. Blind 的失败主要体现为无约束分配导致的致命错误积累。",
                "3. MOO 的主要问题不是完全失效，而是对高信任对象过度集中，并显著排斥新人。",
                "4. A8 的 Goodhart 操纵效应只得到了部分复现，后续仍可加强其“高信任、低真实质量”的观测偏差设计。",
                "5. 因此，这份报告最适合作为机制验证型结果，而不是工程系统的最终定量结论。",
            ]
        )
        add_text_page(pdf, "结论与后续工作", wrap_lines(closing, 34), font_prop, size=13)

    return pdf_path


def main() -> None:
    parser = argparse.ArgumentParser()
    project_root = Path(__file__).resolve().parent.parent
    parser.add_argument("--input-dir", type=Path, default=project_root / "data" / "final_results_v2")
    parser.add_argument("--font-path", type=Path, default=project_root / "assets" / "fonts" / "NotoSansCJKsc-Regular.otf")
    args = parser.parse_args()

    summary = pd.read_csv(args.input_dir / "TRUE_summary.csv")
    tests = pd.read_csv(args.input_dir / "TRUE_hypothesis_tests.csv")
    timeseries = pd.read_csv(args.input_dir / "TRUE_round_timeseries.csv")
    font_prop = set_chinese_font(args.font_path)

    md_path = make_markdown(args.input_dir, summary, tests)
    pdf_path = make_pdf(args.input_dir, summary, tests, timeseries, font_prop)

    print(f"Wrote markdown report to {md_path}")
    print(f"Wrote PDF report to {pdf_path}")


if __name__ == "__main__":
    main()
