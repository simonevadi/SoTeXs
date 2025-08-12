import numpy as np

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




