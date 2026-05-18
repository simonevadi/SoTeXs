#!/usr/bin/env bash
set -euo pipefail

SCRIPTS=(
  "simulation_nodef.py"
  "simulation_profile001.py"
  "simulation_profile002.py"
  "simulation_profile003.py"
  "simulation_profile004.py"
)

cd "$(dirname "$0")"

for script in "${SCRIPTS[@]}"; do
  echo "[START] ${script}"
  python "${script}"
  echo "[DONE]  ${script}"
  echo
  
done

echo "All simulations completed successfully."
