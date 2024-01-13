import numpy as np
import matplotlib.pyplot as plt

Pt10=np.loadtxt('reflectivity/pt_1.0.dat', skiprows=2)
Pt12=np.loadtxt('reflectivity/pt_1.2.dat', skiprows=2)

Pd10=np.loadtxt('reflectivity/pd_1.0.dat', skiprows=2)
Pd12=np.loadtxt('reflectivity/pd_1.2.dat', skiprows=2)

PtPd10=np.loadtxt('reflectivity/ptpd_1.0.dat', skiprows=2)
PtPd12=np.loadtxt('reflectivity/ptpd_1.2.dat', skiprows=2)

IrCrC10=np.loadtxt('reflectivity/ircrc_1.0.dat', skiprows=2)
IrCrC12=np.loadtxt('reflectivity/ircrc_1.2.dat', skiprows=2)

IrCrB4C10=np.loadtxt('reflectivity/ircrb4c_1.0.dat', skiprows=2)
IrCrB4C12=np.loadtxt('reflectivity/ircrb4c_1.2.dat', skiprows=2)

PtCrB4C10=np.loadtxt('reflectivity/ptcrb4c_1.0.dat', skiprows=2)
PtCrB4C12=np.loadtxt('reflectivity/ptcrb4c_1.2.dat', skiprows=2)

IrNiB4C10=np.loadtxt('reflectivity/irnib4c_1.0.dat', skiprows=2)
IrNiB4C12=np.loadtxt('reflectivity/irnib4c_1.2.dat', skiprows=2)

Rh10=np.loadtxt('reflectivity/rh_1.0.dat', skiprows=2)
Rh12=np.loadtxt('reflectivity/rh_1.2.dat', skiprows=2)

IrCr10=np.loadtxt('reflectivity/ircr_1.0.dat', skiprows=2)


#plt.figure(10)
#plt.plot(Pt10[:,0],Pt10[:,1]**3*PtPd10[:,1]**2, 'r', linestyle = 'solid')
#plt.plot(Pt10[:,0],Pt10[:,1]**3*IrCr10[:,1]**2, 'r', linestyle = 'dashed')

#plt.plot(Pt10[:,0],PtPd10[:,1]**5, 'b', linestyle = 'solid')
#plt.plot(Pt10[:,0],IrCr10[:,1]**5, 'b', linestyle = 'dashed')

fig, (axs) = plt.subplots(2, 2,figsize=(10,10))


# 1.0 degree 
ax2=axs[0,0]
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

ax2.set_title('Comparison different coatings at 1.0°')
ax2.legend()


# 1.0 degree best candidates
ax2=axs[0,1]
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.set_title('Most promising candidates at 1.0°')
ax2.plot(Rh10[:,0],Rh10[:,1], 'r', linestyle='solid', label='Rh')
ax2.plot(PtPd10[:,0],PtPd10[:,1], 'violet', linestyle='solid', label='PtPd')
ax2.plot(IrCrC10[:,0],IrCrC10[:,1], 'k', linestyle='solid', label='IrCrC')
ax2.plot(IrCrB4C10[:,0],IrCrB4C10[:,1], 'magenta', linestyle='solid', label='IrCrB4C')

ax2.legend()




# 1.2 degree
ax2=axs[1,0]
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.plot(Pt12[:,0],Pt12[:,1], 'b', linestyle='solid', label='Pt')

ax2.plot(Rh12[:,0],Rh12[:,1], 'r', linestyle='solid', label='Rh')

ax2.plot(Pd12[:,0],Pd12[:,1], 'g', linestyle='solid', label='Pd')

ax2.plot(PtPd12[:,0],PtPd12[:,1], 'violet', linestyle='solid', label='PtPd')

ax2.plot(IrCrC12[:,0],IrCrC12[:,1], 'k', linestyle='solid', label='IrCrC')

ax2.plot(IrCrB4C12[:,0],IrCrB4C12[:,1], 'magenta', linestyle='solid', label='IrCrB4C')

ax2.plot(IrNiB4C12[:,0],IrNiB4C12[:,1], 'pink', linestyle='solid', label='IrNiB4C')

ax2.plot(PtCrB4C12[:,0],PtCrB4C12[:,1], 'lightblue', linestyle='solid', label='PtCrB4C')

ax2.set_title('Comparison different coatings at 1.2°')
ax2.legend()






# 1.2 degree best candidates
ax2=axs[1,1]
ax2.set_xlabel('Energy [eV]')
ax2.set_ylabel('Reflectivity [a.u.]')
ax2.plot(Rh12[:,0],Rh12[:,1], 'r', linestyle='solid', label='Rh')

ax2.plot(PtPd12[:,0],PtPd12[:,1], 'violet', linestyle='solid', label='PtPd')

ax2.plot(IrCrC12[:,0],IrCrC12[:,1], 'k', linestyle='solid', label='IrCrC')

ax2.plot(IrCrB4C12[:,0],IrCrB4C12[:,1], 'magenta', linestyle='solid', label='IrCrB4C')

ax2.set_title('Most promising candidates at 1.2°')
ax2.legend()


plt.tight_layout()

