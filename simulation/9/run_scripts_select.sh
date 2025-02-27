#!/bin/bash


pgrep -f 'simulation_' | xargs kill
printf "\n"
printf "\n"
printf "\n"
printf "\n"
# python simulation_1200.py
# python simulation_1200_07.py
python simulation_2400_ML.py
python simulation_2400_ML_07.py


