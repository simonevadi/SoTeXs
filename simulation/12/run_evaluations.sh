#!/bin/bash

for py_file in $(find -maxdepth 1 -name '*eval*.py' | sort -f)
do
    printf $py_file 
    printf "\n"
    python $py_file

done
