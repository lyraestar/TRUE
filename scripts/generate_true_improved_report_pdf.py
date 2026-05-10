#!/usr/bin/env python3
"""Generate a professionally formatted PDF report for the improved TRUE experiment."""

from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle


SCENARIO_ORDER = [
    "baseline",
    "safety_critical",
    "observation_manipulated",
    "utility_trust_misalignment",
]

SCENARIO_LABELS = {
    "baseline": "Baseline",
    "safety_critical": "Safety-Critical",
    "observation_manipulated": "Observation-Manipulated",
    "utility_trust_misalignment": "Utility-Trust-Misalignment",
}

SCENARIO_DESCRIPTIONS = {
    "baseline": "标准参考环境，观测噪声适中，任务结构与上一轮实验保持连续可比。",
    "safety_critical": "高风险高惩罚环境，致命错误代价更高，依赖误差传播更强。",
    "observation_manipulated": "观测污染环境，将真实质量与表面质量分离，用于检验 Goodhart 式误导。",
    "utility_trust_misalignment": "局部错位环境，短期效用、当前信任与长期信息价值在阶段性上不一致。",
}

GROUP_COLORS = {"TRUE": "#1f5aa6", "Blind": "#c73e1d", "MOO": "#2b8a3e"}


def fmt(x: float, digits: int = 3) -> str:
    return f"{float(x):.{digits}f}"


def set_chinese_font(font_path: Path):
    font_manager.fontManager.addfont(str(font_path))
    return font_manager.FontProperties(fname=str(font_path))


def wrap(text: str, width: int = 38) -> str:
    blocks = []
    for para in text.split("\n"):
        if not para.strip():
            blocks.append("")
            continue
        blocks.extend(textwrap.wrap(para, width=width, break_long_words=False, break_on_hyphens=False))
    return "\n".join(blocks)


def add_page_base(fig, title: str, subtitle: str | None, font_prop, page_no: int) -> None:
    fig.patch.set_facecolor("#f7f7f5")
    fig.add_artist(Rectangle((0, 0.965), 1, 0.035, transform=fig.transFigure, color="#143b63", zorder=0))
    fig.add_artist(Rectangle((0.06, 0.06), 0.88, 0.86, transform=fig.transFigure, color="white", zorder=0))
    fig.text(0.08, 0.93, title, fontproperties=font_prop, fontsize=22, weight="bold", color="#143b63", va="top")
    if subtitle:
        fig.text(0.08, 0.90, subtitle, fontproperties=font_prop, fontsize=10.5, color="#5c6773", va="top")
    fig.text(0.92, 0.035, f"{page_no}", fontproperties=font_prop, fontsize=9, color="#7b8794", ha="right")


