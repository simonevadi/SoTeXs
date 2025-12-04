#!/bin/bash

for py_file in $(find -maxdepth 1 -name '*eval*.py' | sort -f)
do
    printf "\n\n\n\n\n"
    printf $py_file 
    python $py_file

done
