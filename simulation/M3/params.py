import numpy as np
import os
import pandas as pd
from pathlib import Path
rounds = 10
ncpu        = 30
nrays       = 5e5
m3_radius = np.arange(220, 240, .1)

energy = 1000

sotexs_1200_sim_name = 'sotexs_1200_Pt_M3'
sotexs_1200_file_name  = 'sotexs_1200_Pt'
sotexs_1200_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     sotexs_1200_file_name+'.rml')


# params only for evaluation
beamline_name = 'SoTeXS'
# define undulator file
undulator_file_path = os.path.join('undulator', 'CPMU20_B2l_k_dep_simp_all_harm_300mA.dbr')
# Undulator SPECTRA
undulator_spectra = np.loadtxt(undulator_file_path, skiprows=8)
