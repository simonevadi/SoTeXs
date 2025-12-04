import os
import matplotlib.pyplot as plt
import pandas as pd


from raypyng.postprocessing import PostProcessAnalyzed

from params import energy

p = PostProcessAnalyzed()
mov_av = p.moving_average
##############################################################
# LOAD IN DATA

# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join('RAYPy_Simulation_sotexs_1200_Pt', 'ExitSlit_RawRaysIncoming.csv')
BL_df = pd.read_csv(BL_file_path)

##############################################################
# PLOTTING AND ANALYSIS
# Create the Main figure
plt.rcParams.update({"font.size": 20})
fig, (axs) = plt.subplots(1, 1, figsize=(20, 15))
fig.suptitle(f'M3 radius and focus Size at Exit Slit @{energy} eV', size=16)

# Vertical Focus Size
axs.plot(BL_df['M3.radius'],
        BL_df['VerticalFocusFWHM'],
        )

axs.set_title('Vertical Focus Size')
axs.set_xlabel('Radius [mm]')
axs.set_ylabel('[µm]')
axs.legend()
axs.minorticks_on()
axs.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='lightgrey')


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
