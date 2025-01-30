#!/bin/bash


pgrep -f 'simulation_' | xargs kill
printf "\n"
printf "\n"
printf "\n"
printf "\n"
printf $py_file 
python simulation_1200_RP.py
python simulation_1200_RP.py
# find . -type d -name "round_*" -exec rm -r {} +

python simulation_1200_Flux.py
python simulation_1200_Flux.py
# find . -type d -name "round_*" -exec rm -r {} +


