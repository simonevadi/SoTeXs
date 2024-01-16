import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# path to xrt:
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm

# andrey ML
from andrey_lib import ML_eff, extract_from_Andrey

# raypyng 
from raypyng.postprocessing import PostProcessAnalyzed

# from helper library
from helper_lib import get_reflectivity
from helper_lib import scale_undulator_flux, order as undulator_order


from params import order as grating_order, energy_rp, energy_flux, SlitSize
from params import index, repeat_rp, repeat_flux
from params import ncpu_rp as ncpu

# define undulator file
undulator_file = os.path.join('undulator', 'CPMU20_B2l_k_dep_simp_all_harm_300mA.dbr')

# define grating efficiency file
grating_eff_file=os.path.join('ML_eff', 'grating_eff.xlsx')
ML_eff_file = os.path.join('ML_eff','grating_eff_5000.xlsx')


ppa = PostProcessAnalyzed()

# Gratings Flux
folder_name  = 'RAYPy_Simulation_FLUX_battery_FLUX_forML_IrCrB4C'
source       = 'CPMU20'
oe           = 'DetectorAtFocus'
nsim         = energy_flux.shape[0]*SlitSize.shape[0]

flux_percent_unordered = ppa.retrieve_flux_beamline(folder_name, source, oe, nsim, rounds=repeat_flux, current=0.3)
flux_percent           = undulator_order(flux_percent_unordered)




### ML RP
folder_name = 'RAYPy_Simulation_RP_battery_FLUX_forML_IrCrB4C'
oe          = 'DetectorAtFocus'
nsim        = energy_rp.shape[0]*SlitSize.shape[0]

bw_ML_2400_2_un, focx_ML_2400_2_un, focy_ML_2400_2_un = ppa.retrieve_bw_and_focusSize(folder_name, 
                                                                                      oe, 
                                                                                      nsim, 
                                                                                      rounds=repeat_rp)
bw_ML_2400_2    = undulator_order(bw_ML_2400_2_un)
focx_ML_2400_2  = undulator_order(focx_ML_2400_2_un)
focy_ML_2400_2  = undulator_order(focy_ML_2400_2_un)

# Undulator SPECTRA
undulator = np.loadtxt(undulator_file, skiprows=8)




########################################
# plotting Flux and RP

fig, (axs) = plt.subplots(4, 2,figsize=(10,10))

ens_flux = energy_flux.shape[0]
ens_rp   = energy_rp.shape[0]

# text
ax = axs[0,0]
en       = extract_from_Andrey(index, 'energy', ML_eff_file)
grat_eff = extract_from_Andrey(index, 'grat_eff', ML_eff_file)
mirr_eff = extract_from_Andrey(index, 'mir_eff', ML_eff_file)
eff = grat_eff*mirr_eff
ax.plot(en, eff)
ax.set_ylabel('Efficiency')
ax.set_xlabel('Energy [eV]')
ax.set_title('ML monochromator efficiency')
ax.grid(which='both', axis='both')

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

ax2=axs[0,1]
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.set_title('Mirror Coating Reflectivity')
ax2.plot(E, IrCrB4C, 'b', label='IrCrB4C')
ax2.legend()


# UNDULATOR
ax = axs[1,0]
ax.plot(undulator[:,0], undulator[:,3])
ax.grid(which='both', axis='both')
ax.set_yscale('log')
ax.set_ylabel('Flux [ph/s/0.1%bw]')
ax.set_xlabel('Harmonic energy [eV]')
ax.set_title('CPMU20 Flux')


# PERCENTAGE FLUX
ax = axs[1,1]
for ind, val in enumerate(SlitSize):
    es=int(val*1000)
    ax.plot(energy_flux,flux_percent[ind*ens_flux:(ind+1)*ens_flux], label=f'ExitSlit {es} um' )

ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Transmission [%]')
ax.set_title('Beamline Transmission')
ax.grid(which='both', axis='both')
ax.legend()


# ABSOLUTE FLUX
ax = axs[2,0]

