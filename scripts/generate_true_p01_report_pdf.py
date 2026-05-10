#!/usr/bin/env python3
"""Generate a formal PDF report with time-series line charts for TRUE P0/P1 experiment."""

import csv
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
)

DATA_DIR = Path(__file__).parent.parent / "data" / "p01_results"
OUT_PATH = Path(__file__).parent.parent / "reports" / "p01" / "TRUE_p01_experiment_report.pdf"
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

GROUP_COLORS = {
    "TRUE": "#1f77b4",
    "TRUE-no-cap": "#aec7e8",
    "TRUE-C": "#ff7f0e",
    "TRUE-E": "#2ca02c",
    "TRUE-N": "#d62728",
    "Blind": "#9467bd",
    "TTB": "#8c564b",
    "TTB-cap": "#bcbd22",
    "MOO": "#e377c2",
    "MOO-cap": "#17becf",
}

GROUP_LABELS = {
    "TRUE": "TRUE",
    "TRUE-no-cap": "TRUE-no-cap",
    "TRUE-C": "TRUE-C (no constraints)",
    "TRUE-E": "TRUE-E (no exploration)",
    "TRUE-N": "TRUE-N (no newcomer)",
    "Blind": "Blind",
    "TTB": "TTB",
    "TTB-cap": "TTB-cap",
    "MOO": "MOO",
    "MOO-cap": "MOO-cap",
}

SCENARIO_LABELS = {
    "baseline": "Baseline",
    "safety_critical": "Safety-Critical",
    "observation_manipulated": "Observation-Manipulated",
    "utility_trust_misalignment": "Utility-Trust-Misalignment",
}


def load_summary(path: Path) -> List[dict]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            rows.append(r)
    return rows


def load_tests(path: Path) -> List[dict]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            rows.append(r)
    return rows


def load_timeseries(path: Path) -> Dict[Tuple[str, str, int], dict]:
    accum: Dict[Tuple[str, str, int], List[dict]] = defaultdict(list)
    with path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            key = (row["scenario"], row["group"], int(row["round"]))
            accum[key].append(row)
    out = {}
    for key, vals in accum.items():
        n = len(vals)
        out[key] = {
            "cumulative_utility": sum(float(v["cumulative_utility"]) for v in vals) / n,
            "fatal": sum(float(v["fatal"]) for v in vals) / n,
            "trust_gini": sum(float(v["trust_gini"]) for v in vals) / n,
            "collapse_index": sum(float(v["collapse_index"]) for v in vals) / n,
            "a9_selected": sum(float(v["a9_selected"]) for v in vals) / n,
            "quality_true": sum(float(v["quality_true"]) for v in vals) / n,
            "quality_surface": sum(float(v["quality_surface"]) for v in vals) / n,
        }
    return out