plt.savefig('plot/coatings.pdf')
plt.show()

#fig2 = plt.figure(3,figsize=(10,10))
#plt.suptitle('Reflectivity of different coatings at 1.5°', y=1.0)
#plt.tight_layout()
#ax2 = fig2.add_subplot(221)
#ax2.set_xlabel('Energy [eV]')
#ax2.set_ylabel('Reflectivity [a.u.]')
#ax2.plot(Au15[:,0],Au15[:,1], linestyle='solid', label='Au')
#ax2.plot(Pt15[:,0],Pt15[:,1], linestyle='solid', label='Pt')
#ax2.plot(Rh15[:,0],Rh15[:,1], linestyle='solid', label='Rh')
#ax2.plot(Pd15[:,0],Pd15[:,1], linestyle='solid', label='Pd')
#ax2.plot(Rh30_Pt8_15[:,0],Rh30_Pt8_15[:,1], linestyle='solid', label='Rh30 Pt8')
#ax2.plot(Au30_Pt8_15[:,0],Au30_Pt8_15[:,1], linestyle='solid', label='Au30 Pt8')
#plt.legend()
#plt.tight_layout()


## Major ticks every 20, minor ticks every 5
#minor_xticks = np.arange(0, 2501, 50)
#minor_yticks = np.arange(0, 1.1, 0.05)

##
#ax2 = fig2.add_subplot(222)
#ax2.set_xticks(minor_xticks, minor=True)
#ax2.set_yticks(minor_yticks, minor=True)
#ax2.set_xlabel('Energy [eV]')
#ax2.set_ylabel('Reflectivity [a.u.]')
##ax2.set_title('Reflectivity of different coatings at 1.5°')
#ax2.plot(Au15[:,0],Au15[:,1], linestyle='solid', label='Au')
#ax2.plot(Pt15[:,0],Pt15[:,1], linestyle='solid', label='Pt')
#ax2.plot(Rh15[:,0],Rh15[:,1], linestyle='solid', label='Rh')
#ax2.plot(Pd15[:,0],Pd15[:,1], linestyle='solid', label='Pd')
#ax2.plot(Rh30_Pt8_15[:,0],Rh30_Pt8_15[:,1], linestyle='solid', label='Rh30 Pt8')
#ax2.plot(Au30_Pt8_15[:,0],Au30_Pt8_15[:,1], linestyle='solid', label='Au30 Pt8')
#ax2.grid(linestyle='-', which='both',linewidth=0.5, alpha=0.2)
#ax2.set_xlim(0,300)
#ax2.set_ylim(0.7,1)
#plt.tight_layout()

#ax2 = fig2.add_subplot(223)
#ax2.set_xticks(minor_xticks, minor=True)
#ax2.set_yticks(minor_yticks, minor=True)
#ax2.set_xlabel('Energy [eV]')
#ax2.set_ylabel('Reflectivity [a.u.]')
##ax2.set_title('Reflectivity of different coatings at 1.5°')
#ax2.plot(Au15[:,0],Au15[:,1], linestyle='solid', label='Au')
#ax2.plot(Pt15[:,0],Pt15[:,1], linestyle='solid', label='Pt')
#ax2.plot(Rh15[:,0],Rh15[:,1], linestyle='solid', label='Rh')
#ax2.plot(Pd15[:,0],Pd15[:,1], linestyle='solid', label='Pd')
#ax2.plot(Rh30_Pt8_15[:,0],Rh30_Pt8_15[:,1], linestyle='solid', label='Rh30 Pt8')
#ax2.plot(Au30_Pt8_15[:,0],Au30_Pt8_15[:,1], linestyle='solid', label='Au30 Pt8')
#ax2.grid(linestyle='-', which='both',linewidth=0.5)
#ax2.set_xlim(0,900)
#ax2.set_ylim(0.4,1)
#plt.tight_layout()

#ax2 = fig2.add_subplot(224)
#ax2.set_xlabel('Energy [eV]')
#ax2.set_ylabel('Reflectivity [a.u.]')
#ax2.set_xticks(minor_xticks, minor=True)
#ax2.set_yticks(minor_yticks, minor=True)
##ax2.set_title('Reflectivity of different coatings at 1.5°')
#ax2.plot(Au15[:,0],Au15[:,1], linestyle='solid', label='Au')
#ax2.plot(Pt15[:,0],Pt15[:,1], linestyle='solid', label='Pt')
#ax2.plot(Rh15[:,0],Rh15[:,1], linestyle='solid', label='Rh')
#ax2.plot(Pd15[:,0],Pd15[:,1], linestyle='solid', label='Pd')
#ax2.plot(Rh30_Pt8_15[:,0],Rh30_Pt8_15[:,1], linestyle='solid', label='Rh30 Pt8')
#ax2.plot(Au30_Pt8_15[:,0],Au30_Pt8_15[:,1], linestyle='solid', label='Au30 Pt8')
#ax2.grid(linestyle='-', which='both',linewidth=0.5)
#ax2.set_xlim(1700,2500)
#ax2.set_ylim(0,0.8)
#plt.tight_layout()

#plt.savefig('plot/reflectivity_at_15.png') 

#plt.show()
