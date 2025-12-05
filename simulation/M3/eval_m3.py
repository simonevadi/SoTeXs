import os
import matplotlib.pyplot as plt
import pandas as pd


from raypyng.postprocessing import PostProcessAnalyzed

from params import energy as energies_list
from params import sotexs_1200_sim_name
p = PostProcessAnalyzed()
mov_av = p.moving_average
##############################################################
# LOAD IN DATA

# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join(f'RAYPy_Simulation_{sotexs_1200_sim_name}', 'ExitSlit_RawRaysIncoming.csv')
BL_df_all = pd.read_csv(BL_file_path)

##############################################################
# PLOTTING AND ANALYSIS
# Create the Main figure
plt.rcParams.update({"font.size": 20})
fig, (axs) = plt.subplots(1, 1, figsize=(20, 15))
fig.suptitle(f'M3 radius and focus Size at Exit Slit @{energies_list} eV')

# Vertical Focus Size
for energy in energies_list:
    BL_df = BL_df_all[BL_df_all['CPMU20.photonEnergy']==energy]
    axs.plot(BL_df['M3.radius'],
            BL_df['VerticalFocusFWHM'],
            label=f'Energy={energy} eV',
            )

axs.set_title('Vertical Focus Size')
axs.set_xlabel('Radius [mm]')
axs.set_ylabel('[µm]')
axs.legend()
axs.minorticks_on()
axs.grid(which='both')


##############################################################
# SAVING
# Ensure the "plot" folder exists
plot_folder = 'plot'
if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)

# Save the the figure
plt.tight_layout()
plt.savefig('plot/sotexs_M3_radius.png')
# plt.show()
