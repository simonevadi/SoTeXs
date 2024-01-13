import numpy as np
import matplotlib.pyplot as plt
# path to xrt:
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import xrt.backends.raycing.materials as rm


def get_reflectivity(material,E, theta):
    theta = np.deg2rad(theta)
    rs, rp = material.get_amplitude(E, np.sin(theta))[0:2]
    return abs(rs)**2, abs(rp)**2

def trilayer(bottom,middle,top):
    trilayer_list = []
    thickness_middle = np.arange(50,71,10)
    thickness_top    = np.arange(40,61,10)

    for cr_t in thickness_middle:
        for b4c_t in thickness_top:
            IrCrB4C = rm.Multilayer( tLayer=B4C, tThickness=b4c_t, 
                                    bLayer=Cr, bThickness=cr_t, 
                                    nPairs=1, substrate=Ir)
            E = np.arange(50, 5001, de)
            IrCrB4C, _ = get_reflectivity(IrCrB4C, E=E, theta=theta)
            trilayer_list.append(IrCrB4C)



    IrCrB4C10=np.loadtxt('reflectivity/ircrb4c_1.0.dat', skiprows=2)

    nplots = thickness_middle.shape[0]
    fig, (axs) = plt.subplots(1,nplots+1,figsize=(30,10))

    counter = 0
    for axn,cr_t in enumerate(thickness_middle):
        ax2=axs[axn]
        axLast = axs[-1]
        ax2.set_xlabel('Energy [eV]')
        ax2.set_ylabel('Reflectivity [a.u.]')        
        ax2.set_title(bottom.name+' 30nm/'+middle.name+' '+str(cr_t/10)+'nm/'+top.name+' (variable)')
        for b4c_t in thickness_top:
            ax2.plot(E, trilayer_list[counter], label=top.name+' '+str(b4c_t/10)+'nm')
            ax2.plot(E, trilayer_list[counter], label=middle.name+' '+str(cr_t/10)+'/'+top.name+' '+str(b4c_t/10)+'nm')
            if b4c_t == thickness_top[-1]:
                ax2.legend()
            counter += 1



    plt.tight_layout()
    plt.show()
    
    
    
de = 38.9579-30.0000

table = 'Henke'
#table = 'Chantler'
theta = 1

Ir  = rm.Material('Ir',  rho=22.56, kind='mirror',table=table)
Cr  = rm.Material('Cr',  rho=7.15,  kind='mirror',table=table)
B4C = rm.Material(('B', 'C'), quantities=(4, 1), rho=2.52)


trilayer(Ir,Cr,B4C)
