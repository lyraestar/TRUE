#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

OUTDIR="data/p01_results"
mkdir -p "$OUTDIR"

echo "Running TRUE P0/P1 experiment: 100 runs x 200 rounds x 4 scenarios x 6 groups"
python3 src/true_simulation.py \
    --runs 100 \
    --rounds 200 \
    --outdir "$OUTDIR" \
    --groups TRUE,TRUE-C,TRUE-E,TRUE-N,Blind,TTB \
    2>&1 | tee "$OUTDIR/run.log"

echo "Done. Outputs in $OUTDIR"
