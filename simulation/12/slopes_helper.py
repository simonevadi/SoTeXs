import matplotlib.pyplot as plt


def filter_df(df, col_to_set=None, value=None):
    cols = [
        'M1.slopeErrorMer',
        'PremirrorM2.slopeErrorMer',
        'PG.slopeErrorMer',
        'M3.slopeErrorSag',
        'KB_ver.slopeErrorMer',
        'KB_hor.slopeErrorMer'
    ]

    mask = (df[cols] == 0)
    if col_to_set is not None and value is not None and col_to_set in cols:
        mask[col_to_set] = (df[col_to_set] == value)
    filtered_df = df[mask.all(axis=1)]
    return filtered_df

def extract_and_plot(dataframe, axs, label):
    energy = dataframe['CPMU20.photonEnergy']
    abs_flux = dataframe['PhotonFlux1']
    bw = dataframe['Bandwidth']
    vfoc = dataframe['VerticalFocusFWHM']*1000  # convert to um
    hfoc = dataframe['HorizontalFocusFWHM']*1000  # convert to um
    axs[0,0].plot(energy,abs_flux, label=f'{label}')
    axs[0,1].plot(energy,bw, label=f'{label}')
    axs[1,0].plot(energy,hfoc, label=f'{label}')
    axs[1,1].plot(energy,vfoc, label=f'{label}')

def decorate_and_save_plot(axs, title=None, savepath=None, showplot=False):
    

    # AVAILABLE/ABS FLUX 
    ax = axs[0,0]           
    ax.set_title('Available Flux')
    ax.set_xlabel(r'Energy [eV]')
    ax.grid(which='both', axis='both')
    ax.set_ylabel('Flux [ph/s/0.3A/tbw]')
    ax.set_yscale('log')
    ax.legend()

    # BANDWIDTH
    ax = axs[0,1]
    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Transmitted Bandwidth [eV]')
    ax.set_title('Transmitted bandwidth (tbw)')
    ax.grid(which='both', axis='both')


    # HORIZONTAL FOCUS
    ax = axs[1,0]
    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Focus Size [um]')
    ax.set_title('Horizontal focus')
    ax.set_ylim(4, 16)


    # VERTICAL FOCUS
    ax = axs[1,1]
    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Focus Size [um]')
    ax.set_title('Vertical focus')
    ax.set_ylim(4, 16)

    plt.suptitle(title)
    plt.tight_layout()
    plt.savefig(savepath)
    if showplot:
        plt.show()


