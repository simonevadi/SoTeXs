import numpy as np
import matplotlib.pyplot as plt

Pt10=np.loadtxt('reflectivity/pt_1.0.dat', skiprows=2)

Pd10=np.loadtxt('reflectivity/pd_1.0.dat', skiprows=2)

PtPd10=np.loadtxt('reflectivity/ptpd_1.0.dat', skiprows=2)

IrCrC10=np.loadtxt('reflectivity/ircrc_1.0.dat', skiprows=2)

IrCrB4C10=np.loadtxt('reflectivity/ircrb4c_1.0.dat', skiprows=2)

PtCrB4C10=np.loadtxt('reflectivity/ptcrb4c_1.0.dat', skiprows=2)

IrNiB4C10=np.loadtxt('reflectivity/irnib4c_1.0.dat', skiprows=2)

Rh10=np.loadtxt('reflectivity/rh_1.0.dat', skiprows=2)

IrCr10=np.loadtxt('reflectivity/ircr_1.0.dat', skiprows=2)


fig, (axs) = plt.subplots(1, 2,figsize=(20,10))


# 1.0 degree 
ax2=axs[0]
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.plot(Pt10[:,0],Pt10[:,1], 'b', linestyle='solid', label='Pt')

ax2.plot(Rh10[:,0],Rh10[:,1], 'r', linestyle='solid', label='Rh')

ax2.plot(Pd10[:,0],Pd10[:,1], 'g', linestyle='solid', label='Pd')

ax2.plot(PtPd10[:,0],PtPd10[:,1], 'violet', linestyle='solid', label='PtPd')

ax2.plot(IrCr10[:,0],IrCr10[:,1], 'orange', linestyle='solid', label='IrCr')

ax2.plot(IrCrC10[:,0],IrCrC10[:,1], 'k', linestyle='solid', label='IrCrC')

ax2.plot(IrCrB4C10[:,0],IrCrB4C10[:,1], 'magenta', linestyle='solid', label='IrCrB4C')

ax2.plot(IrNiB4C10[:,0],IrNiB4C10[:,1], 'pink', linestyle='solid', label='IrNiB4C')

ax2.plot(PtCrB4C10[:,0],PtCrB4C10[:,1], 'lightblue', linestyle='solid', label='PtCrB4C')

tick_pos = np.arange(0,5001,100)
ax2.xaxis.set_ticks(tick_pos)
ax2.set_xticklabels(ax2.get_xticks(), rotation = 90)

start, end = ax2.get_ylim()
tick_pos = np.array([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
ax2.yaxis.set_ticks(tick_pos)
ax2.set_yticklabels(ax2.get_yticks())
ax2.grid(visible=True, which='both', axis='both')

ax2.set_title('Comparison different coatings at 1.0°')
ax2.legend()


# 1.0 degree best candidates
ax2=axs[1]
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.set_title('Most promising candidates at 1.0°')
ax2.plot(Rh10[:,0],Rh10[:,1], 'r', linestyle='solid', label='Rh')
ax2.plot(PtPd10[:,0],PtPd10[:,1], 'violet', linestyle='solid', label='PtPd')
ax2.plot(IrCrC10[:,0],IrCrC10[:,1], 'k', linestyle='solid', label='IrCrC')
ax2.plot(IrCrB4C10[:,0],IrCrB4C10[:,1], 'magenta', linestyle='solid', label='IrCrB4C')

tick_pos = np.arange(0,5001,100)
ax2.xaxis.set_ticks(tick_pos)
ax2.set_xticklabels(ax2.get_xticks(), rotation = 90)

start, end = ax2.get_ylim()
tick_pos = np.array([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
ax2.yaxis.set_ticks(tick_pos)
ax2.set_yticklabels(ax2.get_yticks())
ax2.grid(visible=True, which='both', axis='both')

ax2.legend()




plt.tight_layout()

plt.savefig('plot/coatings_1deg.pdf')
plt.show()


