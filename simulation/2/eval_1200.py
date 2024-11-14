import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# from helper library
from helper_lib import scale_undulator_flux

# import simulation parameters
from params import SlitSize, grating_1200 as grating
from params import colors, beamline_name, undulator_spectra, undulator_file_path

# import coating
from mirror_coating import coating, energy_coating, coating_label

# file/folder/ml index definition
flux_simulation_folder = 'RAYPy_Simulation_FLUX_1200'
rp_simulation_folder = 'RAYPy_Simulation_RP_1200'

# define the varying variable
varying_var = SlitSize
varying_var_n = 'Exit Slit'
varying_var_unit = 'um'

# load simulation results
oe           = 'DetectorAtFocus'
source       = 'CPMU20'
flux         = pd.read_csv(os.path.join(flux_simulation_folder, f'{oe}_RawRaysOutgoing.csv'))
rp           = pd.read_csv(os.path.join(rp_simulation_folder, f'{oe}_RawRaysOutgoing.csv'))
source_flux  = flux.drop_duplicates(subset=f'{source}.photonEnergy')[[f'{source}.photonEnergy', 'SourcePhotonFlux']]
en_flux_path = os.path.join(flux_simulation_folder, f'input_param_{source}_photonEnergy.dat')
energy_flux  = np.loadtxt(en_flux_path)




########################################
# plotting Flux and RP

fig, (axs) = plt.subplots(4, 2,figsize=(10,10))
fig.suptitle(f"{beamline_name}, {grating} l/mm grating")

# Mirror Coating
ax2=axs[0,0]
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.set_title('Mirror Coating Reflectivity')
ax2.plot(energy_coating, coating, 'b', label=f'{coating_label}')
ax2.legend()

# UNDULATOR
ax = axs[0,1]
ax.plot(undulator_spectra[:,0], undulator_spectra[:,3])
ax.grid(which='both', axis='both')
ax.set_yscale('log')
ax.set_ylabel('Flux [Ph/s/0.1%bw]')
ax.set_xlabel('Harmonic energy [eV]')
ax.set_title('CPMU20 Flux')


# BEAMLINE TRANSMISSION, IN PERCENT
ax = axs[1,0]
for ind, es_size in enumerate(varying_var):
    filtered_flux = flux[flux['ExitSlit.totalHeight'] == es_size]
    energy = filtered_flux['CPMU20.photonEnergy']
    perc_flux = filtered_flux['PercentageRaysSurvived']
    ax.plot(energy,perc_flux,colors[ind], label=f'{varying_var_n} {int(es_size*1000)} {varying_var_unit}' )
ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Transmission [%]')
ax.set_title('Available Flux [in percentage]')
ax.grid(which='both', axis='both')

# BEAMLINE TRANSMISSION, ABSOLUTE
ax = axs[1,1]
for ind, es_size in enumerate(varying_var):
    filtered_flux = flux[flux['ExitSlit.totalHeight'] == es_size]
    energy = filtered_flux['CPMU20.photonEnergy']
    perc_flux = filtered_flux['PercentageRaysSurvived']
    flux_abs  = scale_undulator_flux(energy, perc_flux, undulator_file_path)
    ax.plot(energy,flux_abs, colors[ind], label=f'{varying_var_n} {int(es_size*1000)} {varying_var_unit}'  )

ax.set_xlabel(f'Energy [eV]')
ax.set_ylabel('Transmission [Ph/s/...]')
ax.set_title('Available Flux [in transmitted bandwidth]')
ax.grid(which='both', axis='both')
ax.set_yscale('log')
ax.legend()


# BANDWIDTH
ax = axs[2,0]
for ind, es_size in enumerate(varying_var):
    filtered_rp = rp[rp['ExitSlit.totalHeight'] == es_size]
    energy = filtered_rp['CPMU20.photonEnergy']
    bw = filtered_rp['Bandwidth']    
    ax.plot(energy,bw*1000,colors[ind])


ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Transmitted Bandwidth [meV]')
ax.set_title('Transmitted Bandwidth (tbw)')
ax.grid(which='both', axis='both')


# RESOLVING POWER
ax = axs[2,1]

# plot and deal with bandwidth=0 case.
for ind, es_size in enumerate(varying_var):
    filtered_rp = rp[rp['ExitSlit.totalHeight'] == es_size]
    energy = filtered_rp['CPMU20.photonEnergy']
    bw = filtered_rp['Bandwidth']  
    try:
        res_p = energy / bw
    except ZeroDivisionError:
        res_p = 0
    inf_indices = np.where(np.isinf(bw))[0]
    if len(inf_indices)>0:
        print(f"For {varying_var_n} size {es_size}, you have zero bandwidth starting at E={energy[inf_indices[0]]} eV.")
    ax.plot(energy, res_p, colors[ind], label=f'{varying_var_n} {es_size} {varying_var_unit}')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('RP [a.u.]')
ax.set_title('Resolving Power')
ax.grid(which='both', axis='both')
ax.legend()

# HORIZONTAL FOCUS
ax = axs[3,0]
for ind, es_size in enumerate(varying_var):
    filtered_rp = rp[rp['ExitSlit.totalHeight'] == es_size]
    energy = filtered_rp['CPMU20.photonEnergy']
    foc = filtered_rp['HorizontalFocusFWHM']  
    ax.plot(energy,foc*1000,colors[ind],label=f'{varying_var_n} {es_size} {varying_var_unit}')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Horizontal Focus')
ax.legend()

# # VERTICAL FOCUS
ax = axs[3,1]
for ind, es_size in enumerate(varying_var):
    filtered_rp = rp[rp['ExitSlit.totalHeight'] == es_size]
    energy = filtered_rp['CPMU20.photonEnergy']
    foc = filtered_rp['VerticalFocusFWHM']  
    ax.plot(energy,foc*1000,colors[ind],label=f'{varying_var_n} {es_size} {varying_var_unit}')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Vertical Focus')

plt.tight_layout()
plt.savefig(f'plot/{beamline_name}_{grating}.png')

# plt.show()