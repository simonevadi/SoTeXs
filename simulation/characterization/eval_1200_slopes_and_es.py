import os
import pandas as pd
import numpy as np

from slopes_helper import filter_df, filter_df_by_values
from slopes_helper import extract_and_plot, decorate_and_save_plot
import matplotlib.pyplot as plt


# 1200 l/mm grating
flux_simulation_folder07 = 'RAYPy_Simulation_1200_slopes_and_exit_slit' 

oe = 'DetectorAtFocus' + '_RawRaysOutgoing.csv'
all_sim = pd.read_csv(os.path.join(flux_simulation_folder07, oe))
all_sim = all_sim[all_sim['CPMU20.photonEnergy'] < 2200]
exit_slit = np.loadtxt(os.path.join(flux_simulation_folder07, 'input_param_ExitSlit_openingHeight.dat'))
# create eval folder
os.makedirs('plot/slopes', exist_ok=True)

# All Zeros but one


for es in exit_slit:
    el_dict = {
        'M1.slopeErrorMer':0.5,
        'M1.slopeErrorSag':1.5,
        'PremirrorM2.slopeErrorMer':0.05,
        'PremirrorM2.slopeErrorSag':0.5,
        'PG.slopeErrorMer':0.05,
        'PG.slopeErrorSag':0.5,
        'M3.slopeErrorSag':1,
        'M3.slopeErrorMer':0.3,
        'KB_ver.slopeErrorMer':0.05,
        'KB_ver.slopeErrorSag':0.1,
        'KB_hor.slopeErrorMer':0.05,
        'KB_hor.slopeErrorSag':0.1
    }
    sim = all_sim[all_sim['ExitSlit.openingHeight'] == es]
    plot_folder = f'plot/slopes/SoTeXS-1200-slopes-es-{int(es*1000)}µm'
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
    extract_and_plot(filtered_sim, axs, label=f'All Slopes Errors')

    decorate_and_save_plot(axs, title=f'SoTeXS, ES={np.round(es*1000, 0)} µm', 
                        savepath=os.path.join(plot_folder, f'SoTeXS-1200-slopes-ES_{np.round(es*1000, 0)} µm.png'), 
                        showplot=False)

    # Each element separately
    base_dir = 'RAYPy_Simulation_1200_slopes_and_exit_slit'
    files = {
        'M1.slopeErrorMer': 'input_param_M1_slopeErrorMer.dat',
        'M1.slopeErrorSag': 'input_param_M1_slopeErrorSag.dat',
        'PremirrorM2.slopeErrorMer': 'input_param_PremirrorM2_slopeErrorMer.dat',
        'PremirrorM2.slopeErrorSag': 'input_param_PremirrorM2_slopeErrorSag.dat',
        'PG.slopeErrorMer': 'input_param_PG_slopeErrorMer.dat',
        'PG.slopeErrorSag': 'input_param_PG_slopeErrorSag.dat',
        'M3.slopeErrorSag': 'input_param_M3_slopeErrorSag.dat',
        'M3.slopeErrorMer': 'input_param_M3_slopeErrorMer.dat',
        'KB_ver.slopeErrorMer': 'input_param_KB_ver_slopeErrorMer.dat',
        'KB_ver.slopeErrorSag': 'input_param_KB_ver_slopeErrorSag.dat',
        'KB_hor.slopeErrorMer': 'input_param_KB_hor_slopeErrorMer.dat',
        'KB_hor.slopeErrorSag': 'input_param_KB_hor_slopeErrorSag.dat'
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
        extract_and_plot(filtered_sim, axs, label='No Slopes Errors')

        for slope in slopes:
            filtered_sim = filter_df(sim, 
                                    cols=list(el_dict.keys()), 
                                    col_to_set=element, 
                                    value=slope)
            extract_and_plot(filtered_sim, axs, label=f'{element} {np.round(slope,2)} rms')

        title = f"SoTeXS, {element.split('.')[0]} {element.split('.')[1]} slope Error, ES={int(es*1000)}µm"
        decorate_and_save_plot(axs, title=title, 
                            savepath=os.path.join(plot_folder, f'SoTeXS-1200-slopes-{element}-ES_{np.round(es*1000, 0)} µm.png'), 
                            showplot=False)


