#!/bin/bash

sudo -v            # Ask for sudo password upfront



python simulation_1200_07.py
git add .
git commit -m "simulation_1200"
git push origin main


python simulation_2400_ML_07.py
git add .
git commit -m "simulation_2400"
git push origin main

python simulation_1200_slopes_smart.py
git add .
git commit -m "simulation_1200_slopes"
git push origin main
# sudo reboot        # Reboot without asking for password again
