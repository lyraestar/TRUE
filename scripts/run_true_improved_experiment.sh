#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
python3 ../src/true_simulation.py \
  --runs 60 \
  --rounds 200 \
  --seed 20260510 \
  --outdir ../data/improved_results_v1
