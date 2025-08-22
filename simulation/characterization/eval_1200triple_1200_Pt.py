import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# path to xrt:
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm
from helper_lib import get_reflectivity


# file/folder/ml index definition
from params import undulator_spectra
from params import efficiency


from raypyng.postprocessing import PostProcessAnalyzed
p = PostProcessAnalyzed()

# 1200 l/mm grating
flux_simulation_folder07 = 'RAYPy_Simulation_1200_Pt' 

oe = 'DetectorAtFocus' + '_RawRaysOutgoing.csv'
flux_Pt = pd.read_csv(os.path.join(flux_simulation_folder07, oe))
flux_Pt = flux_Pt[flux_Pt['CPMU20.photonEnergy'] < 2200]

# 2400 l/mm grating
flux_simulation_folder07 = 'RAYPy_Simulation_1200_triple_coating' 

oe = 'DetectorAtFocus' + '_RawRaysOutgoing.csv'
flux_triple = pd.read_csv(os.path.join(flux_simulation_folder07, oe))
flux_triple = flux_triple[flux_triple['CPMU20.photonEnergy'] < 5000]



cff_list = flux_triple['PG.cFactor'].unique()
exit_slit_list = flux_triple['ExitSlit.openingHeight'].unique()
exit_slit_list = [0.03]

xlim = [500, 2100]

# plotting beamline
fig, (axs) = plt.subplots(4, 2,figsize=(12,12))

# MIRROR COATING
ax2=axs[0,0]
de = 38.9579-30.0000
table = 'Henke'
energy_coating = np.arange(500, 2501, de)
theta = 0.7

Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C', rho=2.52,  kind='mirror',  table=table)
Pt  = rm.Material('Pt', rho=21.45, kind='mirror', table=table)
IrCrB4C = rm.Multilayer( tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)
IrCrB4C, _ = get_reflectivity(IrCrB4C, E=energy_coating, theta=theta)
Pt, _ = get_reflectivity(Pt, E=energy_coating, theta=theta)

ax2.plot(energy_coating, IrCrB4C, label=f'IrCrB4C at {theta}°')
ax2.plot(energy_coating, Pt, label=f'Pt at {theta}°')

ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.set_title(f'Mirror Coating Reflectivity ')
ax2.legend()

# Save data to a CSV file
output_file = "coating_IrCrB4C_07.csv"
np.savetxt(output_file, np.column_stack((energy_coating, IrCrB4C)),
           delimiter=",", header="Energy[eV],Reflectivity", comments='')
output_file = "coating_Pt_07.csv"
np.savetxt(output_file, np.column_stack((energy_coating, Pt)),
           delimiter=",", header="Energy[eV],Reflectivity", comments='')



# Undulator Flux
ax = axs[0,1]
ax.plot(undulator_spectra[:,0], undulator_spectra[:,3])

ax.set_title('CPMU20 Flux')
ax.grid(which='both', axis='both')
ax.set_ylabel('Flux [ph/s/0.1%bw]')
ax.set_xlabel('Energy [eV]')
ax.set_xlim(xlim[0], xlim[1])

# AVAILABLE/ABS FLUX 
ax = axs[1,0]
ax2 = axs[1,1]
for ind, es in enumerate(exit_slit_list):
    #2400
    filtered_flux = flux_triple[flux_triple['ExitSlit.openingHeight'] == es]
    energy = filtered_flux['CPMU20.photonEnergy']
    perc_flux = filtered_flux['PercentageRaysSurvived']
    abs_flux = filtered_flux['PhotonFlux1']
    ax.plot(energy,perc_flux, label=f'1200 triple')
    ax2.plot(energy,abs_flux)

    # 1200
    window = 20
    
    cff = 2.25
    filtered_flux = flux_Pt[flux_Pt['PG.cFactor'] == cff]
    energy = filtered_flux['CPMU20.photonEnergy']
    perc_flux = filtered_flux['PercentageRaysSurvived']
    abs_flux = filtered_flux['PhotonFlux1']
    ax.plot(p.moving_average(energy, window),p.moving_average(perc_flux, window), label=f'1200')
    ax2.plot(p.moving_average(energy, window),p.moving_average(abs_flux, window))

             
ax.set_xlabel(r'Energy [eV]')
ax.set_ylabel('Transmission [%]')
ax.set_title('Available Flux (in percent)')
ax.grid(which='both', axis='both')
ax.legend()
# ax.set_yscale('log')
ax2.set_title('Available Flux')
ax2.set_xlabel(r'Energy [eV]')
ax.grid(which='both', axis='both')
ax2.set_ylabel('Flux [ph/s/0.3A/tbw]')
ax.set_xlim(xlim[0], xlim[1])

ax2.set_yscale('log')
# ax2.set_ylim(10e9, 10e13)



# BANDWIDTH
ax = axs[2,0]
window = 10
for ind, es in enumerate(exit_slit_list):
    # 2400
    filtered_rp = flux_triple[flux_triple['ExitSlit.openingHeight'] == es]
    energy = filtered_rp['CPMU20.photonEnergy']
    bw = filtered_rp['Bandwidth']
    ax.plot(p.moving_average(energy,window),p.moving_average(bw,window))


    # 1200
    filtered_rp = flux_Pt[flux_Pt['PG.cFactor'] == cff]
    energy = filtered_rp['CPMU20.photonEnergy']
    bw = filtered_rp['Bandwidth']
    ax.plot(p.moving_average(energy,window),p.moving_average(bw, window) )


ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Transmitted Bandwidth [eV]')
ax.set_title('Transmitted bandwidth (tbw)')
ax.grid(which='both', axis='both')

