import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# path to xrt:
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm
from helper_lib import get_reflectivity, scale_undulator_flux


# file/folder/ml index definition
from params import ml_sim_name_rp, ml_sim_name_flux
from params import undulator_spectra
from multilayer_helper import ML_eff_new

from raypyng.postprocessing import PostProcessAnalyzed
p = PostProcessAnalyzed()
w = 20

flux_simulation_folder07 = 'RAYPy_Simulation_2400_07' 
flux_simulation_folder08 = 'RAYPy_Simulation_2400_08' 

colors = ['red', 'blue', 'green']

# loading the data
oe = 'DetectorAtFocus' + '_RawRaysOutgoing.csv'
flux07 = pd.read_csv(os.path.join(flux_simulation_folder07, oe))
flux08 = pd.read_csv(os.path.join(flux_simulation_folder08, oe))
cff_list = flux07['PG.cFactor'].unique()
exit_slit_list = flux07['ExitSlit.openingHeight'].unique()
exit_slit_list = [0.02]
# plotting Flux and RP
fig, (axs) = plt.subplots(4, 2,figsize=(12,12))

# text
ax = axs[0,1]
ax.plot(undulator_spectra[:,0], undulator_spectra[:,3])

ax.set_title('CPMU20 Flux')
ax.grid(which='both', axis='both')
ax.set_ylabel('Flux [ph/s/0.1%bw]')
ax.set_xlabel('Energy [eV]')


# MIRROR COATING
ax2=axs[0,0]
de = 38.9579-30.0000
table = 'Henke'
E = np.arange(500, 5001, de)

theta = 0.7
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C', rho=2.52,  kind='mirror',  table=table)
IrCrB4C = rm.Multilayer( tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)
IrCrB4C, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)
ax2.plot(E, IrCrB4C, label='IrCrB4C')

theta = 0.8
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C', rho=2.52,  kind='mirror',  table=table)
IrCrB4C = rm.Multilayer( tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)
IrCrB4C, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)
ax2.plot(E, IrCrB4C, linestyle='dashed', label=f'IrCrB4C at {theta}°')



ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.set_title(f'Mirror Coating Reflectivity ')
ax2.legend()


# AVAILABLE/ABS FLUX 
ax = axs[1,0]
ax2 = axs[1,1]
for ind, es in enumerate(exit_slit_list):
    filtered_flux = flux07[flux07['ExitSlit.openingHeight'] == es]
    energy = filtered_flux['CPMU20.photonEnergy']
    perc_flux = filtered_flux['PercentageRaysSurvived']
    perc_flux = ML_eff_new(energy, perc_flux)
    abs_flux = scale_undulator_flux(energy, perc_flux, undulator_spectra)
    ax.plot(energy,perc_flux,color=colors[ind], label=f'es {es} μm, theta=0.7')
    ax2.plot(energy,abs_flux,color=colors[ind], label=f'es {es} μm, theta=0.7')

    filtered_flux = flux08[flux08['ExitSlit.openingHeight'] == es]
    energy = filtered_flux['CPMU20.photonEnergy']
    perc_flux = filtered_flux['PercentageRaysSurvived']
    perc_flux = ML_eff_new(energy, perc_flux)
    abs_flux = scale_undulator_flux(energy, perc_flux, undulator_spectra)
    ax.plot(energy,perc_flux,color=colors[ind], label=f'es {es} μm, theta=0.8°', linestyle='dashed')
    ax2.plot(energy,abs_flux,color=colors[ind], label=f'es {es} μm, theta=0.8°', linestyle='dashed')
             
ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Transmission [%]')
ax.set_title('Available Flux (in percent)')
ax.grid(which='both', axis='both')
ax.legend()
# ax.set_yscale('log')
ax2.set_title('Available Flux')
ax2.set_xlabel(r'Energy [eV]')
ax.grid(which='both', axis='both')
ax2.set_ylabel('Flux [ph/s/tbw]')
ax2.set_yscale('log')
ax2.set_ylim(10e9, 10e13)



# BANDWIDTH
ax = axs[2,0]
for ind, es in enumerate(exit_slit_list):
    filtered_rp = flux07[flux07['ExitSlit.openingHeight'] == es]
    energy = filtered_rp['CPMU20.photonEnergy']
    bw = filtered_rp['Bandwidth']
    ax.plot(p.moving_average(energy,w*5),p.moving_average(bw,w*5),color=colors[ind], label=f'es {es} μm' )

    filtered_rp = flux08[flux08['ExitSlit.openingHeight'] == es]
    energy = filtered_rp['CPMU20.photonEnergy']
    bw = filtered_rp['Bandwidth']
    ax.plot(p.moving_average(energy,w*5),p.moving_average(bw,w*5),color=colors[ind], label=f'es {es} μm', linestyle='dashed' )
    
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Transmitted Bandwidth [eV]')
ax.set_title('Transmitted bandwidth (tbw)')
ax.grid(which='both', axis='both')

# Calculate the line as 6000 divided by the energy values
energy_threshold = np.arange(energy.iloc[0], energy.iloc[-1])
threshold_transmission = energy_threshold/6000
ax.plot(energy_threshold, threshold_transmission, linestyle='dashed', color='black')
    
# ax.legend()


