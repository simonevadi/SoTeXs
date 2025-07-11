import matplotlib.pyplot as plt
import pandas as pd

def make_slopes_params(param_dict):
    new_dict = {}
    for key, value in param_dict.items():
        new_dict[key] = [0]
        new_dict[key].append(value[1])  # single value for the parameter
    for key,value_tuple in param_dict.items():
        values = value_tuple[0]
        for value in values:
            for new_key in new_dict.keys():
                if new_key == key:
                    new_dict[new_key].append(value)
                else:
                    new_dict[new_key].append(0)     
    return new_dict

def filter_df(df, cols=None, col_to_set=None, value=None):
    mask = (df[cols] == 0)
    if col_to_set is not None and value is not None and col_to_set in cols:
        mask[col_to_set] = (df[col_to_set] == value)
    filtered_df = df[mask.all(axis=1)]
    return filtered_df

def filter_df_by_values(df, col_values, cols=None, atol=1e-8, debug=False):
    """
    Filter the DataFrame by specifying a dictionary of {column: value} pairs.
    Uses np.isclose for float comparisons.
    If debug=True, prints matching info for each column.
    """

    mask = pd.Series([True] * len(df), index=df.index)
    if debug:
        print("DEBUG: Unique values and matches per column:")
    for col, val in col_values.items():
        count = (df[col] == val).sum()
        df = df[df[col] == val]
        if debug:
            print(f"{col} looking for {val} | found: {count} matches")
    if debug:
        print(f"DEBUG: Final number of matching rows: {mask.sum()}")
    return df

def extract_and_plot(dataframe, axs, label):
    energy = dataframe['CPMU20.photonEnergy']
    abs_flux = dataframe['PhotonFlux1']
    bw = dataframe['Bandwidth']
    vfoc = dataframe['VerticalFocusFWHM']*1000  # convert to um
    hfoc = dataframe['HorizontalFocusFWHM']*1000  # convert to um
    axs[0].plot(energy,bw, label=f'{label}')
    axs[1].plot(energy,energy/bw, label=f'{label}')
    axs[2].plot(energy,hfoc, label=f'{label}')
    axs[3].plot(energy,vfoc, label=f'{label}')

def decorate_and_save_plot(axs, title=None, savepath=None, showplot=False):

    # BANDWIDTH
    ax = axs[0]
    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Transmitted Bandwidth [eV]')
    ax.set_title('Transmitted bandwidth (tbw)')
    ax.grid(which='both', axis='both')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # BANDWIDTH
    ax = axs[1]
    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Resolving Power [a.u.]')
    ax.set_title('Resolving Power')
    ax.grid(which='both', axis='both')

    # HORIZONTAL FOCUS
    ax = axs[2]
    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Focus Size [um]')
    ax.set_title('Horizontal focus')
    ax.grid(which='both', axis='both')
    # ax.set_ylim(4, 16)


    # VERTICAL FOCUS
    ax = axs[3]
    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Focus Size [um]')
    ax.set_title('Vertical focus')
    ax.grid(which='both', axis='both')
    # ax.set_ylim(4, 16)

    plt.suptitle(title)
    plt.tight_layout()
    plt.savefig(savepath)
    if showplot:
        plt.show()
    plt.close()


