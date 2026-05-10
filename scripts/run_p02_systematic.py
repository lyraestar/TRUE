#!/usr/bin/env python3
"""Systematic B+C experiment for P02.

Phase 1: Hyperparameter tuning for TRUE, TTB-cap, MOO-cap (100 runs, Baseline only).
Phase 2: Full scenario comparison with tuned params under cap_noise = 0.0, 0.10, 0.20.
"""

import csv
import json
import subprocess
from pathlib import Path
from itertools import product

SRC = Path(__file__).parent.parent / "src" / "true_simulation.py"
P02_DIR = Path(__file__).parent.parent / "data" / "p02_results"
P02_DIR.mkdir(parents=True, exist_ok=True)


def read_src() -> str:
    with open(SRC, "r") as f:
        return f.read()


def write_src(content: str):
    with open(SRC, "w") as f:
        f.write(content)


def set_param(content: str, name: str, value) -> str:
    for line in content.split("\n"):
        if line.startswith(f"{name} = "):
            content = content.replace(line, f"{name} = {value}")
            break
    return content


def set_scenario_cap_noise(content: str, noise: float) -> str:
    import re
    # Replace all cap_noise=X.XX, patterns
    content = re.sub(r'cap_noise=[0-9.]+,', f'cap_noise={noise},', content)
    return content


def run(groups: str, scenarios: str, runs: int, outdir: Path, seed: int = 20260510) -> list:
    outdir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "python3", str(SRC),
        "--runs", str(runs), "--rounds", "200",
        "--seed", str(seed),
        "--groups", groups,
        "--scenarios", scenarios,
        "--outdir", str(outdir),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    rows = []
    with open(outdir / "TRUE_p01_summary.csv", "r") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def phase1_tune_true() -> list:
    print("\n" + "=" * 60)
    print("Phase 1-A: Tuning TRUE (Baseline, 100 runs)")
    print("=" * 60)
    base = read_src()
    results = []
    best_score = -1e9
    best_config = None

    for cw in [0.3, 0.5, 0.7, 0.9, 1.1]:
        for tw in [0.1, 0.3, 0.5]:
            for ec in [0.0, 0.15, 0.3, 0.5]:
                c = set_param(base, "TRUE_CAP_WEIGHT", cw)
                c = set_param(c, "TRUE_THETA_WEIGHT", tw)
                c = set_param(c, "TRUE_EXPLORATION_COEF", ec)
                write_src(c)
                subprocess.run(["python3", "-m", "py_compile", str(SRC)], check=True)

                rows = run("TRUE,Blind", "baseline", 100, P02_DIR / "tune_true")
                for r in rows:
                    if r["group"] == "TRUE":
                        u = float(r["cumulative_utility_mean"])
                        results.append({"cw": cw, "tw": tw, "ec": ec, "utility": u})
                        if u > best_score:
                            best_score = u
                            best_config = (cw, tw, ec)
                        print(f"  cw={cw:.1f} tw={tw:.1f} ec={ec:.2f}  U={u:.1f}")

    write_src(base)
    print(f"  BEST TRUE config: cap_weight={best_config[0]}, theta_weight={best_config[1]}, exploration={best_config[2]}  U={best_score:.1f}")
    with open(P02_DIR / "p02_tune_true.json", "w") as f:
        json.dump({"results": results, "best": {"cw": best_config[0], "tw": best_config[1], "ec": best_config[2], "utility": best_score}}, f, indent=2)
    return results


def phase1_tune_ttb() -> list:
    print("\n" + "=" * 60)
    print("Phase 1-B: Tuning TTB-cap (Baseline, 100 runs)")
    print("=" * 60)
    base = read_src()
    results = []
    best_score = -1e9
    best_config = None

    for tw in [0.3, 0.5, 0.7, 0.9, 1.1]:
        for vp in [-0.1, -0.04, 0.0]:
            uw = round(1.0 - tw, 2)
            c = set_param(base, "TTB_TRUST_WEIGHT", tw)
            c = set_param(c, "TTB_UTIL_WEIGHT", uw)
            c = set_param(c, "TTB_VAR_PENALTY", vp)
            write_src(c)
            subprocess.run(["python3", "-m", "py_compile", str(SRC)], check=True)

            rows = run("TTB-cap,Blind", "baseline", 100, P02_DIR / "tune_ttb")
            for r in rows:
                if r["group"] == "TTB-cap":
                    u = float(r["cumulative_utility_mean"])
                    results.append({"tw": tw, "uw": uw, "vp": vp, "utility": u})
                    if u > best_score:
                        best_score = u
                        best_config = (tw, uw, vp)
                    print(f"  tw={tw:.1f} uw={uw:.2f} vp={vp:.2f}  U={u:.1f}")

    write_src(base)
    print(f"  BEST TTB config: trust_weight={best_config[0]}, util_weight={best_config[1]}, var_penalty={best_config[2]}  U={best_score:.1f}")
    with open(P02_DIR / "p02_tune_ttb.json", "w") as f:
        json.dump({"results": results, "best": {"tw": best_config[0], "uw": best_config[1], "vp": best_config[2], "utility": best_score}}, f, indent=2)
    return results


