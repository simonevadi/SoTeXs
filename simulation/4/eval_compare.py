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
fig, (axs) = plt.subplots(3, 2,figsize=(10,10))
log = False
# MIRROR COATING
ax=axs[0,0]

de = 38.9579-30.0000
table = 'Henke'
theta = 0.8
E = np.arange(50, 5001, de)
# triple coating
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C', rho=2.52,  kind='mirror',  table=table)
IrCrB4C = rm.Multilayer( tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)
IrCrB4C, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)


ax.plot(E, IrCrB4C, 'blue', label='IrCrB4C')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Reflectivity [a.u.]')
ax.set_title(f'Mirror Coating Reflectivity at {theta}° ')
ax.legend()

# CPMU20

ax = axs[0,1]
ax.plot(undulator_spectra[:,0], undulator_spectra[:,3])

ax.set_title('CPMU20 Flux')
ax.grid(which='both', axis='both')

ax.set_ylabel('Flux [ph/s/0.1A/0.1%bw]')

# AVAILABLE FLUX IN PERCENTAGE
ax = axs[1,0]
energy1200 = flux1200['CPMU20.photonEnergy']
perc_flux_1200 = flux1200['PercentageRaysSurvived']

ax.plot(energy1200,perc_flux_1200, label=f'1200 l/mm' )

ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Transmission [%]')
ax.set_title('Available Flux (in transmitted bandwidth)')
ax.grid(which='both', axis='both')
if log:
    ax.set_yscale('log')

# Define a custom formatter function to display labels as floats with two decimal places
def custom_formatter(x, pos):
    return f"{x:.2}%"

# Apply the custom formatter to the y-axis
ax.yaxis.set_major_formatter(ticker.FuncFormatter(custom_formatter))

# AVAILABLE FLUX ABSOLUTE
ax = axs[1,1]
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
ax.plot(energy_ml, abs_flux_ml, label=f'ML' )
if log:
    ax.set_yscale('log')
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Flux [ph/s/0.1A/tbw]')
ax.grid(which='both', axis='both')
ax.set_title('Available Flux (absolute)')
# ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
ax.legend()

# BANDWIDTH
ax = axs[2,0]
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
ax.set_title('Transmitted bandwidth (tbw)')
ax.grid(which='both', axis='both')


# RESOLVING POWER
ax = axs[2,1]
energy_1200 = rp1200['CPMU20.photonEnergy']
bw_1200 = rp1200['Bandwidth']
energy_ml = rpml['CPMU20.photonEnergy']
bw_ml = rpml['Bandwidth']

ax.plot(energy_1200,energy_1200/bw_1200)
ax.plot(energy_ml,energy_ml/bw_ml)
ax.axhline(y=6000, color='r', linestyle='--', label='RP 6000')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('RP [a.u.]')
ax.set_title('Resolving Power')
ax.grid(which='both', axis='both')

plt.suptitle('SoTeXs', fontsize=suptitle_size)
plt.tight_layout()
plt.savefig('plot/SoTeXs.png')

# plotting Flux and RP
fig, (axs) = plt.subplots(2, 1,figsize=(10,10))

# HORIZONTAL FOCUS
ax = axs[0]
energy_1200 = rp1200['CPMU20.photonEnergy']
focx_1200 = rp1200['HorizontalFocusFWHM']
energy_ml = rpml['CPMU20.photonEnergy']
focx_ml = rpml['HorizontalFocusFWHM']

ax.plot(energy_1200,focx_1200*1000)
ax.plot(energy_ml,focx_ml*1000)

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Horizontal focus')

# VERTICAL FOCUS
ax = axs[1]
energy_1200 = rp1200['CPMU20.photonEnergy']
focy_1200 = rp1200['VerticalFocusFWHM']
energy_ml = rpml['CPMU20.photonEnergy']
focy_ml = rpml['VerticalFocusFWHM']

ax.plot(energy_1200,focy_1200*1000)
ax.plot(energy_ml,focy_ml*1000)

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Vertical focus')

plt.suptitle('SoTeXs Focus Size', fontsize=suptitle_size)
plt.tight_layout()
plt.savefig('plot/SoTeXs-Focus.png')
# plt.show()


fig, (axs) = plt.subplots(2, 1,figsize=(10,10))


# PERMIL BANDWIDTH
ax = axs[0]
energy_1200 = rp1200['CPMU20.photonEnergy']
permil_bw_1200 = flux1200['EnergyPerMilPerBw']
permil_bw_ml = fluxml['EnergyPerMilPerBw']


ax.plot(energy_1200/1000,permil_bw_1200, label=f'1200 l/mm')
ax.plot(energy_ml/1000,permil_bw_ml, label=f'ML')

ax.set_xlabel('Energy [keV]')
ax.set_ylabel('Energy/1000/bandwidth [a.u.]')
ax.set_title('PerMil Transmission')
ax.grid(which='both', axis='both')
ax.legend()


# PERMIL FLUX 
ax = axs[1]
energy1200 = flux1200['CPMU20.photonEnergy']
permil_flux_1200 = flux1200['FluxPerMilPerBwPerc']
permil_flux_ml = fluxml['FluxPerMilPerBwPerc']

ax.plot(energy_1200,permil_flux_1200)
ax.plot(energy_ml,permil_flux_ml)

ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Flux [ph/s/0.1A/tbw]')
ax.set_title('Transmission / Per Mil bandwidth')
ax.grid(which='both', axis='both')
# ax.set_yscale('log')

plt.suptitle('SoTeXs PerMil', fontsize=suptitle_size)
plt.tight_layout()
plt.savefig('plot/SoTeXs-PerMil.png')


