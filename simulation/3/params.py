import numpy as np
import os

rounds =100
cpu    = 30
nrays  = 1e4

#   PARAMS FOR 1200l/mm GRATING SIMULATIONS
hb_1200_order       = 1
hb_1200_energy_flux = np.arange(50, 2551,10)
hb_1200_energy_rp   = np.arange(50, 2551,10)
hb_1200_SlitSize    = np.array([0.1])
hb_1200_grating     = np.array([1200])
hb_1200_blaze       = np.array([0.9])
hb_1200_cff         = np.array([2.25])
hb_1200_nrays_flux  = nrays
hb_1200_nrays_rp    = nrays 
hb_1200_rounds_flux = rounds
hb_1200_rounds_rp   = rounds
hb_1200_ncpu_flux   = cpu
hb_1200_ncpu_rp     = cpu

hb_1200_sim_name_flux = '1200_FLUX'
hb_1200_sim_name_rp   = '1200_RP'
hb_1200_rml_file_name = 'sotexs_1200'

this_file_dir   = os.path.dirname(os.path.realpath(__file__))
hb_1200_file_path   = os.path.join('rml/'+hb_1200_rml_file_name+'.rml')


#   PARAMS FOR ML 2400l/mm GRATING SIMULATIONS
ml_order        = 2
ml_index        = 'MLBG_mfm_second'
ml_table        = os.path.join('ML_eff', 'grating_eff_5000.xlsx')
ml_energy_flux  = np.arange(500, 5001,500)
ml_energy_rp    = np.arange(500, 5001,500)
ml_SlitSize     = np.array([0.1])
ml_grating      = np.array([2400])
ml_nrays_flux   = nrays
ml_nrays_rp     = nrays 
ml_rounds_flux  = rounds
ml_rounds_rp    = rounds
ml_ncpu_flux    = cpu
ml_ncpu_rp      = cpu

ml_sim_name_rp     = '2400_RP'
ml_sim_name_flux   = '2400_FLUX'
ml_rml_file_name   = 'sotexs_2400'

this_file_dir      = os.path.dirname(os.path.realpath(__file__))
ml_rml_file_path   = os.path.join('rml/'+ml_rml_file_name+'.rml')