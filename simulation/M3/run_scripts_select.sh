#!/bin/bash

python simulation_PGM.py
git add .
git commit -m 'sim STXM PGM'
git push

python simulation_PGM_noM1.py
git add .
git commit -m 'sim STXM PGM_noM1'
git push

# python simulation_VLS.py
# git add .
# git commit -m 'sim STXM VLS'
# git push
