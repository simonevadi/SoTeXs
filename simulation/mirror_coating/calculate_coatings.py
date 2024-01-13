import numpy as np
import matplotlib.pyplot as plt
# path to xrt:
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm


def get_reflectivity(material,E, theta):
    theta = np.deg2rad(theta)
    rs, rp = material.get_amplitude(E, np.sin(theta))[0:2]
    return abs(rs)**2, abs(rp)**2


de = 38.9579-30.0000

table = 'Henke'
#table = 'Chantler'
theta = 1

Rh  = rm.Material('Rh', rho=12.41, kind='mirror')
Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
C   = rm.Material('C',   rho=3.52,  kind='mirror',table=table)
B4C = rm.Material('C', rho=2.52,  kind='mirror',  table=table)
IrCrC = rm.Multilayer( tLayer=C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)

IrCrB4C = rm.Multilayer( tLayer=B4C, tThickness=40, 
                        bLayer=Cr, bThickness=60, 
                        nPairs=1, substrate=Ir)
IrCr = rm.Coated(coating=Cr, substrate=Ir, cThickness=60)
E = np.arange(50, 4001, de)
Rh, _      = get_reflectivity(Rh,      E=E, theta=theta)
IrCrC, _   = get_reflectivity(IrCrC,   E=E, theta=theta)
IrCrB4C, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)
IrCr, _    = get_reflectivity(IrCr,    E=E, theta=theta)


Rh10=np.loadtxt('reflectivity/rh_1.0.dat', skiprows=2)
IrCr10=np.loadtxt('reflectivity/ircr_1.0.dat', skiprows=2)
IrCrC10=np.loadtxt('reflectivity/ircrc_1.0.dat', skiprows=2)
IrCrB4C10=np.loadtxt('reflectivity/ircrb4c_1.0.dat', skiprows=2)

fig, (axs) = plt.subplots(1, 4,figsize=(30,10))

ax2=axs[0]
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.set_title('Rhodium')
ax2.plot(E, Rh, 'r', label='XRT')
ax2.plot(Rh10[:,0],Rh10[:,1], 'b', label='CXRO')
ax2.legend()


ax2=axs[1]
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.set_title('IrCrC')
ax2.plot(E, IrCrC, 'r', label='XRT')
ax2.plot(IrCrC10[:,0],IrCrC10[:,1], 'b', label='CXRO')
ax2.legend()


ax2=axs[2]
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.set_title('IrCrB4C')
ax2.plot(E, IrCrB4C, 'r', label='XRT')
ax2.plot(IrCrB4C10[:,0],IrCrB4C10[:,1], 'b', label='CXRO')
ax2.legend()

ax2=axs[3]
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.set_title('IrCr')
ax2.plot(IrCrC10[:,0],IrCrC10[:,1], 'b', label='C')
ax2.plot(IrCrB4C10[:,0],IrCrB4C10[:,1], 'r', label='B4C')
ax2.legend()

plt.tight_layout()
plt.show()