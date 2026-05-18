#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "[START] simulation_2400_all.py"
python simulation_2400_all.py
python eval_2400_fwhm_bandwidth_vs_energy.py
echo "[DONE]  simulation_2400_all.py"

echo "[START] simulation_1200_all.py"
python simulation_1200_all.py
python eval_1200_fwhm_bandwidth_vs_energy.py
echo "[DONE]  simulation_1200_all.py"

echo "All simulation batches completed successfully."
