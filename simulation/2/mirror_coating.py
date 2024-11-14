import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm

import numpy as np

from helper_lib import get_reflectivity


de = 38.9579-30.0000
table = 'Henke'
theta_coating = 0.8
energy_coating = np.arange(50, 5001, de)
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material('C', rho=2.52,  kind='mirror',  table=table)
IrCrB4C = rm.Multilayer( tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)

coating, _ = get_reflectivity(IrCrB4C, E=energy_coating, theta=theta_coating)
coating_label = 'IrCrB4C'