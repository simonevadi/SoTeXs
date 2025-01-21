import numpy as np
import os
import pandas as pd

rounds_1200 = 5
rounds_ml = 1
cpu    = 30
nrays  = 5e5

#   PARAMS FOR 1200l/mm GRATING SIMULATIONS
hb_1200_order       = 1
hb_1200_energy_flux = np.arange(50, 2551,10)
hb_1200_energy_rp   = np.arange(50, 2551,10)
hb_1200_SlitSize    = np.array([0.05])
hb_1200_grating     = np.array([1200])
hb_1200_blaze       = np.array([0.9])
hb_1200_cff         = np.array([2.25])
hb_1200_nrays_flux  = nrays
hb_1200_nrays_rp    = nrays 
hb_1200_rounds_flux = rounds_1200
hb_1200_rounds_rp   = rounds_1200
hb_1200_ncpu_flux   = cpu
hb_1200_ncpu_rp     = cpu

hb_1200_sim_name_flux = '1200_FLUX_m1_in'
hb_1200_sim_name_rp   = '1200_RP_m1_in'
hb_1200_rml_file_name = 'sotexs_1200_m1_in'

this_file_dir   = os.path.dirname(os.path.realpath(__file__))
hb_1200_file_path   = os.path.join('rml/'+hb_1200_rml_file_name+'.rml')


#   PARAMS FOR ML 2400l/mm GRATING SIMULATIONS
ml_order        = 2
ml_index        = 'MLBG_mfm_second'
ml_table        = os.path.join('ML_eff', 'grating_eff_5000.xlsx')
ml_energy_flux  = np.arange(500, 5001,500)
ml_energy_rp    = np.arange(500, 5001,500)
ml_SlitSize     = np.array([0.05])
ml_grating      = np.array([2400])
ml_nrays_flux   = nrays
ml_nrays_rp     = nrays 
ml_rounds_flux  = rounds_ml
ml_rounds_rp    = rounds_ml
ml_ncpu_flux    = cpu
ml_ncpu_rp      = cpu

ml_sim_name_rp     = '2400_RP_m1_in'
ml_sim_name_flux   = '2400_FLUX_m1_in'
ml_rml_file_name   = 'sotexs_2400_m1_in'

grating_file_path = os.path.join('ML_eff',
        'ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLbGR.dat')
grating_df = pd.read_csv(grating_file_path, delim_whitespace=True, header=[0, 1])

beta_file_path = os.path.join('ML_eff',
        'ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLPM-max.dat')
beta_df = pd.read_csv(beta_file_path, delim_whitespace=True, header=[0, 1])


ml_cff = grating_df['Cff'].to_numpy().flatten()
ml_energy_rp = grating_df['Energy'].to_numpy().flatten()
ml_energy_flux = grating_df['Energy'].to_numpy().flatten()


this_file_dir      = os.path.dirname(os.path.realpath(__file__))
ml_rml_file_path   = os.path.join('rml/'+ml_rml_file_name+'.rml')


# params only for evaluation
beamline_name = 'SoTeXS'
# define undulator file
undulator_file_path = os.path.join('undulator', 'CPMU20_B2l_k_dep_simp_all_harm_300mA.dbr')
# Undulator SPECTRA
undulator_spectra = np.loadtxt(undulator_file_path, skiprows=8)
