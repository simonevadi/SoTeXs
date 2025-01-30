#!/bin/bash

for py_file in $(find -maxdepth 1 -name '*simulation*.py' | sort -f)
do
    pgrep -f 'simulation_' | xargs kill
    printf "\n"
    printf "\n"
    printf "\n"
    printf "\n"
    printf $py_file 
    python $py_file
    python $py_file
    python $py_file
    find . -type d -name "round_*" -exec rm -r {} +


done