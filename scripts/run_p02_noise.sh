#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# Helper: patch cap_noise in all scenarios
patch_noise() {
    local noise=$1
    sed -i "s/cap_noise=0\.0,/cap_noise=${noise},/g" src/true_simulation.py
}

# Helper: restore cap_noise to 0.0
restore_noise() {
    sed -i 's/cap_noise=[0-9.]*,/cap_noise=0.0,/g' src/true_simulation.py
}

mkdir -p data/p02_results

echo "Running cap-noise sweep: TRUE, TTB-cap, MOO-cap, Blind"

for noise in 0.00 0.05 0.10 0.15 0.20; do
    echo ""
    echo "=== cap_noise = $noise ==="
    restore_noise
    patch_noise "$noise"
    python3 -m py_compile src/true_simulation.py
    
    python3 src/true_simulation.py \
        --runs 100 --rounds 200 \
        --groups TRUE,TTB-cap,MOO-cap,Blind \
        --outdir "data/p02_results/noise_${noise}"
    
    # Archive results
    cp "data/p02_results/noise_${noise}/TRUE_p01_summary.csv" "data/p02_results/summary_noise_${noise}.csv"
    cp "data/p02_results/noise_${noise}/TRUE_p01_experiment_report.md" "data/p02_results/report_noise_${noise}.md" 2>/dev/null || true
done

restore_noise
python3 -m py_compile src/true_simulation.py

echo ""
echo "All noise experiments done. Results in data/p02_results/"