# Calculate the line as 6000 divided by the energy values
energy_threshold = np.arange(energy.iloc[0], 6000)
threshold_transmission = energy_threshold/6000
ax.plot(energy_threshold, threshold_transmission, linestyle='dashed', color='black', label='tbw at RP=6000')
ax.legend()
ax.set_xlim(xlim[0], xlim[1])
ax.set_ylim(0, 0.42)


# RESOLVING POWER
ax = axs[2,1]
window=20
for ind, es in enumerate(exit_slit_list):
    # 2400
    filtered_rp = flux_triple[flux_triple['ExitSlit.openingHeight'] == es]
    energy = filtered_rp['CPMU20.photonEnergy']
    bw = filtered_rp['Bandwidth']
    ax.plot(p.moving_average(energy,window),p.moving_average(energy/bw,window))
    
    # 1200
    window = 200
    filtered_rp = flux_Pt[flux_Pt['PG.cFactor'] == cff]
    energy = filtered_rp['CPMU20.photonEnergy']
    bw = filtered_rp['Bandwidth']
    ax.plot(p.moving_average(energy, window),p.moving_average(energy/bw, window) )

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('RP [a.u.]')
ax.set_title('Resolving Power')
ax.grid(which='both', axis='both')
ax.axhline(y=6000, color='k', linestyle='--', label='RP=6000')
ax.legend()
ax.set_xlim(xlim[0], xlim[1])
ax.set_ylim(5500, 14000)


# HORIZONTAL FOCUS
ax = axs[3,0]
# Initialize an empty list to accumulate 'HorizontalFocusFWHM' data
focx07 = []
focx07_1200 = []

# Loop through each slit size in the 'SlitSize' list
for ind, es in enumerate(exit_slit_list):
    #2400
    filtered_rp = flux_triple[flux_triple['ExitSlit.openingHeight'] == es]
    energy = filtered_rp['CPMU20.photonEnergy']
    focx07.append(filtered_rp['HorizontalFocusFWHM'])

    # 1200
    filtered_rp07 = flux_Pt[flux_Pt['PG.cFactor'] == cff]
    energy07_1200 = filtered_rp07['CPMU20.photonEnergy']
    focx07_1200.append(filtered_rp07['HorizontalFocusFWHM'])

#2400 
focx07 = np.array(focx07)
focx07 = np.mean(focx07, axis=0)

# 1200
focx07_1200 = np.array(focx07_1200)
focx07_1200 = np.mean(focx07_1200, axis=0)


#2400
window = 20
ax.plot(p.moving_average(energy,window*1),p.moving_average(focx07*1000,window*1) )
# 1200
window=100
ax.plot(p.moving_average(energy07_1200,window),p.moving_average(focx07_1200*1000,window))
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Horizontal focus')
ax.set_ylim(6, 14)
ax.set_xlim(xlim[0], xlim[1])

# ax.legend()

# VERTICAL FOCUS
ax = axs[3,1]
for ind, es in enumerate(exit_slit_list):
    window=20
    filtered_rp = flux_triple[flux_triple['ExitSlit.openingHeight'] == es]
    energy = filtered_rp['CPMU20.photonEnergy']
    focy = filtered_rp['VerticalFocusFWHM']
    ax.plot(p.moving_average(energy,window),p.moving_average(focy*1000,window), label=f'ExitSlit {es} μm' )

    # 1200
    window = 100
    filtered_rp = flux_Pt[flux_Pt['PG.cFactor'] == cff]
    energy = filtered_rp['CPMU20.photonEnergy']
    focy = filtered_rp['VerticalFocusFWHM']
    ax.plot(p.moving_average(energy,window),p.moving_average(focy*1000,window), label=f'ExitSlit {cff}, theta=0.7°' )

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Focus Size [um]')
ax.set_title('Vertical focus')
ax.set_ylim(6, 14)
ax.set_xlim(xlim[0], xlim[1])



plt.suptitle('SoTeXS, ES=30 µm')
plt.tight_layout()
plt.savefig('plot/SoTeXS_1200Pt_1200triple.png')
plt.close()




# Flux Density
fig, (ax) = plt.subplots(1, 1,figsize=(12,12))
for ind, es in enumerate(exit_slit_list):
    # 2400
    window = 50

    filtered_flux = flux_triple[flux_triple['ExitSlit.openingHeight'] == es]
    energy = filtered_flux['CPMU20.photonEnergy']
    abs_flux = filtered_flux['PhotonFlux1']
    foc_area = (filtered_flux['VerticalFocusFWHM']*filtered_flux['HorizontalFocusFWHM'])*1000  # in µm²
    flux_density = abs_flux / foc_area
    ax.plot(p.moving_average(energy, window),p.moving_average(flux_density, window), label=f'2400')


    # 1200
    filtered_flux = flux_Pt[flux_Pt['ExitSlit.openingHeight'] == es]
    energy = filtered_flux['CPMU20.photonEnergy']
    abs_flux = filtered_flux['PhotonFlux1']
    foc_area = (filtered_flux['VerticalFocusFWHM']*filtered_flux['HorizontalFocusFWHM'])*1000  # in µm²
    flux_density = abs_flux / foc_area
    ax.plot(p.moving_average(energy, window),p.moving_average(flux_density, window), label=f'1200')

ax.set_xlabel(f'Energy [eV]')
ax.set_ylabel('Flux Density [ph/s/0.3A/tbw/µm²]')
ax.set_title('Available Flux (in percent)')
ax.grid(which='both', axis='both')
ax.legend()

plt.suptitle('SoTeXS, ES=30 µm')
plt.tight_layout()
plt.savefig('plot/SoTeXS_1200Pt_1200triple_flux_density.png')
