import numpy as np

order       = 2
energy_flux = np.arange(500, 5001,500)
energy_rp   = np.arange(500, 5001,500)
SlitSize    = np.array([0.05,0.04,0.03,0.02,0.01])
nrays_flux  = 50000
nrays_rp    = 500000
index       = 'MLBG_mfm_second'
repeat_flux = 1
repeat_rp   = 10
ncpu_flux   = 10
ncpu_rp     = 10