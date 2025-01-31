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

flux_simulation_folder_ml_list = ['RAYPy_Simulation_2400_FLUX', 
                                    'RAYPy_Simulation_2400_07_FLUX']
rp_simulation_folder_ml_list   = ['RAYPy_Simulation_2400_RP', 
                                    'RAYPy_Simulation_2400_07_RP']



colors = ['red', 'green', 'blue', 'pink', 'lime', 'cyan' ]
linestyles = ['solid', 'dashed']
labels = ['0.8°','0.7°']
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
de = 38.9579-30.0000
table = 'Henke'
theta = 0.8
E = np.arange(500, 6001, de)
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C', rho=2.52,  kind='mirror',  table=table)
IrCrB4C = rm.Multilayer( tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)
IrCrB4C, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)



ax2=axs[0,0]
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.set_title(f'Mirror Coating Reflectivity at {theta}° ')
ax2.plot(E, IrCrB4C, label='IrCrB4C')
ax2.legend()

for ind2 in range(2):

    flux_simulation_folder = flux_simulation_folder_ml_list[ind2]
    rp_simulation_folder = rp_simulation_folder_ml_list[ind2]
    
    # loading the data
    oe = 'DetectorAtFocus' + '_RawRaysOutgoing.csv'
    flux = pd.read_csv(os.path.join(flux_simulation_folder, oe))
    rp = pd.read_csv(os.path.join(rp_simulation_folder, oe))
    exit_slit_list = flux['ExitSlit.totalHeight'].unique()[::-1]


    # AVAILABLE/ABS FLUX 
    ax = axs[1,0]
    ax2 = axs[1,1]
    for ind, es in enumerate(exit_slit_list):
        filtered_flux = flux[flux['ExitSlit.totalHeight'] == es]
        energy = filtered_flux['CPMU20.photonEnergy']
        perc_flux = filtered_flux['PercentageRaysSurvived']
        # perc_flux = ML_eff_new(energy, perc_flux)
        abs_flux = scale_undulator_flux(energy, perc_flux, undulator_spectra)
        ax.plot(energy,perc_flux,color=colors[ind+3*ind2], linestyle=linestyles[ind2], label=f'es {es} μm')
        ax2.plot(energy,abs_flux,color=colors[ind+3*ind2], linestyle=linestyles[ind2], label=f'es {es} μm')

    ax.set_xlabel(r'Energy [eV]')
    ax.set_ylabel('Transmission [%]')
    ax.set_title('Available Flux (in percent)')
    ax.grid(which='both', axis='both')
    if ind==0:
        ax.legend()
    # ax.set_yscale('log')
    ax2.set_title('Available Flux')
    ax2.set_xlabel(r'Energy [eV]')
    ax.grid(which='both', axis='both')
    ax2.set_ylabel('Flux [ph/s/tbw]')
    ax2.set_yscale('log')



    # BANDWIDTH
    ax = axs[2,0]
    for ind, es in enumerate(exit_slit_list):
        filtered_rp = rp[rp['ExitSlit.totalHeight'] == es]
        energy = filtered_rp['CPMU20.photonEnergy']
        bw = filtered_rp['Bandwidth']
        ax.plot(p.moving_average(energy,w),
                p.moving_average(bw,w),
                color=colors[ind+3*ind2], linestyle=linestyles[ind2],
                label=f'{labels[ind2]}, es {int(es*1000)} μm' )
    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Transmitted Bandwidth [eV]')
    ax.set_title('Transmitted bandwidth (tbw)')
    ax.grid(which='both', axis='both')

    if ind2==1:
        # Calculate the line as 6000 divided by the energy values
        energy_threshold = np.arange(energy.iloc[0], energy.iloc[-1])
        threshold_transmission = energy_threshold/6000
        ax.plot(energy_threshold, threshold_transmission, linestyle='dashed', color='black')
        ax.legend()

    # RESOLVING POWER
    ax = axs[2,1]
    for ind, es in enumerate(exit_slit_list):
        filtered_rp = rp[rp['ExitSlit.totalHeight'] == es]
        energy = filtered_rp['CPMU20.photonEnergy']
        bw = filtered_rp['Bandwidth']
        ax.plot(p.moving_average(energy,w),
                p.moving_average(energy/bw,w),
                color=colors[ind+3*ind2], linestyle=linestyles[ind2],
                label=f'{labels[ind2]}, es {int(es*1000)} μm' )

    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('RP [a.u.]')
    ax.set_title('Resolving Power')
    ax.grid(which='both', axis='both')
    if ind2==1:
        ax.axhline(y=6000, color='k', linestyle='--', label='RP 6000')
        # ax.legend()

    # HORIZONTAL FOCUS
    ax = axs[3,0]
    # Initialize an empty list to accumulate 'HorizontalFocusFWHM' data
    focx = []

    # Loop through each slit size in the 'SlitSize' list
    for ind, es in enumerate(exit_slit_list):
        # Filter the DataFrame for the current slit size
        filtered_rp = rp[rp['ExitSlit.totalHeight'] == es]
        
        energy = filtered_rp['CPMU20.photonEnergy']
        
        # Sum up 'HorizontalFocusFWHM' for each slit size
        focx.append(filtered_rp['HorizontalFocusFWHM'])

    # Convert 'focx_plot' to a numpy array for element-wise operations
    focx = np.array(focx)
    focx = np.mean(focx, axis=0)

    ax.plot(p.moving_average(energy,w),
            p.moving_average(focx*1000,w),
            color='black', linestyle=linestyles[ind2],
            label=f'es {es} μm' )

    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Focus Size [um]')
    ax.set_title('Horizontal focus')
    if ind ==0:
        ax.legend()

    # VERTICAL FOCUS
    ax = axs[3,1]
    for ind, es in enumerate(exit_slit_list):
        filtered_rp = rp[rp['ExitSlit.totalHeight'] == es]
        energy = filtered_rp['CPMU20.photonEnergy']
        focy = filtered_rp['VerticalFocusFWHM']
        ax.plot(p.moving_average(energy,w),
                p.moving_average(focy*1000,w),
                color=colors[ind+3*ind2], linestyle=linestyles[ind2],
                label=f'ExitSlit {es} μm' )

    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Focus Size [um]')
    ax.set_title('Vertical focus')

