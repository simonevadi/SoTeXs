import numpy as np
import pandas as pd
import os 

#### XRT
def get_reflectivity(material,E,theta):
    """Calculate the reflectivity for a given material at
    a certain incident angle theta for a given energy range E

    Args:
        material (XRT material): A material defined in XRT
        E (np.array): the desidered energy range
        theta (float): the grazing incidence angle

    Returns:
        rs,rp: reflectivity fr the s and p polarization
    """    
    theta = np.deg2rad(theta)
    rs, rp = material.get_amplitude(E, np.sin(theta))[0:2]
    return abs(rs)**2, abs(rp)**2


### UNDULATOR
def scale_undulator_flux(ray_energy, ray_flux, undulator_spectra):
    """Takes as input the flux points in percentage at defined energy points and
    returns the absolute flux. Performs interpolation if needed.

    Args:
        ray_energy (np.array): array of energy
        ray_flux (np.array): array of flux
        undulator_file (str): the filename and location of the undulator flux file

    Returns:
        absolute_flux (np.array): the absolute flux
    """    
    breakpoint()
    en_undulator    = undulator_spectra[:,0]
    flux_undulator  = undulator_spectra[:,3]
    und_interp_flux = np.interp(ray_energy, en_undulator, flux_undulator) 

    return ray_flux*und_interp_flux/100 

def order(unordered):
    ordered = []
    for i in range(5):
        for v in range(10):
            ordered.append(unordered[int(i+v*5)])
    return np.array(ordered)





def combine_simulations_results(sim_folder, oe):
    """
    Combines simulation results from two data sources into a single DataFrame.

    This function reads two datasets: one CSV file named 'looper.csv' and another
    data file specific to an optical element (OE) with tab-separated values. It merges these
    datasets by concatenating them column-wise.

    Args:
        sim_folder (str): The directory path where the simulation files are stored.
        oe (str): The name of the optical element, used to construct the filename for the OE's data.

    Returns:
        pd.DataFrame: A DataFrame that combines data from 'looper.csv' and the OE-specific data file.

    Raises:
        FileNotFoundError: If 'looper.csv' or the OE-specific file does not exist in the directory.
    """
    looper_path = os.path.join(sim_folder, 'looper.csv')
    oe_path = os.path.join(sim_folder, oe + '_RawRaysOutgoing.dat')
    
    # Check if the files exist before attempting to read them
    if not os.path.exists(looper_path):
        raise FileNotFoundError(f"The file 'looper.csv' does not exist in the directory '{sim_folder}'.")
    if not os.path.exists(oe_path):
        raise FileNotFoundError(f"The file '{oe}_RawRaysOutgoing.dat' does not exist in the directory '{sim_folder}'.")

    looper = pd.read_csv(looper_path)
    # Reading the data into a DataFrame, specify no comment handling and read headers normally
    res = pd.read_csv(oe_path, sep="\t", comment=None, header=0)
    # Manually remove the '#' from the first column name
    res.columns = [col.replace('#', '').strip() for col in res.columns]
    res_combined = pd.concat([looper, res], axis=1)
    
    return res_combined

def moving_average(data, window_size):
    """
    Computes the moving average of the given data using a specified window size.

    :param data: np.array, the data array on which to compute the moving average.
    :param window_size: int, the size of the moving window.
    :return: np.array, the moving average of the data.
    """
    if window_size <= 0:
        raise ValueError("Window size must be positive")

    # Ensure that window_size is an integer
    window_size = int(window_size)

    # Use numpy's convolution function to compute the moving average
    weights = np.ones(window_size) / window_size
    return np.convolve(data, weights, mode='valid') 