def phase1_tune_moo() -> list:
    print("\n" + "=" * 60)
    print("Phase 1-C: Tuning MOO-cap (Baseline, 100 runs)")
    print("=" * 60)
    base = read_src()
    results = []
    best_score = -1e9
    best_config = None

    for u in [0.1, 0.2, 0.3, 0.4]:
        t = round(0.55 - u, 2)
        weights = [u, t, 0.03, 0.18, 0.24]
        c = set_param(base, "MOO_WEIGHTS", weights)
        write_src(c)
        subprocess.run(["python3", "-m", "py_compile", str(SRC)], check=True)

        rows = run("MOO-cap,Blind", "baseline", 100, P02_DIR / "tune_moo")
        for r in rows:
            if r["group"] == "MOO-cap":
                score = float(r["cumulative_utility_mean"])
                results.append({"w": weights, "utility": score})
                if score > best_score:
                    best_score = score
                    best_config = weights
                print(f"  w={weights}  U={score:.1f}")

    write_src(base)
    print(f"  BEST MOO config: {best_config}  U={best_score:.1f}")
    with open(P02_DIR / "p02_tune_moo.json", "w") as f:
        json.dump({"results": results, "best": {"w": best_config, "utility": best_score}}, f, indent=2)
    return results


def phase2_noise_sweep(best_true: dict, best_ttb: dict, best_moo: dict):
    print("\n" + "=" * 60)
    print("Phase 2: Full scenario comparison with tuned params + cap noise")
    print("=" * 60)
    base = read_src()

    # Apply best configs
    c = set_param(base, "TRUE_CAP_WEIGHT", best_true["cw"])
    c = set_param(c, "TRUE_THETA_WEIGHT", best_true["tw"])
    c = set_param(c, "TRUE_EXPLORATION_COEF", best_true["ec"])
    c = set_param(c, "TTB_TRUST_WEIGHT", best_ttb["tw"])
    c = set_param(c, "TTB_UTIL_WEIGHT", best_ttb["uw"])
    c = set_param(c, "TTB_VAR_PENALTY", best_ttb["vp"])
    c = set_param(c, "MOO_WEIGHTS", best_moo["w"])

    results = []
    for noise in [0.0, 0.10, 0.20]:
        print(f"\n--- cap_noise = {noise:.2f} ---")
        c_noisy = set_scenario_cap_noise(c, noise)
        write_src(c_noisy)
        subprocess.run(["python3", "-m", "py_compile", str(SRC)], check=True)

        out = P02_DIR / f"noise_{noise:.2f}"
        rows = run("TRUE,TTB-cap,MOO-cap,Blind",
                   "baseline,safety_critical,observation_manipulated,utility_trust_misalignment",
                   100, out)
        for r in rows:
            if r["group"] != "Blind":
                results.append({
                    "cap_noise": noise,
                    "scenario": r["scenario"],
                    "group": r["group"],
                    "utility": float(r["cumulative_utility_mean"]),
                    "fatal": float(r["fatal_errors_mean"]),
                    "gini": float(r["final_trust_gini"]),
                    "collapse": float(r["final_collapse_index"]),
                })
                print(f"  {r['scenario']:25s} {r['group']:10s} U={float(r['cumulative_utility_mean']):8.1f} Fatal={float(r['fatal_errors_mean']):5.1f}")

    write_src(base)
    with open(P02_DIR / "p02_noise_sweep.json", "w") as f:
        json.dump(results, f, indent=2)
    return results


def main():
    base = read_src()
    # Ensure clean state
    base = set_scenario_cap_noise(base, 0.0)
    write_src(base)
    subprocess.run(["python3", "-m", "py_compile", str(SRC)], check=True)

    # Phase 1
    tune_true = phase1_tune_true()
    tune_ttb = phase1_tune_ttb()
    tune_moo = phase1_tune_moo()

    best_true = json.load(open(P02_DIR / "p02_tune_true.json"))["best"]
    best_ttb = json.load(open(P02_DIR / "p02_tune_ttb.json"))["best"]
    best_moo = json.load(open(P02_DIR / "p02_tune_moo.json"))["best"]

    # Phase 2
    phase2_noise_sweep(best_true, best_ttb, best_moo)

    print("\n" + "=" * 60)
    print("P02 systematic experiment complete.")
    print(f"Results in {P02_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