# RESOLVING POWER
ax = axs[2,1]
for ind, es in enumerate(exit_slit_list):
    filtered_rp = flux07[flux07['ExitSlit.openingHeight'] == es]
    energy = filtered_rp['CPMU20.photonEnergy']
    bw = filtered_rp['Bandwidth']
    ax.plot(p.moving_average(energy,w*5),p.moving_average(energy/bw,w*5), color=colors[ind], label=f'es {es} μm' )

    filtered_rp = flux08[flux08['ExitSlit.openingHeight'] == es]
    energy = filtered_rp['CPMU20.photonEnergy']
    bw = filtered_rp['Bandwidth']
    ax.plot(p.moving_average(energy,w*5),p.moving_average(energy/bw,w*5), color=colors[ind], linestyle='dashed', label=f'es {es} μm' )


ax.set_xlabel('Energy [eV]')
ax.set_ylabel('RP [a.u.]')
ax.set_title('Resolving Power')
ax.grid(which='both', axis='both')
ax.axhline(y=6000, color='k', linestyle='--', label='RP 6000')
# ax.legend()

# HORIZONTAL FOCUS
ax = axs[3,0]
# Initialize an empty list to accumulate 'HorizontalFocusFWHM' data
focx07 = []
focx08 = []

# Loop through each slit size in the 'SlitSize' list
for ind, es in enumerate(exit_slit_list):
    filtered_rp = flux07[flux07['ExitSlit.openingHeight'] == es]
    energy = filtered_rp['CPMU20.photonEnergy']
    focx07.append(filtered_rp['HorizontalFocusFWHM'])

    filtered_rp = flux08[flux08['ExitSlit.openingHeight'] == es]
    energy = filtered_rp['CPMU20.photonEnergy']
    focx08.append(filtered_rp['HorizontalFocusFWHM'])

# Convert 'focx_plot' to a numpy array for element-wise operations
focx07 = np.array(focx07)
focx07 = np.mean(focx07, axis=0)
focx08 = np.array(focx08)
focx08 = np.mean(focx08, axis=0)

ax.plot(p.moving_average(energy,w*1),p.moving_average(focx07*1000,w*1), label=f'theta=0.7°' )
ax.plot(p.moving_average(energy,w*1),p.moving_average(focx08*1000,w*1), linestyle='dashed',label=f'theta=0.8°' )

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Horizontal focus')
ax.legend()

# VERTICAL FOCUS
ax = axs[3,1]
for ind, es in enumerate(exit_slit_list):
    filtered_rp = flux07[flux07['ExitSlit.openingHeight'] == es]
    energy = filtered_rp['CPMU20.photonEnergy']
    focy = filtered_rp['VerticalFocusFWHM']
    ax.plot(p.moving_average(energy,w),p.moving_average(focy*1000,w), color=colors[ind], label=f'ExitSlit {es} μm' )

    filtered_rp = flux08[flux08['ExitSlit.openingHeight'] == es]
    energy = filtered_rp['CPMU20.photonEnergy']
    focy = filtered_rp['VerticalFocusFWHM']
    ax.plot(p.moving_average(energy,w),p.moving_average(focy*1000,w), color=colors[ind], linestyle='dashed', label=f'ExitSlit {es} μm' )

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Vertical focus')

plt.suptitle('SoTeXs, 2400 l/mm blazed grating + ML')
plt.tight_layout()
plt.savefig('plot/SoTeXS-2400.png')


fig, (axs) = plt.subplots(2, 1,figsize=(10,10))


# PERMIL BANDWIDTH
ax = axs[0]
for ind, es in enumerate(exit_slit_list):
    filtered_rp = flux07[flux07['ExitSlit.openingHeight'] == es]
    energy = filtered_rp['CPMU20.photonEnergy']
    bw = filtered_rp['EnergyPerMilPerBw']
    ax.plot(p.moving_average(energy,w),p.moving_average(bw,w),color=colors[ind], label=f'es {es} μm, theta=0.7°')

    filtered_rp = flux08[flux08['ExitSlit.openingHeight'] == es]
    energy = filtered_rp['CPMU20.photonEnergy']
    bw = filtered_rp['EnergyPerMilPerBw']
    ax.plot(p.moving_average(energy,w),p.moving_average(bw,w), linestyle='dashed', color=colors[ind], label=f'es {es} μm, theta=0.8°')

ax.set_xlabel('Energy [keV]')
ax.set_ylabel('Energy/1000/bandwidth [a.u.]')
ax.set_title('PerMil Transmission')
ax.grid(which='both', axis='both')
ax.legend()

# PERMIL FLUX 
ax = axs[1]
for ind, es in enumerate(exit_slit_list):
    filtered_flux = flux07[flux07['ExitSlit.openingHeight'] == es]
    energy = filtered_flux['CPMU20.photonEnergy']
    permil = filtered_flux['FluxPerMilPerBwPerc']
    ax.plot(p.moving_average(energy,w),p.moving_average(permil,w), color=colors[ind])

    filtered_flux = flux08[flux08['ExitSlit.openingHeight'] == es]
    energy = filtered_flux['CPMU20.photonEnergy']
    permil = filtered_flux['FluxPerMilPerBwPerc']
    ax.plot(p.moving_average(energy,w),p.moving_average(permil,w), linestyle='dashed', color=colors[ind])

ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Flux [ph/s/tbw]')
ax.set_title('Transmission / Per MIl bandwidth')
ax.grid(which='both', axis='both')

plt.suptitle('SoTeXs, 2400 l/mm blazed grating + ML')
plt.tight_layout()
plt.savefig('plot/SoTeXS-2400-PerMil.png')
plt.show()

