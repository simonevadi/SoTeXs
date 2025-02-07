#!/bin/bash

for py_file in $(find -maxdepth 1 -name '*simulation*.py' | sort -f)
do
    pgrep -f 'simulation_' | xargs kill

    python $py_file


done