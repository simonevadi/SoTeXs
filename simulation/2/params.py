import numpy as np
import os 

rml_file_name = 'battery_FLUX_forML_IrCrB4C'
order         = 2
energy_flux   = np.arange(500, 5001,500)
energy_rp     = np.arange(500, 5001,500)
SlitSize      = np.array([0.05, 0.01])
grating_1200  = 1200
cff_1200      = 2.25
grating_2400  = 2400
nrays_flux    = 50000
nrays_rp      = 500000
ml_index      = 'MLBG_mfm_second'
repeat_flux   = 1
repeat_rp     = 1
ncpu_flux     = 10
ncpu_rp       = 10

# params only for evaluation
beamline_name = 'SoTeXS'
# define undulator file
undulator_file_path = os.path.join('undulator', 'CPMU20_B2l_k_dep_simp_all_harm_300mA.dbr')
# Undulator SPECTRA
undulator_spectra = np.loadtxt(undulator_file_path, skiprows=8)


### plotting colors
import matplotlib
import matplotlib.pyplot as plt
# Generate 20 colors from the 'hsv' colormap which resembles a rainbow
colors_rainbow = plt.cm.tab20(np.linspace(0, 2, int(max(1,2))))
# Convert the colors to hex format for easy usage
colors = [matplotlib.colors.rgb2hex(color) for color in colors_rainbow]
colors = ["Red", "Orange", "Green", "Blue", "Indigo", "Violet"]