for ind, val in enumerate(SlitSize):
    es=int(val*1000)
    flux_abs = scale_undulator_flux(energy_flux,flux_percent[ind*ens_flux:(ind+1)*ens_flux], undulator_file)
    ax.plot(energy_flux,flux_abs, label=f'ExitSlit {es} um' )

ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Input Flux [ph/s/tbw]')
ax.set_yscale('log')
ax.set_title('Available Flux (in transmitted bandwidth)')
ax.grid(which='both', axis='both')
# ax.legend()

# ABSOLUTE FLUX SCALED WITH ML EFF.
ax = axs[2,1]

for ind, val in enumerate(SlitSize):
    es=int(val*1000)
    flux_abs = scale_undulator_flux(energy_flux,
                                    flux_percent[ind*ens_flux:(ind+1)*ens_flux], 
                                    undulator_file)
    flux_abs_ML = ML_eff(flux_abs,
                         ind=index, 
                         energy=energy_flux,
                         grating_eff_file=grating_eff_file)
    ax.plot(energy_flux,flux_abs_ML, label=f'ExitSlit {es} um' )

ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Flux [ph/s/tbw]')
ax.set_yscale('log')
ax.set_title('Flux (2400l/mm, Blazed Grat., 2nd order)')
ax.grid(which='both', axis='both')
# ax.legend()

# BANDWIDTH
ax = axs[3,0]
for ind, val in enumerate(SlitSize):
    es=int(val*1000)
    ax.plot(energy_rp,bw_ML_2400_2[ind*ens_rp:(ind+1)*ens_rp],label=f'ExitSlit {es} um')
    

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Transmitted Bandwidth [eV]')
ax.set_title('Transmitted bandwidth (tbw)')
ax.grid(which='both', axis='both')
# ax.legend()


# RESOLVING POWER
ax = axs[3,1]
for ind, val in enumerate(SlitSize):
    es=int(val*1000)
    ax.plot(energy_rp,energy_rp/bw_ML_2400_2[ind*ens_rp:(ind+1)*ens_rp],label=f'ExitSlit {es} um')


ax.axhline(y=6000, color='k', linestyle='dashed', label='RP=6000')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('RP [a.u.]')
ax.set_title('Resolving Power')
ax.grid(which='both', axis='both')
ax.legend()
plt.suptitle('SoTeXs - Flux and Resolving Power', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('plot/battery_beamline_IrCrB4C_2order_FluxRp.png')


########################################
# plotting FOCUS SIZE
fig, (axs) = plt.subplots(1, 2,figsize=(10,10))

# VERTICAL FOCUS
ax = axs[1]
focy_ML_2400_2 = focy_ML_2400_2*1000 # in micrometer
for ind, val in enumerate(SlitSize):
    es=int(val*1000)
    ax.plot(energy_rp,focy_ML_2400_2[ind*ens_rp:(ind+1)*ens_rp],label=f'ExitSlit {es} um')
bot, top = ax.get_ylim()
ax.set_ylim(bottom=bot, top=top+2)
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Vertical focus')
ax.legend()


# HORIZONTAL FOCUS
ax = axs[0]
focx_ML_2400_2 = focx_ML_2400_2*1000 # in micrometer
for ind, val in enumerate(SlitSize):
    es=int(val*1000)
    if ind ==0:
        focx_ML_average=focx_ML_2400_2[ind*ens_rp:(ind+1)*ens_rp]
    else:
        focx_ML_average+=focx_ML_2400_2[ind*ens_rp:(ind+1)*ens_rp]

    # ax.plot(energy_rp,focx_ML_2400_2[ind*ens_rp:(ind+1)*ens_rp],label=f'ExitSlit {es} um')
ax.plot(energy_rp,focx_ML_average/(ind+1),'black', label=f'average')
# bot = np.average(focx_ML_average/(ind+1))-2
# top = np.average(focx_ML_average/(ind+1))+2
ax.set_ylim(bottom=bot, top=top+2)
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Horizontal focus')
ax.legend()
plt.suptitle('SoTeXs - Focus Size', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('plot/battery_beamline_IrCrB4C_2order_focusSize.png')

plt.show()