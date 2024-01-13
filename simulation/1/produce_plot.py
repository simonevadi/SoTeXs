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
from helper_lib import scale_undulator_flux, order

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
energy    = np.arange(500,5001,500)
SlitSize  = np.array([0.05,0.04,0.03,0.02,0.01])
nsim      = energy.shape[0]*SlitSize.shape[0]

flux_percent_unordered = ppa.retrieve_flux_beamline(folder_name, source, oe, nsim, rounds=1, current=0.3)
flux_percent           = order(flux_percent_unordered)

ens = energy.shape[0]
flux_percent_50 = flux_percent[0*ens:1*ens]
flux_percent_40 = flux_percent[1*ens:2*ens]
flux_percent_30 = flux_percent[2*ens:3*ens]
flux_percent_20 = flux_percent[3*ens:4*ens]
flux_percent_10 = flux_percent[4*ens:5*ens]

flux_abs_50 = scale_undulator_flux(energy,flux_percent_50, undulator_file)
flux_abs_40 = scale_undulator_flux(energy,flux_percent_40, undulator_file)
flux_abs_30 = scale_undulator_flux(energy,flux_percent_30, undulator_file)
flux_abs_20 = scale_undulator_flux(energy,flux_percent_20, undulator_file)
flux_abs_10 = scale_undulator_flux(energy,flux_percent_10, undulator_file)

### ML RP
energy_ml_rp = np.arange(500,5001,500)
SlitSize  = np.array([0.05,0.04,0.03,0.02,0.01])
rounds      = 10
folder_name = 'RAYPy_Simulation_RP_battery_FLUX_forML_IrCrB4C'
oe          = 'DetectorAtFocus'
nsim      = energy_ml_rp.shape[0]*SlitSize.shape[0]

bw_ML_2400_2_un, focx_ML_2400_2_un, focy_ML_2400_2_un = ppa.retrieve_bw_and_focusSize(folder_name, oe, nsim, rounds=rounds)
bw_ML_2400_2 = order(bw_ML_2400_2_un)
focx_ML_2400_2= order(focx_ML_2400_2_un)
focy_ML_2400_2 = order(focy_ML_2400_2_un)

# Undulator SPECTRA
undulator = np.loadtxt(undulator_file, skiprows=8)


# scaling
flux_abs_50_MLBG_mfm_second = ML_eff(flux_abs_50, 
                                    ind='MLBG_mfm_second', 
                                    energy=energy,
                                    grating_eff_file=grating_eff_file)
flux_abs_40_MLBG_mfm_second = ML_eff(flux_abs_40, 
                                    ind='MLBG_mfm_second', 
                                    energy=energy,
                                    grating_eff_file=grating_eff_file)
flux_abs_30_MLBG_mfm_second = ML_eff(flux_abs_30, 
                                    ind='MLBG_mfm_second', 
                                    energy=energy,
                                    grating_eff_file=grating_eff_file)
flux_abs_20_MLBG_mfm_second = ML_eff(flux_abs_20, 
                                    ind='MLBG_mfm_second', 
                                    energy=energy,
                                    grating_eff_file=grating_eff_file)
flux_abs_10_MLBG_mfm_second = ML_eff(flux_abs_10, 
                                    ind='MLBG_mfm_second', 
                                    energy=energy,
                                    grating_eff_file=grating_eff_file)


########################################
# plotting Flux and RP

fig, (axs) = plt.subplots(4, 2,figsize=(10,10))

# text
ax = axs[0,0]
en       = extract_from_Andrey('MLBG_mfm_second', 'energy', ML_eff_file)
grat_eff = extract_from_Andrey('MLBG_mfm_second', 'grat_eff', ML_eff_file)
mirr_eff = extract_from_Andrey('MLBG_mfm_second', 'mir_eff', ML_eff_file)
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
ax.plot(energy,flux_percent_50, 'r', label='ExitSlit 50 um' )
ax.plot(energy,flux_percent_40, 'b', label='ExitSlit 40 um' )
ax.plot(energy,flux_percent_30, 'g', label='ExitSlit 30 um' )
ax.plot(energy,flux_percent_20, 'orange', label='ExitSlit 20 um' )
ax.plot(energy,flux_percent_10, 'violet', label='ExitSlit 10 um' )

ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Transmission [%]')
ax.set_title('Beamline Transmission')
ax.grid(which='both', axis='both')
ax.legend()


# ABSOLUTE FLUX
ax = axs[2,0]

ax.plot(energy,flux_abs_50, 'r', label='ExitSlit 50 um' )
ax.plot(energy,flux_abs_40, 'b', label='ExitSlit 40 um' )
ax.plot(energy,flux_abs_30, 'g', label='ExitSlit 30 um' )
ax.plot(energy,flux_abs_20, 'orange', label='ExitSlit 20 um' )
ax.plot(energy,flux_abs_10, 'violet', label='ExitSlit 10 um' )

ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Input Flux [ph/s/tbw]')
ax.set_yscale('log')
ax.set_title('Available Flux (in transmitted bandwidth)')
ax.grid(which='both', axis='both')
# ax.legend()

