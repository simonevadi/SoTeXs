import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

# path to xrt:
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm

# helper lib
from helper_lib import get_reflectivity
from helper_lib import scale_undulator_flux

# andrey ML
from multilayer_helper import ML_eff

# file/folder/ml index definition
from params import ml_order, ml_table, ml_index
from params import hb_1200_SlitSize, ml_SlitSize 
from params import hb_1200_cff
from params import hb_1200_sim_name_flux, ml_sim_name_flux
from params import hb_1200_sim_name_rp, ml_sim_name_rp

from params import beamline_name, undulator_spectra, undulator_file_path


flux_simulation_folder_1200 = 'RAYPy_Simulation_' + hb_1200_sim_name_flux
rp_simulation_folder_1200   = 'RAYPy_Simulation_' + hb_1200_sim_name_rp
flux_simulation_folder_ml = 'RAYPy_Simulation_' + ml_sim_name_flux
rp_simulation_folder_ml   = 'RAYPy_Simulation_' + ml_sim_name_rp

# loading the data
oe = 'DetectorAtFocus' + '_RawRaysOutgoing.csv'
# 1200 l/mm
flux1200 = pd.read_csv(os.path.join(flux_simulation_folder_1200, oe))
rp1200 = pd.read_csv(os.path.join(rp_simulation_folder_1200, oe))
source_flux1200 = flux1200.drop_duplicates(subset='CPMU20.photonEnergy')[['CPMU20.photonEnergy', 'SourcePhotonFlux']]
# ml 
fluxml = pd.read_csv(os.path.join(flux_simulation_folder_ml, oe))
rpml = pd.read_csv(os.path.join(rp_simulation_folder_ml, oe))
source_fluxml = fluxml.drop_duplicates(subset='CPMU20.photonEnergy')[['CPMU20.photonEnergy', 'SourcePhotonFlux']]

# Set global font sizes
suptitle_size = 18
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['font.size'] = 12  # Adjust font size globally
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

# plotting Flux and RP
fig, (axs) = plt.subplots(2, 2,figsize=(20,10))
log = False
# MIRROR COATING
ax=axs[0,0]

de = 38.9579-30.0000
table = 'Henke'
theta = 0.8
E = np.arange(50, 6001, de)
# triple coating
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C', rho=2.52,  kind='mirror',  table=table)
IrCrB4C = rm.Multilayer( tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)
IrCrB4C, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)


ax.plot(E, IrCrB4C, 'blue', label='IrCrB4C')
ax.plot(E, IrCrB4C**4, 'red', label='IrCrB4C, 4 mirrors')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Reflectivity [a.u.]')
ax.set_title(f'Mirror Coating Reflectivity at {theta}° ')
ax.legend()

# CPMU20

ax = axs[0,1]
ax.plot(undulator_spectra[:,0], undulator_spectra[:,3])

ax.set_title('CPMU20 Flux')
ax.grid(which='both', axis='both')

ax.set_ylabel('Flux [ph/s/0.1A/0.1%BW]')

# AVAILABLE FLUX ABSOLUTE
ax = axs[1,0]
energy_1200 = flux1200['CPMU20.photonEnergy']
perc_flux_1200 = flux1200['PercentageRaysSurvived']
abs_flux_1200 = scale_undulator_flux(energy_1200,
                                     perc_flux_1200,
                                     undulator_file_path)
energy_ml = fluxml['CPMU20.photonEnergy']
perc_flux_ml = fluxml['PercentageRaysSurvived']
abs_flux_ml = ML_eff(perc_flux_ml, 
                ind=ml_index, 
                energy=energy_ml,
                grating_eff_file=ml_table)
abs_flux_ml = scale_undulator_flux(energy_ml,
                                     abs_flux_ml,
                                     undulator_file_path)

ax.plot(energy_1200, abs_flux_1200, label=f'1200 l/mm' )
ax.plot(energy_ml, abs_flux_ml, label=f'2400 l/mm + ML' )
if log:
    ax.set_yscale('log')
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Flux [ph/s/0.1A/TBW]')
ax.grid(which='both', axis='both')
ax.set_title('Flux')
# ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
ax.legend(title='cff=2.25, ES=50μm')

# BANDWIDTH
ax = axs[1,1]
energy_1200 = rp1200['CPMU20.photonEnergy']
bw_1200 = rp1200['Bandwidth']
energy_ml = rpml['CPMU20.photonEnergy']
bw_ml = rpml['Bandwidth']

ax.plot(energy_1200,bw_1200)
ax.plot(energy_ml, bw_ml)
# Calculate the line as 6000 divided by the energy values
inv_energy_line = 6000 / energy_ml

# Plot this calculated line on the same axes
# ax.plot(energy_ml, inv_energy_line, label='6000/Energy', linestyle='--', color='red')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Transmitted Bandwidth [eV]')
ax.set_title('Transmitted Bandwidth (TBW)')
ax.grid(which='both', axis='both')



plt.suptitle('SoTeXs', fontsize=suptitle_size)
plt.tight_layout()
plt.savefig('plot/SoTeXs_kickoff.png')


