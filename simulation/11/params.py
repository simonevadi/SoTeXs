import numpy as np
import os
import pandas as pd

rounds_1200 = 2
rounds_ml = 20
cpu    = 30
nrays  = 5e5

#   PARAMS FOR 1200l/mm GRATING SIMULATIONS
hb_1200_order       = 1
hb_1200_energy_flux = np.arange(500, 2550.1,0.2)
hb_1200_SlitSize    = np.array([0.03])
hb_1200_cff         = np.array([2.25])
hb_1200_nrays_flux  = nrays
hb_1200_rounds_flux = rounds_1200
hb_1200_ncpu_flux   = cpu

hb_1200_sim_name_flux = '1200_07_FLUX'
hb_1200_rml_file_name = 'sotexs_1200_07'

this_file_dir   = os.path.dirname(os.path.realpath(__file__))
hb_1200_file_path   = os.path.join('rml/'+hb_1200_rml_file_name+'.rml')


#   PARAMS FOR ML 2400l/mm GRATING SIMULATIONS
ml_order        = 2
ml_index        = 'MLBG_mfm_second'
ml_table        = os.path.join('ML_eff', 'grating_eff_5000.xlsx')
ml_SlitSize     = np.array([0.03])
ml_grating      = np.array([2400])
ml_nrays_flux   = nrays
ml_rounds_flux  = 1
ml_ncpu_flux    = cpu

ml_sim_name_rp     = '2400_07_RP'
ml_sim_name_flux   = '2400_07_FLUX'
ml_rml_file_name   = 'sotexs_2400_07'

grating_file_path = os.path.join('ML_eff',
        'ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLbGR.dat')
grating_df = pd.read_csv(grating_file_path, sep='\s+', header=[0, 1])

beta_file_path = os.path.join('ML_eff',
        'ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLPM-max.dat')
beta_df = pd.read_csv(beta_file_path, sep='\s+', header=[0, 1])


ml_cff = grating_df['Cff'].to_numpy().flatten()[::10]
ml_energy_rp = grating_df['Energy'].to_numpy().flatten()[::10]
ml_energy_flux = grating_df['Energy'].to_numpy().flatten()[::10]


this_file_dir      = os.path.dirname(os.path.realpath(__file__))
ml_rml_file_path   = os.path.join('rml/'+ml_rml_file_name+'.rml')

grating = pd.read_csv('ML_eff/ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLbGR.dat',
                      sep='\s+')
mirror = pd.read_csv('ML_eff/ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLPM-max.dat',
                      sep='\s+')

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
