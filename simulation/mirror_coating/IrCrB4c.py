import matplotlib.pyplot as plt

import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm

import numpy as np

from helper_lib import get_reflectivity


de = 38.9579-30.0000
table = 'Henke'
energy_coating = np.arange(500, 5001, de)
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C', rho=2.52,  kind='mirror',  table=table)

IrCrB4C = rm.Multilayer( tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)

coating_label = 'IrCrB4C'
beamline_name = 'SoTeXs'


fig = plt.figure(figsize=(10, 12))
fig.suptitle(f"{beamline_name} mirror coatings")

log=True


ax = plt.subplot2grid((3, 2), (0, 0), colspan=2)
theta = 0.7
Ir_coating, _ = get_reflectivity(Ir, E=energy_coating, theta=theta)
Cr_coating, _ = get_reflectivity(Cr, E=energy_coating, theta=theta)
B4C_coating, _ = get_reflectivity(B4C, E=energy_coating, theta=theta)
ax.plot(energy_coating, Ir_coating, label=f'Ir, {np.round(theta,1)}°')
ax.plot(energy_coating, Cr_coating, label=f'Cr, {np.round(theta,1)}°')
ax.plot(energy_coating, B4C_coating, label=f'B4C, {np.round(theta,1)}°')

ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Reflectivity [%]')
ax.set_title('IrCrB4C reflectivity')
ax.legend()
# MIRROR COATING
ax = plt.subplot2grid((3, 2), (1, 0))
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Reflectivity [%]')
ax.set_title('IrCrB4C reflectivity')
for theta in [x * 0.1 for x in range(5, 12)]:
    coating, _ = get_reflectivity(IrCrB4C, E=energy_coating, theta=theta)
    ax.plot(energy_coating, coating*100, label=f'{np.round(theta,1)}°')
ax.grid(True, which='both')

ax.legend()

# MIRROR COATING
ax = plt.subplot2grid((3, 2), (1, 1))
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Reflectivity [%]')
ax.set_title('IrCrB4C reflectivity, 4 mirrors')
for theta in [x * 0.1 for x in range(5, 12)]:
    coating, _ = get_reflectivity(IrCrB4C, E=energy_coating, theta=theta)
    ax.plot(energy_coating, (coating**4)*100, label=f'{np.round(theta,1)}°')
ax.grid(True, which='both')


# MIRROR COATING

ax = plt.subplot2grid((3, 2), (2, 0))
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Reflectivity [%]')
ax.set_title('IrCrB4C reflectivity')
theta = 0.70
for thickness in range(20, 70,  10):
    IrCrB4C = rm.Multilayer( tLayer=B4C, tThickness=thickness, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)
    coating, _ = get_reflectivity(IrCrB4C, E=energy_coating, theta=theta)
    ax.plot(energy_coating, coating*100, label=f'B4C: {int(thickness/10)} nm')
ax.grid(True, which='both')
ax.legend()


# MIRROR COATING

ax = plt.subplot2grid((3, 2), (2, 1))
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Reflectivity [%]')
ax.set_title('IrCrB4C reflectivity')
theta = 0.70
for thickness in range(20, 70,  10):
    IrCrB4C = rm.Multilayer( tLayer=B4C, tThickness=60, 
                        bLayer=Cr, bThickness=thickness, 
                        nPairs=1, substrate=Ir)
    coating, _ = get_reflectivity(IrCrB4C, E=energy_coating, theta=theta)
    ax.plot(energy_coating, coating*100, label=f'{int(thickness/10)} nm')
ax.grid(True, which='both')

ax.legend()







plt.tight_layout()
plt.savefig(f'plot/{beamline_name}_IrCrB4C.png')