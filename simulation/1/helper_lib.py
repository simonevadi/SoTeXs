import numpy as np
import pandas as pd

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
def scale_undulator_flux(ray_energy, ray_flux, undulator_file):
    """Takes as input the flux points in percentage at defined energy points and
    returns the absolute flux. Performs interpolation if needed.

    Args:
        ray_energy (np.array): array of energy
        ray_flux (np.array): array of flux
        undulator_file (str): the filename and location of the undulator flux file

    Returns:
        absolute_flux (np.array): the absolute flux
    """    
    undulator       = np.loadtxt(undulator_file,skiprows=8)
    en_undulator    = undulator[:,0]
    flux_undulator  = undulator[:,3]
    und_interp_flux = np.interp(ray_energy, en_undulator, flux_undulator) 

    return ray_flux*und_interp_flux/100 

def order(unordered):
    ordered = []
    for i in range(5):
        for v in range(10):
            ordered.append(unordered[int(i+v*5)])
    return np.array(ordered)