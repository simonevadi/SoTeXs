import numpy as np
import os
import pandas as pd
from pathlib import Path
rounds = 1
ncpu        = 30
nrays       = 5e4
m3_radius = np.arange(225, 240, .1)

energy = [500, 2000]

# define undulator file
undulator_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'undulator',
                                     'CPMU20.csv')
# Undulator SPECTRA
undulator_spectra = pd.read_csv(undulator_file_path)


sotexs_1200_sim_name = 'sotexs_1200_Pt_M3'
sotexs_1200_file_name  = 'sotexs_1200_Pt_m3'
sotexs_1200_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     sotexs_1200_file_name+'.rml')

# varying CFF
exit_slit_height = 0.01  # in mm
rounds_cff = 20
sotexs_1200_cff_sim_name = 'sotexs_1200_Pt_cff'
energy_cff = np.arange(500, 2001, 500)
cff = [1.6,2.25,5,10]
m3_radius_cff = [225,232,240, 245]
m3_radius_cff = np.arange(230, 234, 0.5)
# params only for evaluation
beamline_name = 'SoTeXS'

