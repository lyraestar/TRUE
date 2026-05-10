#!/usr/bin/env python3
"""Hyperparameter tuning + cap-noise experiment for P02.

Usage:
    python3 scripts/tune_p02.py --mode tune   # parameter sweep
    python3 scripts/tune_p02.py --mode noise  # cap-noise sweep
"""

import subprocess
import csv
import json
from pathlib import Path
from itertools import product

SRC = Path(__file__).parent.parent / "src" / "true_simulation.py"
OUTDIR = Path(__file__).parent.parent / "data" / "p02_results"
OUTDIR.mkdir(parents=True, exist_ok=True)


def patch_param(name: str, value: float):
    """Replace a global parameter in the source file."""
    with open(SRC, "r") as f:
        content = f.read()
    old = f"{name} = "
    # Find the current value line
    for line in content.split("\n"):
        if line.startswith(old):
            content = content.replace(line, f"{name} = {value}")
            break
    with open(SRC, "w") as f:
        f.write(content)


def run_experiment(groups: str, scenarios: str, runs: int = 20, seed: int = 20260510) -> list:
    """Run a quick experiment and return summary rows."""
    cmd = [
        "python3", str(SRC),
        "--runs", str(runs),
        "--rounds", "200",
        "--seed", str(seed),
        "--groups", groups,
        "--scenarios", scenarios,
        "--outdir", str(OUTDIR),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    summary_path = OUTDIR / "TRUE_p01_summary.csv"
    rows = []
    with open(summary_path, "r") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def tune_true_cap_weight():
    """Sweep TRUE's cap weight."""
    print("=" * 50)
    print("Tuning TRUE cap_weight (Baseline + Observation-Manipulated)")
    print("=" * 50)
    results = []
    for cw in [0.3, 0.5, 0.7, 0.9, 1.1]:
        patch_param("TRUE_CAP_WEIGHT", cw)
        rows = run_experiment("TRUE,Blind", "baseline,observation_manipulated", runs=20)
        for r in rows:
            if r["group"] == "TRUE":
                results.append({
                    "param": "cap_weight",
                    "value": cw,
                    "scenario": r["scenario"],
                    "utility": float(r["cumulative_utility_mean"]),
                    "fatal": float(r["fatal_errors_mean"]),
                })
                print(f"  cap_weight={cw:.1f} {r['scenario']} U={float(r['cumulative_utility_mean']):.1f} Fatal={float(r['fatal_errors_mean']):.1f}")
    # Restore default
    patch_param("TRUE_CAP_WEIGHT", 0.55)
    return results


def tune_ttb_trust_weight():
    """Sweep TTB's trust weight."""
    print("=" * 50)
    print("Tuning TTB trust_weight (Baseline + Observation-Manipulated)")
    print("=" * 50)
    results = []
    for tw in [0.4, 0.6, 0.8, 1.0, 1.2]:
        patch_param("TTB_TRUST_WEIGHT", tw)
        patch_param("TTB_UTIL_WEIGHT", round(1.0 - tw, 2))
        rows = run_experiment("TTB-cap,Blind", "baseline,observation_manipulated", runs=20)
        for r in rows:
            if r["group"] == "TTB-cap":
                results.append({
                    "param": "trust_weight",
                    "value": tw,
                    "scenario": r["scenario"],
                    "utility": float(r["cumulative_utility_mean"]),
                    "fatal": float(r["fatal_errors_mean"]),
                })
                print(f"  trust_weight={tw:.1f} {r['scenario']} U={float(r['cumulative_utility_mean']):.1f} Fatal={float(r['fatal_errors_mean']):.1f}")
    # Restore defaults
    patch_param("TTB_TRUST_WEIGHT", 0.70)
    patch_param("TTB_UTIL_WEIGHT", 0.22)
    return results


def sweep_cap_noise():
    """Sweep cap noise level."""
    print("=" * 50)
    print("Sweeping cap_noise (all scenarios)")
    print("=" * 50)
    results = []
    for noise in [0.0, 0.05, 0.10, 0.15, 0.20]:
        # Patch cap_noise into all scenarios
        with open(SRC, "r") as f:
            content = f.read()
        # Simple replacement: change cap_noise=0.0 in Scenario definitions
        # This is fragile but works for current structure
        for scenario_name in ["baseline", "safety_critical", "observation_manipulated", "utility_trust_misalignment"]:
            old = f'cap_noise=0.0,\n        {scenario_name}'
            new = f'cap_noise={noise},\n        {scenario_name}'
            content = content.replace(old, new)
            # Also handle misalignment scenario
            old2 = f'cap_noise=0.0,\n        misalignment_rounds'
            new2 = f'cap_noise={noise},\n        misalignment_rounds'
            content = content.replace(old2, new2)
        with open(SRC, "w") as f:
            f.write(content)

        rows = run_experiment("TRUE,TTB-cap,MOO-cap,Blind", "baseline,safety_critical,observation_manipulated,utility_trust_misalignment", runs=100)
        for r in rows:
            if r["group"] != "Blind":
                results.append({
                    "cap_noise": noise,
                    "scenario": r["scenario"],
                    "group": r["group"],
                    "utility": float(r["cumulative_utility_mean"]),
                    "fatal": float(r["fatal_errors_mean"]),
                })
        print(f"  cap_noise={noise:.2f} done")

    # Restore
    with open(SRC, "r") as f:
        content = f.read()
    for noise in [0.05, 0.10, 0.15, 0.20]:
        content = content.replace(f'cap_noise={noise},', 'cap_noise=0.0,')
    with open(SRC, "w") as f:
        f.write(content)

    return results


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["tune", "noise", "all"], default="all")
    args = parser.parse_args()

    if args.mode in ("tune", "all"):
        tune_results = []
        tune_results.extend(tune_true_cap_weight())
        tune_results.extend(tune_ttb_trust_weight())
        with open(OUTDIR / "p02_tune_results.json", "w") as f:
            json.dump(tune_results, f, indent=2)
        print(f"Tuning results written to {OUTDIR / 'p02_tune_results.json'}")

    if args.mode in ("noise", "all"):
        noise_results = sweep_cap_noise()
        with open(OUTDIR / "p02_noise_results.json", "w") as f:
            json.dump(noise_results, f, indent=2)
        print(f"Noise sweep results written to {OUTDIR / 'p02_noise_results.json'}")


if __name__ == "__main__":
    main()
