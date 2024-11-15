import matplotlib.pyplot as plt

import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm

import numpy as np

from helper_lib import get_reflectivity


# Material setup
table = 'Henke'
Au = rm.Material('Au', rho=19.32, kind='mirror', table=table)
Rh = rm.Material('Rh', rho=12.41, kind='mirror', table=table)
Pd = rm.Material('Pd', rho=12.02, kind='mirror', table=table)
Pt = rm.Material('Pt', rho=21.45, kind='mirror', table=table)
Ir = rm.Material('Ir', rho=22.56, kind='mirror', table=table)
Cr = rm.Material('Cr', rho=7.15, kind='mirror', table=table)
B4C = rm.Material('C', rho=2.52, kind='mirror', table=table)

energy_coating = np.arange(500, 5001, 38.9579 - 30.0000)  # Energy range

coating_label = 'IrCrB4C'
beamline_name = 'SoTeXs'


fig = plt.figure(figsize=(10, 12))
fig.suptitle(f"{beamline_name} mirror coatings")

theta_list = [0.5, 0.6, 0.7, 0.8]
for ind, theta in enumerate(theta_list):
    ax = plt.subplot2grid((len(theta_list), 2), (ind, 0), colspan=2)
    # Get reflectivity
    Ir_coating, _ = get_reflectivity(Ir, E=energy_coating, theta=theta)
    Cr_coating, _ = get_reflectivity(Cr, E=energy_coating, theta=theta)
    B4C_coating, _ = get_reflectivity(B4C, E=energy_coating, theta=theta)
    Au_coating, _ = get_reflectivity(Au, E=energy_coating, theta=theta)
    Rh_coating, _ = get_reflectivity(Rh, E=energy_coating, theta=theta)
    Pd_coating, _ = get_reflectivity(Pd, E=energy_coating, theta=theta)
    Pt_coating, _ = get_reflectivity(Pt, E=energy_coating, theta=theta)
    
    # Plot
    ax.plot(energy_coating, Ir_coating, label=f'Ir')
    ax.plot(energy_coating, Cr_coating, label=f'Cr')
    ax.plot(energy_coating, B4C_coating, label=f'B4C')
    ax.plot(energy_coating, Au_coating, label=f'Au')
    ax.plot(energy_coating, Rh_coating, label=f'Rh')
    ax.plot(energy_coating, Pd_coating, label=f'Pd')
    ax.plot(energy_coating, Pt_coating, label=f'Pt')

    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Reflectivity [%]')
    ax.set_title(f'Theta = {theta}')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

plt.tight_layout(rect=[0, 0, 0.85, 1])  # Adjust the right margin to make room for the legend
plt.savefig(f'plot/{beamline_name}_standard_coatings.png')
plt.show()

