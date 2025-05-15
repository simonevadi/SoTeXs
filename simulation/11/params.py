import numpy as np
import os
import pandas as pd

rounds_1200 = 2
rounds_ml = 1
ncpu    = 30
nrays  = 5e5

#   PARAMS FOR 1200l/mm GRATING SIMULATIONS
hb_1200_order       = 1
hb_1200_energy      = np.arange(500, 2550.1,0.2)
hb_1200_SlitSize    = np.array([0.03])
hb_1200_cff         = np.array([2.25])


#   PARAMS FOR ML 2400l/mm GRATING SIMULATIONS
ml_order        = 2
ml_SlitSize     = np.array([0.03])
ml_grating      = np.array([2400])
ml_nrays   = nrays

# ml_rml_file_path   = os.path.join('rml/'+ml_rml_file_name+'.rml')

grating = pd.read_csv('ML_eff/ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLbGR.dat',
                      sep='\s+')
mirror = pd.read_csv('ML_eff/ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLPM-max.dat',
                      sep='\s+')

ml_cff = grating['Cff'].to_numpy().flatten()#[::10]
ml_energy = grating['Energy'].to_numpy().flatten()#[::10]

# Extract efficiency from Andrey's data 
common_energy = None

if grating['Energy'].equals(mirror['Energy']):
    # If energy columns match, directly multiply
    efficiency = pd.DataFrame({
        'Energy[eV]': grating['Energy'],
        'Efficiency': grating['Efficiency(GR)'] * mirror['Efficiency(PM)']
    })
else:
    # Interpolate to a common energy range
    min_energy = max(grating['Energy'].min(), mirror['Energy'].min())
    max_energy = min(grating['Energy'].max(), mirror['Energy'].max())
    common_energy = np.linspace(min_energy, max_energy, num=1000)  # Define a common range

    grating_eff = np.interp(common_energy, grating['Energy'], grating['Efficiency(GR)'])
    mirror_eff = np.interp(common_energy, mirror['Energy'], mirror['Efficiency(PM)'])

    # Create a new DataFrame with interpolated values
    efficiency = pd.DataFrame({
        'Energy[eV]': common_energy,
        'Efficiency': grating_eff * mirror_eff
    })
# params only for evaluation
beamline_name = 'SoTeXS'
# define undulator file
undulator_file_path = os.path.join('undulator', 'CPMU20_B2l_k_dep_simp_all_harm_300mA.dbr')
# Undulator SPECTRA
undulator_spectra = np.loadtxt(undulator_file_path, skiprows=8)