def make_line_chart(data, scenario, metric, ylabel, title, tmpdir, symlog=False):
    groups = sorted({k[1] for k in data if k[0] == scenario},
                    key=lambda g: list(GROUP_COLORS.keys()).index(g) if g in GROUP_COLORS else 99)
    rounds = sorted({k[2] for k in data if k[0] == scenario})

    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    for group in groups:
        xs = []
        ys = []
        for r in rounds:
            val = data.get((scenario, group, r), {}).get(metric, 0)
            xs.append(r)
            ys.append(val)
        ax.plot(xs, ys, label=GROUP_LABELS.get(group, group),
                color=GROUP_COLORS.get(group, "#333333"), linewidth=1.3)

    ax.set_xlabel("Round", fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_title(title, fontsize=11, fontweight="bold")
    if symlog:
        ax.set_yscale("symlog", linthresh=50)
        ax.set_ylabel(ylabel + " (symlog)", fontsize=10)
    ax.legend(loc="best", fontsize=7.5, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(1, max(rounds))
    fig.tight_layout()
    out = tmpdir / f"{scenario}_{metric}.png"
    fig.savefig(out, dpi=180)
    plt.close(fig)
    return out


def make_all_charts(data, tmpdir):
    charts = {}
    scenarios = sorted({k[0] for k in data})
    metrics = [
        ("cumulative_utility", "Cumulative Utility", "Cumulative Utility"),
        ("fatal", "Fatal Errors (per round)", "Fatal Errors"),
        ("trust_gini", "Trust Gini", "Trust Gini"),
        ("collapse_index", "Collapse Index", "Collapse Index"),
    ]
    for scenario in scenarios:
        charts[scenario] = {}
        for metric, ylabel, title_suffix in metrics:
            title = f"{SCENARIO_LABELS.get(scenario, scenario)} — {title_suffix}"
            use_symlog = metric in ("cumulative_utility", "fatal")
            charts[scenario][metric] = make_line_chart(data, scenario, metric, ylabel, title, tmpdir, symlog=use_symlog)
    return charts


def fmt_f(x, digits=1):
    try:
        return f"{float(x):.{digits}f}"
    except ValueError:
        return x


def build_pdf(summary, tests, charts, out):
    doc = SimpleDocTemplate(str(out), pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("Title", parent=styles["Title"], fontSize=20, spaceAfter=16, alignment=1)
    h1_style = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=16, spaceAfter=10, spaceBefore=14)
    h2_style = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=13, spaceAfter=8, spaceBefore=12)
    body_style = ParagraphStyle("Body", parent=styles["BodyText"], fontSize=9.5, leading=14, alignment=4)
    small_style = ParagraphStyle("Small", parent=styles["BodyText"], fontSize=8, leading=12)

    story = []

    # Cover
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("TRUE Simulation Experiment Report", title_style))
    story.append(Paragraph("P0/P1 Refactored Round", title_style))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Trust-Reliability Unified Engineering<br/>Multi-Agent Collaboration Simulation", body_style))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("100 runs x 200 rounds x 4 scenarios x 7 groups<br/>Fixed task-flow pairing | Bootstrap CIs | Bonferroni correction", small_style))
    story.append(PageBreak())

    # Executive Summary
    story.append(Paragraph("Executive Summary", h1_style))
    story.append(Paragraph("""
    This report presents the P0/P1 refactored experimental results for the TRUE (Trust-Reliability Unified Engineering)
    multi-agent collaboration framework. All groups within each Monte Carlo run face the identical task sequence,
    ensuring that outcome differences are attributable to selection mechanisms rather than task luck.
    """, body_style))
    story.append(Paragraph("""
    <b>Key changes:</b> (1) Fixed task-flow pairing; (2) Removed group-specific observation manipulation for A8;
    (3) Renamed MOO to TTB (Trust-Targeted Baseline) and added a proper MOO baseline using weighted Tchebycheff;
    (4) Added ablation variants TRUE-C, TRUE-E, TRUE-N;
    (5) Wilcoxon signed-rank test + bootstrap 95% CIs + Bonferroni correction.
    """, body_style))
    story.append(Spacer(1, 0.5*cm))

    # Scenario table
    story.append(Paragraph("Scenario Definitions", h2_style))
    scen_data = [
        ["Scenario", "Description"],
        ["Baseline", "Standard engineering collaboration with moderate observation noise."],
        ["Safety-Critical", "High-stakes safety environment with harsher penalties and stronger error propagation."],
        ["Observation-Manipulated", "Observation-contaminated environment where surface quality diverges from true quality."],
        ["Utility-Trust-Misalignment", "Local phases where trusted incumbents underperform and low-history entities hold latent value."],
    ]
    scen_tbl = Table(scen_data, colWidths=[4*cm, 11*cm])
    scen_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(scen_tbl)
    story.append(PageBreak())

    # Results Summary Table
    story.append(Paragraph("Results Summary", h1_style))
    story.append(Paragraph("Mean cumulative utility, 95% bootstrap CI, fatal errors, and key metrics per scenario and group.", body_style))
    story.append(Spacer(1, 0.3*cm))

    tbl_header = ["Scenario", "Group", "Cum.Utility", "95% CI", "Fatal", "True Q", "Gini", "Collapse", "A9 Delay"]
    tbl_rows = [tbl_header]
    for row in sorted(summary, key=lambda r: (list(SCENARIO_LABELS.keys()).index(r["scenario"]), list(GROUP_COLORS.keys()).index(r["group"]))):
        ci = f"[{fmt_f(row['cumulative_utility_ci_lo'])}, {fmt_f(row['cumulative_utility_ci_hi'])}]"
        tbl_rows.append([
            SCENARIO_LABELS.get(row["scenario"], row["scenario"]),
            GROUP_LABELS.get(row["group"], row["group"]),
            fmt_f(row["cumulative_utility_mean"]),
            ci,
            fmt_f(row["fatal_errors_mean"], 1),
            fmt_f(row["mean_quality_true"], 3),
            fmt_f(row["final_trust_gini"], 3),
            fmt_f(row["final_collapse_index"], 3),
            fmt_f(row["a9_first_delay"], 1),
        ])

    t = Table(tbl_rows, colWidths=[3.2*cm, 3.6*cm, 2.2*cm, 3.0*cm, 1.4*cm, 1.6*cm, 1.4*cm, 1.6*cm, 1.4*cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTSIZE", (0, 0), (-1, 0), 8.5),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 1), (-1, -1), 7.5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t)
    story.append(PageBreak())

    # Charts per scenario
    for scenario in sorted(charts.keys(), key=lambda s: list(SCENARIO_LABELS.keys()).index(s)):
        story.append(Paragraph(f"{SCENARIO_LABELS.get(scenario, scenario)} — Time-Series Analysis", h1_style))
        story.append(Spacer(1, 0.2*cm))

        for metric in ["cumulative_utility", "fatal", "trust_gini", "collapse_index"]:
            img_path = charts[scenario][metric]
            img = Image(str(img_path), width=15*cm, height=8.4*cm)
            story.append(img)
            story.append(Spacer(1, 0.2*cm))

        story.append(PageBreak())

    # Hypothesis Tests (selected key ones)
    story.append(Paragraph("Hypothesis Tests (Selected)", h1_style))
    story.append(Paragraph("All p-values reported with Bonferroni correction across the full test battery.", body_style))
    story.append(Spacer(1, 0.3*cm))

    key_tests = [t for t in tests if t["hypothesis"] in {
        "TRUE_U > Blind_U", "TRUE_Fatal < Blind_Fatal", "TRUE_U > TTB_U", "TRUE_Fatal < TTB_Fatal",
        "TRUE_U > MOO_U", "TRUE_Fatal < MOO_Fatal",
        "TRUE_Collapse < TTB_Collapse", "TRUE_Collapse < MOO_Collapse",
        "TRUE_A9 < Blind_A9",
        "MOO_U > TTB_U", "MOO_Fatal < TTB_Fatal",
    }]
    test_header = ["Scenario", "Hypothesis", "Mean Diff", "t", "p_t(Bonf)", "Cohen d"]
    test_rows = [test_header]
    for t in key_tests:
        test_rows.append([
            SCENARIO_LABELS.get(t["scenario"], t["scenario"]),
            t["hypothesis"],
            fmt_f(t["mean_diff"]),
            fmt_f(t["t"], 2),
            f"{float(t.get('p_t_bonf', 1.0)):.4f}",
            fmt_f(t["cohens_d"]),
        ])

    tt = Table(test_rows, colWidths=[3.5*cm, 4.5*cm, 2.0*cm, 1.4*cm, 2.0*cm, 1.4*cm], repeatRows=1)
    tt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTSIZE", (0, 0), (-1, 0), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 1), (-1, -1), 7.5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(tt)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("Interpretation & Limitations", h1_style))
    story.append(Paragraph("""
    <b>Task-flow pairing:</b> Within each run all groups see the same module sequence. Differences are therefore
    attributable to selection mechanisms, not task luck.<br/><br/>
    <b>Observation uniformity:</b> A8 surface-quality bonus is uniform across groups. The only A8 asymmetry in TTB
    is its scoring-function bonus (hard-coded trust-objective weight), which is a mechanism-level difference.
    MOO has no hard-coded A8 bonus; any A8 advantage emerges naturally from high surface-quality observations.<br/><br/>
    <b>MOO vs TTB:</b> The weighted Tchebycheff MOO baseline includes explicit diversity objective (selection
    concentration penalty) and per-candidate-pool normalization. It consistently outperforms TTB but still
    falls short of TRUE, confirming that the problem is "trust-as-objective" rather than the specific
    aggregation function.<br/><br/>
    <b>Ablation surprise:</b> TRUE-C and TRUE-N outperform full TRUE in cumulative utility under current parameters,
    suggesting that constraint filtering and newcomer protection may be overly conservative. However, TRUE-N shows
    dramatically higher A9 cold-start delay, confirming that newcomer protection serves its intended purpose.<br/><br/>
    <b>Bonferroni correction:</b> Conservative; hypotheses remaining significant after correction are robust.
    """, body_style))

    doc.build(story)
    print(f"PDF written to {out}")


def main():
    print("Loading data...")
    summary = load_summary(DATA_DIR / "TRUE_p01_summary.csv")
    tests = load_tests(DATA_DIR / "TRUE_p01_tests.csv")
    print("Loading timeseries (this may take a moment)...")
    ts = load_timeseries(DATA_DIR / "TRUE_p01_round_timeseries.csv")

    with tempfile.TemporaryDirectory() as tmpdir:
        print("Generating charts...")
        charts = make_all_charts(ts, Path(tmpdir))
        print("Building PDF...")
        build_pdf(summary, tests, charts, OUT_PATH)


if __name__ == "__main__":
    main()
