#!/bin/bash

# set -euo pipefail

# # Force a sudo prompt now, fail if canceled
# sudo -k
# sudo -v

# # Keep sudo alive while this script runs
# # Refresh every 60 seconds so the timestamp never expires
# while true; do sudo -n -v; sleep 60; done 2>/dev/null &
# SUDO_KEEPALIVE_PID=$!

# # Clean up the background refresher on exit
# cleanup() { kill "$SUDO_KEEPALIVE_PID" 2>/dev/null || true; }
# trap cleanup EXIT



python simulation_1200_roughness_and_es_cff5.py
git add .
git commit -m "simulation_1200_roughness_and_es_cff5"
git push 

# python simulation_1200_slopes_and_es_cff5.py
# git add .
# git commit -m "simulation_1200_slopes_and_es_cff5"
# git push 

python simulation_1200_slopes_and_es_cff10.py
git add .
git commit -m "simulation_1200_slopes_and_es_cff10"
git push 

# python simulation_1200_slopes_and_es.py
# git add .
# git commit -m "simulation_1200_slopes_and_es"
# git push 

# echo "All tasks completed. Rebooting now..."
# sudo /sbin/reboot