plt.suptitle('SoTeXs, 2400 l/mm blazed grating + ML')
plt.tight_layout()
plt.savefig('plot/SoTeXS-2400.png')
# plt.show()


# fig, (axs) = plt.subplots(2, 1,figsize=(10,10))


# # PERMIL BANDWIDTH
# ax = axs[0]
# for ind, es in enumerate(exit_slit_list):
#     filtered_rp = rp[rp['ExitSlit.totalHeight'] == es]
#     energy = filtered_rp['CPMU20.photonEnergy']
#     bw = filtered_rp['EnergyPerMilPerBw']
#     ax.plot(energy,bw, label=f'es {es} μm')

# ax.set_xlabel('Energy [keV]')
# ax.set_ylabel('Energy/1000/bandwidth [a.u.]')
# ax.set_title('PerMil Transmission')
# ax.grid(which='both', axis='both')
# ax.legend()

# # PERMIL FLUX 
# ax = axs[1]
# for ind, es in enumerate(exit_slit_list):
#     filtered_flux = flux[flux['ExitSlit.totalHeight'] == es]
#     energy = filtered_flux['CPMU20.photonEnergy']
#     permil = filtered_flux['FluxPerMilPerBwPerc']
#     ax.plot(energy,permil)

# ax.set_xlabel(r'Energy [eV]')
# ax.set_ylabel('Flux [ph/s/tbw]')
# ax.set_title('Transmission / Per MIl bandwidth')
# ax.grid(which='both', axis='both')

# plt.suptitle('SoTeXs, 2400 l/mm blazed grating + ML')
# plt.tight_layout()
# plt.savefig('plot/SoTeXS-2400-PerMil.png')


