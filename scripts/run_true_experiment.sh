#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
python3 ../src/true_simulation.py --runs 100 --rounds 200 --seed 20260510 --outdir ../data/final_results_v2
