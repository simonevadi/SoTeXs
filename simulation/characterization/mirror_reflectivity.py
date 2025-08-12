import numpy as np
import matplotlib.pyplot as plt

# path to xrt:
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm
from helper_lib import get_reflectivity





# plotting Flux and RP
fig, (axs) = plt.subplots(1, 1,figsize=(20,5))

# MIRROR COATING
ax2=axs
de = 38.9579-30.0000
table = 'Henke'
E = np.arange(500, 5001, de)


theta = 0.8
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C', rho=2.52,  kind='mirror',  table=table)
IrCrB4C = rm.Multilayer( tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)
IrCrB4C, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)

Pt = rm.Material('Pt', rho=21.45,  kind='mirror',  table=table)
Au = rm.Material('Au', rho=19.3,  kind='mirror',  table=table)
Rh = rm.Material('Rh', rho=12.45,  kind='mirror',  table=table)
Pt, _ = get_reflectivity(Pt, E=E, theta=theta)
Au, _ = get_reflectivity(Au, E=E, theta=theta)
Rh, _ = get_reflectivity(Rh, E=E, theta=theta)
Ir, _ = get_reflectivity(Ir, E=E, theta=theta)

ax2.plot(E, IrCrB4C, linewidth=3, label=f'IrCrB4C')
ax2.plot(E, Pt, label='Pt')
ax2.plot(E, Au, label='Au')
ax2.plot(E, Rh, label='Rh')
ax2.plot(E, Ir, label='Ir')


ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.legend()


plt.suptitle('SoTeXS, mirror reflectivity at 0.7° incident angle')
plt.tight_layout()
plt.savefig('plot/SoTeXS-mirror_reflectivity.png')


