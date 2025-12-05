import os
import matplotlib.pyplot as plt
import pandas as pd


from raypyng.postprocessing import PostProcessAnalyzed

from params import sotexs_1200_cff_sim_name
from params import cff as cff_list
from params import m3_radius_cff as m3_radius_list

p = PostProcessAnalyzed()
mov_av = p.moving_average
##############################################################
# LOAD IN DATA

# Read CSV-File of the Beamline Simulation
BL_file_path = os.path.join(f'RAYPy_Simulation_{sotexs_1200_cff_sim_name}', 'ExitSlit_RawRaysOutgoing.csv')
BL_df_all_radii = pd.read_csv(BL_file_path)

##############################################################
# PLOTTING AND ANALYSIS
# Create the Main figure
for m3_radius in m3_radius_list:
    BL_df_all = BL_df_all_radii[BL_df_all_radii['M3.radius']==m3_radius]
    
    plt.rcParams.update({"font.size": 20})
    fig, (axs) = plt.subplots(2, 1, figsize=(20, 15))
    fig.suptitle(f'Transmitted Bandwidth vs Energy at different cFactors, M3 radius={m3_radius} mm')

    # Transmitted BW
    ax = axs[0]
    for cff in cff_list:
        BL_df = BL_df_all[BL_df_all['PG.cFactor']==cff]

        ax.plot(BL_df['PhotonEnergy'],
                BL_df['Bandwidth'],
                label=f'cFactor={cff}',
                )

    ax.set_title('Transmittted Bandwidth')
    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Transmittted Bandwidth [eV]')
    ax.legend()
    ax.minorticks_on()
    ax.grid(which='both')


    # Flux
    ax = axs[1]
    for cff in cff_list:
        BL_df = BL_df_all[BL_df_all['PG.cFactor']==cff]

        ax.plot(BL_df['PhotonEnergy'],
                BL_df['PhotonFlux1'],
                label=f'cFactor={cff}',
                )

    ax.set_title('Photon Flux')
    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Photon Flux [ph/s/0.3A/tbw]')
    ax.legend()
    ax.minorticks_on()
    ax.grid(which='both')


    ##############################################################
    # SAVING
    # Ensure the "plot" folder exists
    plot_folder = 'plot'
    if not os.path.exists(plot_folder):
        os.makedirs(plot_folder)

    # Save the the figure
    plt.tight_layout()
    plt.savefig(f'plot/sotexs_cff_m3radius{m3_radius}.png')
    # plt.show()