# ABSOLUTE FLUX SCALED WITH ML EFF.
ax = axs[2,1]

ax.plot(energy,flux_abs_50_MLBG_mfm_second, 'r', label='ExitSlit 50 um' )
ax.plot(energy,flux_abs_40_MLBG_mfm_second, 'b', label='ExitSlit 40 um' )
ax.plot(energy,flux_abs_30_MLBG_mfm_second, 'g', label='ExitSlit 30 um' )
ax.plot(energy,flux_abs_20_MLBG_mfm_second, 'orange', label='ExitSlit 20 um' )
ax.plot(energy,flux_abs_10_MLBG_mfm_second, 'violet', label='ExitSlit 10 um' )

ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Flux [ph/s/tbw]')
ax.set_yscale('log')
ax.set_title('Flux (2400l/mm, Blazed Grat., 2nd order)')
ax.grid(which='both', axis='both')
# ax.legend()

# BANDWIDTH
ax = axs[3,0]
ss = energy_ml_rp.shape[0]
ax.plot(energy_ml_rp,bw_ML_2400_2[0*ss:1*ss],'r',label='ExitSlit 50 um')
ax.plot(energy_ml_rp,bw_ML_2400_2[1*ss:2*ss],'b',label='ExitSlit 40 um')
ax.plot(energy_ml_rp,bw_ML_2400_2[2*ss:3*ss],'g',label='ExitSlit 30 um')
ax.plot(energy_ml_rp,bw_ML_2400_2[3*ss:4*ss],'orange',label='ExitSlit 20 um')
ax.plot(energy_ml_rp,bw_ML_2400_2[4*ss:5*ss],'violet',label='ExitSlit 10 um')


ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Transmitted Bandwidth [eV]')
ax.set_title('Transmitted bandwidth (tbw)')
ax.grid(which='both', axis='both')
# ax.legend()


# RESOLVING POWER
ax = axs[3,1]
ss = energy_ml_rp.shape[0]
ax.plot(energy_ml_rp,energy_ml_rp/bw_ML_2400_2[0*ss:1*ss],'r')#,label='ExitSlit 50 um')
ax.plot(energy_ml_rp,energy_ml_rp/bw_ML_2400_2[1*ss:2*ss],'b')#,label='ExitSlit 40 um')
ax.plot(energy_ml_rp,energy_ml_rp/bw_ML_2400_2[2*ss:3*ss],'g')#,label='ExitSlit 30 um')
ax.plot(energy_ml_rp,energy_ml_rp/bw_ML_2400_2[3*ss:4*ss],'orange')#,label='ExitSlit 20 um')
ax.plot(energy_ml_rp,energy_ml_rp/bw_ML_2400_2[4*ss:5*ss],'violet')#,label='ExitSlit 10 um')

ax.axhline(y=6000, color='k', linestyle='dashed', label='RP=6000')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('RP [a.u.]')
ax.set_title('Resolving Power')
ax.grid(which='both', axis='both')
ax.legend()

plt.tight_layout()
plt.savefig('plot/battery_beamline_IrCrB4C_2order_FluxRp.png')


########################################
# plotting FOCUS SIZE
fig, (axs) = plt.subplots(1, 2,figsize=(10,10))

# HORIZONTAL FOCUS
ax = axs[0]
focx_ML_2400_2 = focx_ML_2400_2*1000 # in micrometer
ax.plot(energy_ml_rp, focx_ML_2400_2[0*ss:1*ss], 'r', label='ExitSlit 50 um')
ax.plot(energy_ml_rp, focx_ML_2400_2[1*ss:2*ss], 'b', label='ExitSlit 40 um')
ax.plot(energy_ml_rp, focx_ML_2400_2[2*ss:3*ss], 'g', label='ExitSlit 30 um')
ax.plot(energy_ml_rp, focx_ML_2400_2[3*ss:4*ss], 'violet', label='ExitSlit 20 um')
ax.plot(energy_ml_rp, focx_ML_2400_2[4*ss:5*ss], 'orange', label='ExitSlit 10 um')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Horizontal focus')
ax.legend()

# VERTICAL FOCUS
ax = axs[1]
focy_ML_2400_2 = focy_ML_2400_2*1000 # in micrometer
ax.plot(energy_ml_rp, focy_ML_2400_2[0*ss:1*ss], 'r', label='ExitSlit 50 um')
ax.plot(energy_ml_rp, focy_ML_2400_2[1*ss:2*ss], 'b', label='ExitSlit 40 um')
ax.plot(energy_ml_rp, focy_ML_2400_2[2*ss:3*ss], 'g', label='ExitSlit 30 um')
ax.plot(energy_ml_rp, focy_ML_2400_2[3*ss:4*ss], 'violet', label='ExitSlit 20 um')
ax.plot(energy_ml_rp, focy_ML_2400_2[4*ss:5*ss], 'orange', label='ExitSlit 10 um')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Vertical focus')

plt.savefig('plot/battery_beamline_IrCrB4C_2order_focusSize.png')

plt.show()