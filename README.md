# TRUE Simulation Project

Executable approximation of the TRUE (Trust–Reliability Unified Engineering) multi-agent collaboration simulation experiment.

## Structure

- `src/`: core simulation code
- `scripts/`: helper scripts for running experiments and generating reports
- `docs/`: experiment design documents and project notes
- `data/`: experiment outputs, grouped by run family
- `reports/`: curated report deliverables
- `assets/`: static assets such as fonts

## Main Entry Points

- `src/true_simulation.py` — current P0/P1 refactored experiment core
- `scripts/run_true_p01_experiment.sh` — run the latest experiment (100 runs × 200 rounds × 4 scenarios × 6 groups)
- `scripts/run_true_experiment.sh` — legacy pre-refactor runner
- `scripts/generate_true_report_pdf.py` — legacy PDF generator

## Current Experiment (P0/P1 Refactored)

The latest round addresses several rigor gaps identified in prior iterations:

1. **Fixed task-flow pairing**: all groups within a run see the identical task sequence.
2. **Removed group-specific observation manipulation**: A8 signals are no longer artificially elevated for any single group.
3. **MOO → TTB**: renamed to Trust-Targeted Baseline with an honest non-Pareto description.
4. **Ablation variants**: TRUE-C (no constraints), TRUE-E (no exploration bonus), TRUE-N (no newcomer protection).
5. **Statistical upgrades**: Wilcoxon signed-rank test, bootstrap 95% CIs, Bonferroni correction.
6. **Runs increased**: from 60 to 100.

### Quick Run

```bash
bash scripts/run_true_p01_experiment.sh
```

Or with custom parameters:

```bash
python3 src/true_simulation.py \
    --runs 100 --rounds 200 \
    --groups TRUE,TRUE-C,TRUE-E,TRUE-N,Blind,TTB \
    --outdir data/my_results
```

## Notes

- `data/p01_results/` is the current primary result set (P0/P1 refactor).
- `data/final_results_v2/` and `data/improved_results_v1/` are archived prior iterations.
- `reports/final/` contains polished report artifacts from earlier rounds.
