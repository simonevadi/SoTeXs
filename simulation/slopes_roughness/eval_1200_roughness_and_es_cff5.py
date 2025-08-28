import os
import pandas as pd
import numpy as np

from slopes_helper import filter_df, filter_df_by_values
from slopes_helper import extract_and_plot, decorate_and_save_plot
import matplotlib.pyplot as plt


# 1200 l/mm grating
flux_simulation_folder07 = 'RAYPy_Simulation_1200_roughness_and_exit_slit_cff5' 

oe = 'DetectorAtFocus' + '_RawRaysOutgoing.csv'
all_sim = pd.read_csv(os.path.join(flux_simulation_folder07, oe))
all_sim = all_sim[all_sim['CPMU20.photonEnergy'] < 2200]
exit_slit = np.loadtxt(os.path.join(flux_simulation_folder07, 'input_param_ExitSlit_openingHeight.dat'))
# create eval folder
os.makedirs('plot/roughness', exist_ok=True)

# make sure exit slit is a list
exit_slit = exit_slit.tolist()

if type(exit_slit) is float:
    exit_slit = [exit_slit]

for es in exit_slit:
    el_dict = {
        'M1.roughnessCoating1':0.3,
        'PremirrorM2.roughnessCoating1':0.3,
        'PG.roughnessSubstrate':0.3,
        'M3.roughnessCoating1':0.3,
        'KB_ver.roughnessCoating1':0.3,
        'KB_hor.roughnessCoating1':0.3,
    }
    sim = all_sim[all_sim['ExitSlit.openingHeight'] == es]
    plot_folder = f'plot/roughness/SoTeXS-1200-slopes-es-{int(es*1000)}µm_cff5'
    os.makedirs(plot_folder, exist_ok=True)
    fig, (axs) = plt.subplots(4, 1,figsize=(12,12))

    # No Slopes Errors
    filtered_sim = filter_df(sim, cols=list(el_dict.keys()))
    extract_and_plot(filtered_sim, axs, label='No Slopes Errors')

    # elemets
    # for element,slope in el_dict.items():
    #     filtered_sim = filter_df(sim, cols=list(el_dict.keys()), col_to_set=element, value=slope)
    #     extract_and_plot(filtered_sim, axs, label=f'{element} {slope} rms')

    # worst case
    filtered_sim = filter_df_by_values(sim, el_dict, cols=list(el_dict.keys()))
    extract_and_plot(filtered_sim, axs, label=f'All roughness')

    decorate_and_save_plot(axs, title=f'SoTeXS, ES={np.round(es*1000, 0)} µm', 
                        savepath=os.path.join(plot_folder, f'SoTeXS-1200-roughness-ES_{np.round(es*1000, 0)} µm.png'), 
                        showplot=False)

    # Each element separately
    base_dir = flux_simulation_folder07
    files = {
        'M1.roughnessCoating1': 'input_param_M1_roughnessCoating1.dat',
        'PremirrorM2.roughnessCoating1': 'input_param_PremirrorM2_roughnessCoating1.dat',
        'PG.roughnessSubstrate': 'input_param_PG_roughnessSubstrate.dat',
        'M3.roughnessCoating1': 'input_param_M3_roughnessCoating1.dat',
        'KB_ver.roughnessCoating1': 'input_param_KB_ver_roughnessCoating1.dat',
        'KB_hor.roughnessCoating1': 'input_param_KB_hor_roughnessCoating1.dat',
    }

    el_dict = {}
    for key, fname in files.items():
        file_path = os.path.join(base_dir, fname)
        data = np.loadtxt(file_path)
        filtered_data = np.unique(data[data != 0])
        el_dict[key] = filtered_data
        
    for element,slopes in el_dict.items():
        fig, (axs) = plt.subplots(4, 1,figsize=(12,12))
        # No Slopes Errors
        filtered_sim = filter_df(sim, cols=list(el_dict.keys()))
        extract_and_plot(filtered_sim, axs, label='No roughness Errors')
        print(slopes[:-1])
        for slope in slopes[:-1]:
            filtered_sim = filter_df(sim, 
                                    cols=list(el_dict.keys()), 
                                    col_to_set=element, 
                                    value=slope)
            extract_and_plot(filtered_sim, axs, label=f'{element} {np.round(slope,2)} rms')

        title = f"SoTeXS, {element.split('.')[0]} {element.split('.')[1]} roughness, ES={int(es*1000)}nm"
        decorate_and_save_plot(axs, title=title, 
                            savepath=os.path.join(plot_folder, f'SoTeXS-1200-roughness-{element}-ES_{np.round(es*1000, 0)} µm.png'), 
                            showplot=False)


