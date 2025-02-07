#!/bin/bash


pgrep -f 'simulation_' | xargs kill
printf "\n"
printf "\n"
printf "\n"
printf "\n"
# python simulation_1200_Flux.py
# python simulation_1200_RP.py
python simulation_2400_ML_Flux.py
python simulation_2400_ML_RP.py


