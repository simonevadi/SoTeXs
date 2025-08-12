#!/bin/bash




# python simulation_1200_Pt.py
# git add .
# git commit -m "simulation_1200_Pt"
# git push origin main

python simulation_1200_triple_coating.py
git add .
git commit -m "simulation_1200_triple"
git push origin main

python simulation_2400.py
git add .
git commit -m "simulation_2400"
git push origin main

python simulation_1200_slopes_smart.py
git add .
git commit -m "simulation_1200_slopes"
git push origin main
# sudo reboot        # Reboot without asking for password again
