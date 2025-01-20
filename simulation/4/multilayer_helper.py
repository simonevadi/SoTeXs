import numpy as np
import pandas as pd

class AndreyML:
    def __init__(self, excel_file_name=None):
        """Initialize AndreyML class instance.

        Args:
            excel_file_name (str, optional): Name of the Excel file to read data from. Defaults to None.
        """
        
        self.excel_file_name = excel_file_name
        

        self.ind_dict = {'MLBG_mfm_first':0,
                    'MLBG_mrm_first':1,
                    'MLBG_mfm_second':2,
                    'MLBG_mrm_second':3,
                    'MLBG_mfm_fourth':4,
                    'MLBG_mrm_fourth':5,
                    'MLLG_mfm_first':6,
                    'MLLG_mrm_first':7}

    def get_cff_for_ML(self, ind: str = 'MLBG_mfm_first', order: int = 2,
                       energy: np.ndarray = np.arange(500, 5001, 500),
                       verbose: bool = False) -> np.ndarray:
        """Get cff for the multilayer depending on the energy.

        Args:
            ind (str, optional): Identifier of the correction factor. Defaults to 'MLBG_mfm_first'.
            order (int, optional): Diffraction order. Defaults to 2.
            energy (np.ndarray, optional): Array of energy values to interpolate the cff for. Defaults to np.arange(500, 5001, 500).
            verbose (bool, optional): Whether to print the energy, alpha, beta, and cff values. Defaults to False.

        Returns:
            np.ndarray: Array of cff values interpolated for the input energy values.
        """        
        ind          = self.ind_dict[ind]
        ml_pandas    = pd.read_excel(self.excel_file_name, header=(0,1,2,3))
        ml           = np.array(ml_pandas)
        energy_ml    = ml[:,0+10*ind]
        alpha        = 90-ml[:,1+10*ind]
        beta         = -(90-ml[:,2+10*ind])
        theta        = ml[:,4+10*ind]

        alpha_radians = np.deg2rad(alpha)
        beta_radians  = np.deg2rad(beta)

        alpha_cos = np.cos(alpha_radians)
        beta_cos = np.cos(beta_radians)

        cff = beta_cos/alpha_cos

        if verbose:
            for i in range(energy_ml.shape[0]):
                print('en', energy_ml[i], 'alpha', alpha[i], 'beta', beta[i], 'cff', cff[i])

        cff = np.interp(energy, energy_ml, cff)
        return cff
    
def ML_eff(ray_calc_eff, scale=None, ind=None, energy=None, grating_eff_file=None, verbose=False):
    """This function reads excel file that Andrey Sokolov
    produced. I basically counted the columns and made a dictionary to 
    index them.

    Args:
        ray_calc_eff (array): The efficency array as calculated by RAY-UI
        scale (float,int, optional): assume scale as the efficiency of both
         the mirror and ML grating . Defaults to None, in that case the efficency is
         read from the excel file of Andrey
        ind (str, optional): Which column to use in Andrey's file. Defaults to None.
        energy (np.array, optional): the enrgy range. Defaults to None.
        grating_eff_file (_type_, optional): _description_. Defaults to None.

    Returns:
        np.array: the efficiency scaled with the ML efficency
    """    
    # if scale exist we ignore the rest and just assume scale as
    # the efficiency of both the mirror and the ML grating
    if isinstance(scale, float) or isinstance(scale, int):
        ray_calc_eff = ray_calc_eff*scale*scale
        return ray_calc_eff
    # if scale is None, we read the efficiency from Andrey excel file
    ind_dict = {'MLBG_mfm_first':0,
                'MLBG_mrm_first':1,
                'MLBG_mfm_second':2,
                'MLBG_mrm_second':3,
                'MLBG_mfm_fourth':4,
                'MLBG_mrm_fourth':5,
                'MLLG_mfm_first':6,
                'MLLG_mrm_first':7}
    if ind == None:
        print('You did not select any index, I use ind=O, that corresponds to "MLBG_mfm_first"')
        ind = 0
    else:
        ind = ind_dict[ind]
    
    ml_pandas    = pd.read_excel(grating_eff_file, header=(0,1,2,3))
    ml           = np.array(ml_pandas)
    energy_ml    = ml[:,0+10*ind]
    grat         = ml[:,3+10*ind]
    m2           = ml[:,5+10*ind]
    de           = ml[:,6+10*ind]
    m2_eff       = np.interp(energy, energy_ml, m2)
    grat_eff     = np.interp(energy, energy_ml, grat)
    if verbose:
        print('###############')
        for ind,en in enumerate(energy):
            print(f'Energy: {en} eV, M2 eff.: {m2_eff[ind]}, Grating eff. {grat_eff[ind]}')
    ray_calc_eff = ray_calc_eff*m2_eff*grat_eff
    return ray_calc_eff

def extract_from_Andrey(table,column, ML_eff_file):
    ml_dict = {'MLBG_mfm_first':0,
                'MLBG_mrm_first':1,
                'MLBG_mfm_second':2,
                'MLBG_mrm_second':3,
                'MLBG_mfm_fourth':4,
                'MLBG_mrm_fourth':5,
                'MLLG_mfm_first':6,
                'MLLG_mrm_first':7}
    column_dict = {'energy':0,
               'alpha': 1,
               'beta': 2,
               'grat_eff': 3,
               'theta': 4,
               'mir_eff': 5,
               'dE': 6,
               'RP': 7,
               }
    ml_pandas    = pd.read_excel(ML_eff_file, header=(0,1,2,3))
    ml           = np.array(ml_pandas)
    return ml[:,column_dict[column]+ml_dict[table]*10]