def add_cover_page(pdf: PdfPages, font_prop, runs: int, rounds: int) -> None:
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.patch.set_facecolor("#153a5b")
    fig.add_artist(Rectangle((0.07, 0.09), 0.86, 0.82, transform=fig.transFigure, color="#f7f7f5", zorder=0))
    fig.text(0.11, 0.80, "TRUE 框架改进版", fontproperties=font_prop, fontsize=30, weight="bold", color="#153a5b")
    fig.text(0.11, 0.74, "参数化场景族模拟实验报告", fontproperties=font_prop, fontsize=24, weight="bold", color="#153a5b")
    fig.text(
        0.11,
        0.63,
        wrap(
            "本报告面向当前不接入真实工具的约束条件，基于概率模型对多场景协作系统进行机制级评估。"
            "相较上一轮单场景实验，本轮将场景差异系统地编码进成功率、效用函数、观测污染和信任更新机制。"
        ),
        fontproperties=font_prop,
        fontsize=13,
        color="#2f3b47",
        va="top",
        linespacing=1.6,
    )
    fig.text(0.11, 0.40, f"Monte Carlo 重复次数: {runs}", fontproperties=font_prop, fontsize=13, color="#153a5b")
    fig.text(0.11, 0.36, f"每次实验轮数: {rounds}", fontproperties=font_prop, fontsize=13, color="#153a5b")
    fig.text(0.11, 0.32, "比较对象: TRUE / Blind / MOO", fontproperties=font_prop, fontsize=13, color="#153a5b")
    fig.text(0.11, 0.12, "Generated from TRUE improved scenario-family experiment", fontsize=10, color="#5c6773")
    plt.axis("off")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def add_text_page(pdf: PdfPages, title: str, body: str, font_prop, page_no: int, subtitle: str | None = None, size: int = 12) -> None:
    fig = plt.figure(figsize=(8.27, 11.69))
    add_page_base(fig, title, subtitle, font_prop, page_no)
    fig.text(0.09, 0.86, body, fontproperties=font_prop, fontsize=size, color="#25313c", va="top", linespacing=1.65)
    plt.axis("off")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def add_table_page(
    pdf: PdfPages,
    title: str,
    df: pd.DataFrame,
    font_prop,
    page_no: int,
    subtitle: str | None = None,
    bbox=(0.05, 0.10, 0.90, 0.74),
    fontsize: int = 9,
    col_widths=None,
) -> None:
    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    add_page_base(fig, title, subtitle, font_prop, page_no)
    ax.axis("off")
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda x: fmt(x, 3))
    table = ax.table(
        cellText=display.values,
        colLabels=display.columns,
        cellLoc="center",
        colLoc="center",
        bbox=bbox,
        colWidths=col_widths,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(fontsize)
    table.scale(1, 1.55)
    for (row, col), cell in table.get_celld().items():
        cell.get_text().set_fontproperties(font_prop)
        cell.set_edgecolor("#d8dee4")
        cell.set_linewidth(0.6)
        if row == 0:
            cell.set_facecolor("#dbeafe")
            cell.get_text().set_weight("bold")
        elif row % 2 == 1:
            cell.set_facecolor("#f8fafc")
        else:
            cell.set_facecolor("white")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def add_scenario_grid_page(pdf: PdfPages, font_prop, page_no: int) -> None:
    fig = plt.figure(figsize=(8.27, 11.69))
    add_page_base(fig, "场景族设计", "本轮实验通过参数化概率模型来表达环境差异，而非更换任务领域。", font_prop, page_no)
    positions = [
        (0.09, 0.58, 0.36, 0.20),
        (0.55, 0.58, 0.36, 0.20),
        (0.09, 0.30, 0.36, 0.20),
        (0.55, 0.30, 0.36, 0.20),
    ]
    colors = ["#e0f2fe", "#fef3c7", "#ede9fe", "#dcfce7"]
    for (scenario, pos, color) in zip(SCENARIO_ORDER, positions, colors):
        x, y, w, h = pos
        fig.add_artist(Rectangle((x, y), w, h, transform=fig.transFigure, facecolor=color, edgecolor="#cbd5e1", linewidth=0.8))
        fig.text(x + 0.02, y + h - 0.03, SCENARIO_LABELS[scenario], fontproperties=font_prop, fontsize=14, weight="bold", color="#1e293b", va="top")
        fig.text(
            x + 0.02,
            y + h - 0.08,
            wrap(SCENARIO_DESCRIPTIONS[scenario], 20),
            fontproperties=font_prop,
            fontsize=10.5,
            color="#334155",
            va="top",
            linespacing=1.5,
        )
    fig.text(
        0.09,
        0.18,
        wrap(
            "四类场景分别覆盖了标准参考、高安全惩罚、观测污染和局部效用-信任错位四种关键机制。"
            "这样做的目的，是把“场景差异”直接落实到概率模型假设，而不是通过更换领域或接入外部工具来制造表面复杂度。"
        ),
        fontproperties=font_prop,
        fontsize=11.5,
        color="#25313c",
        va="top",
        linespacing=1.6,
    )
    plt.axis("off")
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def add_plot_page(pdf: PdfPages, title: str, subtitle: str, font_prop, page_no: int, plot_fn) -> None:
    fig = plt.figure(figsize=(8.27, 11.69))
    add_page_base(fig, title, subtitle, font_prop, page_no)
    plot_fn(fig)
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def scenario_summary_text(summary_df: pd.DataFrame) -> str:
    blocks = []
    for scenario in SCENARIO_ORDER:
        rs = summary_df[summary_df["scenario"] == scenario].set_index("group")
        tr, bl, mo = rs.loc["TRUE"], rs.loc["Blind"], rs.loc["MOO"]
        blocks.append(
            f"{SCENARIO_LABELS[scenario]}：TRUE 累积效用为 {fmt(tr['cumulative_utility_mean'],1)}，"
            f" 相比 Blind 高 {fmt(tr['cumulative_utility_mean'] - bl['cumulative_utility_mean'],1)}，"
            f" 相比 MOO 高 {fmt(tr['cumulative_utility_mean'] - mo['cumulative_utility_mean'],1)}；"
            f" TRUE 的致命错误均值为 {fmt(tr['fatal_errors_mean'],1)}，"
            f" MOO 为 {fmt(mo['fatal_errors_mean'],1)}。"
        )
    return "\n\n".join(blocks)


def build_markdown(outdir: Path, summary_df: pd.DataFrame, tests_df: pd.DataFrame) -> Path:
    lines = [
        "# TRUE 改进版专业实验报告",
        "",
        "## 执行摘要",
        "",
        "本报告基于参数化场景族，对 TRUE、Blind 与 MOO 三种多人多 Agent 协作机制进行了新一轮模拟对比。"
        "实验不引入真实外部工具，而是通过概率模型对任务成功、表面观测、延迟反馈和局部错位现象进行统一建模。",
        "",
        "本轮实验表明，TRUE 在四类场景下都显著优于 Blind，并且相对 MOO 也保持稳定优势。"
        "其中，Observation-Manipulated 场景最清楚地展示了将信任作为目标函数时可能带来的误导性分配问题，"
        "而 Utility-Trust-Misalignment 场景则更直接说明了 TRUE 在保留长期信息价值方面的机制优势。",
        "",
        "## 场景结果摘要",
        "",
        scenario_summary_text(summary_df),
        "",
        "## 结果表与检验",
        "",
        summary_df.to_markdown(index=False),
        "",
        tests_df.to_markdown(index=False),
    ]
    path = outdir / "TRUE_improved_experiment_report_professional.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    project_root = Path(__file__).resolve().parent.parent
    parser.add_argument("--input-dir", type=Path, default=project_root / "data" / "improved_results_v1")
    parser.add_argument("--output-dir", type=Path, default=project_root / "reports" / "improved")
    parser.add_argument("--font-path", type=Path, default=project_root / "assets" / "fonts" / "NotoSansCJKsc-Regular.otf")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    font_prop = set_chinese_font(args.font_path)
    summary = pd.read_csv(args.input_dir / "TRUE_improved_summary.csv")
    tests = pd.read_csv(args.input_dir / "TRUE_improved_tests.csv")
    timeseries = pd.read_csv(args.input_dir / "TRUE_improved_round_timeseries.csv")
    summary["scenario_order"] = summary["scenario"].map({name: i for i, name in enumerate(SCENARIO_ORDER)})
    summary = summary.sort_values(["scenario_order", "group"]).drop(columns=["scenario_order"])
    tests["scenario_order"] = tests["scenario"].map({name: i for i, name in enumerate(SCENARIO_ORDER)})
    tests = tests.sort_values(["scenario_order", "hypothesis"]).drop(columns=["scenario_order"])

    md_path = build_markdown(args.output_dir, summary, tests)
    pdf_path = args.output_dir / "TRUE_improved_experiment_report_professional.pdf"

    summary_disp = summary.rename(
        columns={
            "scenario": "场景",
            "group": "组别",
            "cumulative_utility_mean": "累积效用均值",
            "mean_quality_true": "真实质量均值",
            "mean_quality_surface": "表面质量均值",
            "fatal_errors_mean": "致命错误均值",
            "success_rate": "成功率",
            "final_trust_gini": "选择Gini",
            "final_collapse_index": "塌缩指数",
            "a9_first_delay": "A9首次延迟",
            "a8_trust_quality_corr": "A8信任-质量相关",
        }
    )
    summary_disp["场景"] = summary_disp["场景"].map(SCENARIO_LABELS)
    summary_disp = summary_disp[
        ["场景", "组别", "累积效用均值", "真实质量均值", "表面质量均值", "致命错误均值", "成功率", "选择Gini", "塌缩指数", "A9首次延迟", "A8信任-质量相关"]
    ]

    tests_disp = tests.rename(
        columns={
            "scenario": "场景",
            "hypothesis": "假设",
            "metric": "指标",
            "mean_diff": "均值差",
            "t": "t值",
            "p_approx": "近似p值",
            "cohens_d": "效应量d",
        }
    )
    tests_disp["场景"] = tests_disp["场景"].map(SCENARIO_LABELS)

    mean_ts = (
        timeseries.groupby(["scenario", "group", "round"], as_index=False)
        .agg(
            cumulative_utility=("cumulative_utility", "mean"),
            quality_true=("quality_true", "mean"),
            quality_surface=("quality_surface", "mean"),
            fatal=("fatal", "mean"),
            trust_gini=("trust_gini", "mean"),
            collapse_index=("collapse_index", "mean"),
            a9_selected=("a9_selected", "mean"),
            a10_selected=("a10_selected", "mean"),
        )
    )
    mean_ts["cum_fatal"] = mean_ts.groupby(["scenario", "group"])["fatal"].cumsum()

    executive_summary = wrap(
        "本轮实验的核心改进，是把原来的单一任务环境扩展成四类参数化场景，并明确区分真实质量、表面质量和最终观测信号。"
        "这样一来，实验不再只回答“TRUE 在一个默认环境里是否更好”，而开始回答“在高风险、观测污染、局部错位等不同环境下，"
        "TRUE 与 Blind、MOO 的相对优势是否稳定，以及这种优势具体来自哪些机制”。\n\n"
        "整体来看，TRUE 在四类场景下都取得了最优或显著更优的综合表现：它在累积效用上持续领先，"
        "在致命错误上明显更低，同时对 A9/A10 这类新加入实体的接纳速度远快于 MOO。"
        "其中，Observation-Manipulated 场景最有力地展示了 MOO 在表面信号污染下的脆弱性；"
        "Utility-Trust-Misalignment 场景则说明了 TRUE 能更好地平衡短期收益与长期信息价值。",
        40,
    )

    mechanism_body = wrap(
        "改进版实验在机理上引入了四项关键变化：\n"
        "1. 三层质量结构：每个模块同时生成真实质量 q_true、表面质量 q_surface 和最终观测 q_obs，从而将“做得好”和“看起来好”区分开。\n"
        "2. 条件依赖传播：上游模块失败会降低下游模块成功率，但高能力执行者可以部分修复依赖链上的损失。\n"
        "3. 场景化效用函数：不同场景改变致命错误惩罚、观测权重、误差传播强度与局部阶段性收益结构。\n"
        "4. 保持组间公平：TRUE、Blind、MOO 在相同任务流和相同场景参数下对比，只改变决策与信任机制。",
        40,
    )

    interpretations = []
    for scenario in SCENARIO_ORDER:
        rs = summary[summary["scenario"] == scenario].set_index("group")
        tr, bl, mo = rs.loc["TRUE"], rs.loc["Blind"], rs.loc["MOO"]
        paragraph = (
            f"{SCENARIO_LABELS[scenario]}：TRUE 的累积效用为 {fmt(tr['cumulative_utility_mean'],1)}，"
            f" 相比 Blind 高 {fmt(tr['cumulative_utility_mean'] - bl['cumulative_utility_mean'],1)}，"
            f" 相比 MOO 高 {fmt(tr['cumulative_utility_mean'] - mo['cumulative_utility_mean'],1)}。"
            f" 同时，TRUE 的致命错误均值为 {fmt(tr['fatal_errors_mean'],1)}，低于 Blind 的 {fmt(bl['fatal_errors_mean'],1)}"
            f" 和 MOO 的 {fmt(mo['fatal_errors_mean'],1)}。"
        )
        if scenario == "observation_manipulated":
            paragraph += (
                f" 这一场景中，MOO 的表面质量均值高达 {fmt(mo['mean_quality_surface'])}，但真实质量仅为 {fmt(mo['mean_quality_true'])}，"
                " 清楚说明了将信任直接纳入目标函数会放大表面信号污染带来的误导。"
            )
        elif scenario == "utility_trust_misalignment":
            paragraph += (
                f" MOO 对 A9 的首次接纳延迟达到 {fmt(mo['a9_first_delay'],1)}，而 TRUE 仅为 {fmt(tr['a9_first_delay'],1)}，"
                " 表明 TRUE 更能容纳“短期不占优但长期有价值”的低历史实体。"
            )
        elif scenario == "safety_critical":
            paragraph += (
                " 高风险场景下三组整体效用都被大幅拉低，但 TRUE 仍然保持了更低的事故数量和更快的新实体纳入速度。"
            )
        else:
            paragraph += " 这说明即使在标准参考环境下，约束式信任仍然优于盲目分配与信任目标化分配。"
        interpretations.append(paragraph)

    with PdfPages(pdf_path) as pdf:
        page = 1
        add_cover_page(pdf, font_prop, 60, 200)
        page += 1

        add_text_page(
            pdf,
            "执行摘要",
            executive_summary,
            font_prop,
            page_no=page,
            subtitle="本页用于给出管理层可快速读取的总体结论。",
            size=12,
        )
        page += 1

        add_text_page(
            pdf,
            "实验机理与建模逻辑",
            mechanism_body,
            font_prop,
            page_no=page,
            subtitle="改进版实验与上一轮单场景实验的关键差别在于概率模型分层和场景参数化。",
            size=11.5,
        )
        page += 1

        add_scenario_grid_page(pdf, font_prop, page)
        page += 1

        add_table_page(
            pdf,
            "核心结果总表",
            summary_disp,
            font_prop,
            page_no=page,
            subtitle="四类场景 × 三组机制的主要结果指标。",
            bbox=(0.03, 0.09, 0.94, 0.76),
            fontsize=8.6,
        )
        page += 1

        add_table_page(
            pdf,
            "主要统计检验",
            tests_disp.iloc[:12],
            font_prop,
            page_no=page,
            subtitle="前 12 条检验结果。",
            bbox=(0.03, 0.10, 0.94, 0.75),
            fontsize=8.2,
        )
        page += 1

        add_table_page(
            pdf,
            "主要统计检验（续）",
            tests_disp.iloc[12:],
            font_prop,
            page_no=page,
            subtitle="剩余检验结果。",
            bbox=(0.03, 0.10, 0.94, 0.75),
            fontsize=8.2,
        )
        page += 1

        def plot_utilities(fig):
            for idx, scenario in enumerate(SCENARIO_ORDER, start=1):
                ax = fig.add_axes([0.08 + ((idx - 1) % 2) * 0.44, 0.54 - ((idx - 1) // 2) * 0.36, 0.34, 0.24])
                for group in ("TRUE", "Blind", "MOO"):
                    g = mean_ts[(mean_ts["scenario"] == scenario) & (mean_ts["group"] == group)]
                    ax.plot(g["round"], g["cumulative_utility"], color=GROUP_COLORS[group], linewidth=2, label=group)
                ax.set_title(SCENARIO_LABELS[scenario], fontsize=10)
                ax.grid(alpha=0.25)
                ax.set_xlabel("Round", fontsize=9)
                ax.set_ylabel("Mean cum. utility", fontsize=9)
                if idx == 1:
                    ax.legend(fontsize=8, loc="best")

        add_plot_page(
            pdf,
            "累积效用曲线",
            "四类场景下 TRUE、Blind、MOO 的平均累积效用随轮数变化。",
            font_prop,
            page,
            plot_utilities,
        )
        page += 1

        def plot_risks(fig):
            for idx, scenario in enumerate(SCENARIO_ORDER, start=1):
                ax = fig.add_axes([0.08 + ((idx - 1) % 2) * 0.44, 0.54 - ((idx - 1) // 2) * 0.36, 0.34, 0.24])
                for group in ("TRUE", "Blind", "MOO"):
                    g = mean_ts[(mean_ts["scenario"] == scenario) & (mean_ts["group"] == group)]
                    ax.plot(g["round"], g["cum_fatal"], color=GROUP_COLORS[group], linewidth=2, label=group)
                ax.set_title(SCENARIO_LABELS[scenario], fontsize=10)
                ax.grid(alpha=0.25)
                ax.set_xlabel("Round", fontsize=9)
                ax.set_ylabel("Cum. fatal errors", fontsize=9)
                if idx == 1:
                    ax.legend(fontsize=8, loc="best")

        add_plot_page(
            pdf,
            "致命错误累积曲线",
            "该页强调安全性差异，尤其用于对比 TRUE 的约束机制与 Blind/MOO 的风险暴露。",
            font_prop,
            page,
            plot_risks,
        )
        page += 1

        def plot_health(fig):
            for idx, scenario in enumerate(SCENARIO_ORDER, start=1):
                ax = fig.add_axes([0.08 + ((idx - 1) % 2) * 0.44, 0.54 - ((idx - 1) // 2) * 0.36, 0.34, 0.24])
                for group in ("TRUE", "Blind", "MOO"):
                    g = mean_ts[(mean_ts["scenario"] == scenario) & (mean_ts["group"] == group)]
                    ax.plot(g["round"], g["collapse_index"], color=GROUP_COLORS[group], linewidth=2, label=group)
                ax.set_title(SCENARIO_LABELS[scenario], fontsize=10)
                ax.grid(alpha=0.25)
                ax.set_xlabel("Round", fontsize=9)
                ax.set_ylabel("Collapse index", fontsize=9)
                if idx == 1:
                    ax.legend(fontsize=8, loc="best")

        add_plot_page(
            pdf,
            "结构塌缩对比",
            "该页重点刻画 MOO 在高信任目标化条件下更容易出现的选择集中和结构塌缩。",
            font_prop,
            page,
            plot_health,
        )
        page += 1

        def plot_surface_gap(fig):
            for idx, scenario in enumerate(SCENARIO_ORDER, start=1):
                ax = fig.add_axes([0.08 + ((idx - 1) % 2) * 0.44, 0.54 - ((idx - 1) // 2) * 0.36, 0.34, 0.24])
                for group in ("TRUE", "Blind", "MOO"):
                    g = mean_ts[(mean_ts["scenario"] == scenario) & (mean_ts["group"] == group)]
                    ax.plot(g["round"], g["quality_true"], color=GROUP_COLORS[group], linewidth=2, label=f"{group}-true")
                    ax.plot(g["round"], g["quality_surface"], color=GROUP_COLORS[group], linewidth=1.4, linestyle="--", alpha=0.85)
                ax.set_title(SCENARIO_LABELS[scenario], fontsize=10)
                ax.grid(alpha=0.25)
                ax.set_xlabel("Round", fontsize=9)
                ax.set_ylabel("Quality", fontsize=9)
                if idx == 1:
                    ax.legend(fontsize=7, loc="best")

        add_plot_page(
            pdf,
            "真实质量与表面质量",
            "虚线表示表面质量，实线表示真实质量。Observation-Manipulated 场景中的分离最为明显。",
            font_prop,
            page,
            plot_surface_gap,
        )
        page += 1

        add_text_page(
            pdf,
            "分场景结果解释",
            wrap("\n\n".join(interpretations), 39),
            font_prop,
            page_no=page,
            subtitle="该页对四类场景的机制差异进行逐项解释，而不是仅重复数字。",
            size=11.4,
        )
        page += 1

        conclusion = wrap(
            "本轮改进版实验说明，TRUE 的优势并不依赖单一默认场景，而是在多种概率模型环境中都表现出稳定性。"
            "当环境更强调安全约束时，TRUE 可以更好地压住事故；当环境存在观测污染时，TRUE 能更有效地区分真实质量和表面质量；"
            "当局部阶段存在短期效用、当前信任与长期信息价值的不一致时，TRUE 仍然能够更快接纳高潜力低历史实体。"
            "\n\n"
            "更重要的是，这份报告把“场景差异来自哪里”交代得更清楚：场景差异不来自领域切换，而来自概率模型、效用结构、观测结构和更新规则的改变。"
            "这使得后续继续做敏感性分析、协议固定和机制扩展会更加顺畅。",
            40,
        )
        add_text_page(
            pdf,
            "结论与后续工作",
            conclusion,
            font_prop,
            page_no=page,
            subtitle="下一步建议在此基础上补 protocol、参数敏感性分析和更正式的统计稳健性检验。",
            size=12,
        )

    print(f"Wrote markdown report to {md_path}")
    print(f"Wrote PDF report to {pdf_path}")


if __name__ == "__main__":
    main()
