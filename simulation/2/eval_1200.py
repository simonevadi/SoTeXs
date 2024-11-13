import numpy as np
# import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

# path to xrt:
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm

# raypyng 
from raypyng.postprocessing import PostProcessAnalyzed

# from helper library
from helper_lib import get_reflectivity
from helper_lib import scale_undulator_flux, order

# import simulation parameters
from params import energy_rp, energy_flux, SlitSize, grating_1200 as grating
from params import colors

# define undulator file
undulator_file = os.path.join('undulator', 'CPMU20_B2l_k_dep_simp_all_harm_300mA.dbr')


# file/folder/ml index definition
flux_simulation_folder = 'RAYPy_Simulation_FLUX_1200'
rp_simulation_folder = 'RAYPy_Simulation_RP_1200'

title = 'SoTeXS'


varying_var = SlitSize
varying_var_n = 'Exit Slit'
varying_var_unit = 'um'

# load the results

oe = 'DetectorAtFocus' + '_RawRaysOutgoing.csv'
flux = pd.read_csv(os.path.join(flux_simulation_folder, oe))
rp = pd.read_csv(os.path.join(rp_simulation_folder, oe))
source_flux = flux.drop_duplicates(subset='CPMU20.photonEnergy')[['CPMU20.photonEnergy', 'SourcePhotonFlux']]
oe           = 'CPMU20'
en_flux_path = os.path.join(flux_simulation_folder, f'input_param_{oe}_photonEnergy.dat')
energy_flux  = np.loadtxt(en_flux_path)




# Undulator SPECTRA
undulator = np.loadtxt(undulator_file, skiprows=8)

########################################
# plotting Flux and RP

fig, (axs) = plt.subplots(4, 2,figsize=(10,10))
fig.suptitle(f"{title}, {grating} l/mm grating")

log=True

# MIRROR COATING
de = 38.9579-30.0000
table = 'Henke'
theta = 0.8
E = np.arange(50, 5001, de)
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
ax2.set_title('Mirror Coating Reflectivity')
ax2.plot(E, IrCrB4C, 'b', label='IrCrB4C')
ax2.legend()

# UNDULATOR
ax = axs[0,1]
ax.plot(undulator[:,0], undulator[:,3])
ax.grid(which='both', axis='both')
if log:
    ax.set_yscale('log')
ax.set_ylabel('Flux [ph/s/0.1%bw]')
ax.set_xlabel('Harmonic energy [eV]')
ax.set_title('CPMU20 Flux')


# BEAMLINE TRANSMISSION, IN PERCENT
ax = axs[1,0]

ss = energy_flux.shape[0]
ind=0
for ind, es_size in enumerate(varying_var):
    filtered_flux = flux[flux['ExitSlit.totalHeight'] == es_size]
    energy = filtered_flux['CPMU20.photonEnergy']
    perc_flux = filtered_flux['PercentageRaysSurvived']
    ax.plot(energy,perc_flux, label=f'{varying_var_n} {int(es_size*1000)} {varying_var_unit}' )
ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Transmission [%]')
ax.set_title('Available Flux [in transmitted bandwidth]')
ax.grid(which='both', axis='both')
ax.legend()

# BEAMLINE TRANSMISSION, ABSOLUTE
ax = axs[1,1]

ss = energy_flux.shape[0]
ind=0

ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Transmission [Ph/s/...]')
ax.set_title('Available Flux [in transmitted bandwidth]')
ax.grid(which='both', axis='both')
for ind, es_size in enumerate(varying_var):
    filtered_flux = flux[flux['ExitSlit.totalHeight'] == es_size]
    energy = filtered_flux['CPMU20.photonEnergy']
    perc_flux = filtered_flux['PercentageRaysSurvived']
    flux_abs  = scale_undulator_flux(energy, perc_flux, undulator_file)
    ax.plot(energy,flux_abs, 'blue', label=f'{varying_var_n} {int(es_size*1000)} {varying_var_unit}'  )
if log:
    ax.set_yscale('log')
ax.legend()


# BANDWIDTH
ax = axs[2,0]
ss = energy_rp.shape[0]

for ind, es in enumerate(varying_var):
    filtered_rp = rp[rp['ExitSlit.totalHeight'] == es_size]
    energy = filtered_rp['CPMU20.photonEnergy']
    bw = filtered_rp['Bandwidth']    
    ax.plot(energy,bw*1000,colors[ind])#,label=f'{varying_var_n} {es} {varying_var_unit}')


ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Transmitted Bandwidth [meV]')
ax.set_title('Transmitted Bandwidth (tbw)')
ax.grid(which='both', axis='both')
# ax.set_yscale('log')
ax.legend()


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
    ax.plot(energy, res_p, colors[ind], label=f'{varying_var_n} {es} {varying_var_unit}')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('RP [a.u.]')
ax.set_title('Resolving Power')
ax.grid(which='both', axis='both')
ax.legend()

# HORIZONTAL FOCUS
ax = axs[3,0]
for ind, es in enumerate(varying_var):
    filtered_rp = rp[rp['ExitSlit.totalHeight'] == es_size]
    energy = filtered_rp['CPMU20.photonEnergy']
    foc = filtered_rp['HorizontalFocusFWHM']  
    ax.plot(energy,foc*1000,colors[ind],label=f'{varying_var_n} {es} {varying_var_unit}')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Horizontal Focus')
ax.legend()

# # VERTICAL FOCUS
ax = axs[3,1]
for ind, es in enumerate(varying_var):
    filtered_rp = rp[rp['ExitSlit.totalHeight'] == es_size]
    energy = filtered_rp['CPMU20.photonEnergy']
    foc = filtered_rp['VerticalFocusFWHM']  
    ax.plot(energy,foc*1000,colors[ind],label=f'{varying_var_n} {es} {varying_var_unit}')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Vertical Focus')

plt.tight_layout()
plt.savefig(f'plot/{title}_{grating}.png')

# plt.show()