import pandas as pd
import numpy as np
from raypyng import Simulate

# define the values of the parameters to scan 
from params import hb_1200_order as order
from params import hb_1200_cff as cff
from params import ncpu
from slopes_helper import make_slopes_params

sim = Simulate('rml/sotexs_1200_Pt.rml', hide=True)

rml=sim.rml
beamline = sim.rml.beamline

energy = np.arange(500, 2000.1, 250)    
rounds = 50
nrays  = 4e5

slopes = {
    beamline.M1.roughnessCoating1:  (np.array([0.1, 0.3, 0.5, 1.5]), 0.3),
    beamline.PremirrorM2.roughnessCoating1: (np.array([0.1, 0.3, 0.5, 1.5]), 0.3),
    beamline.PG.roughnessSubstrate: (np.array([0.1, 0.3, 0.5, 1.5]), 0.3),
    beamline.M3.roughnessCoating1: (np.array([0.1, 0.3, 0.5, 1.5]), 0.3),
    beamline.KB_ver.roughnessCoating1: (np.array([0.1, 0.3, 0.5, 1.5]), 0.3),
    beamline.KB_hor.roughnessCoating1: (np.array([0.1, 0.3, 0.5, 1.5]), 0.3),
}
slopes_dict = make_slopes_params(slopes)
# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.ExitSlit.openingHeight:[0.01]},
            {beamline.CPMU20.photonEnergy:energy},
            {beamline.PG.cFactor:5}, 
            {beamline.PG.orderDiffraction:order},
            {beamline.CPMU20.numberRays:nrays}, 
        ]

params.append(slopes_dict)  # append the slopes dictionary to the list of parameters

# import the parameters into the simulation
#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = '1200_roughness_and_exit_slit_cff5'

# turn off reflectivity
sim.reflectivity(False)

# repeat the simulations as many time as needed
sim.repeat = rounds

sim.analyze = False # let RAY-UI analyze the results
sim.raypyng_analysis = True # let RAY-UI analyze the results
## This must be a list of dictionaries
sim.exports  =  [{beamline.DetectorAtFocus:['RawRaysOutgoing']}]

undulator_table = pd.read_csv('undulator/CPMU20.csv')
sim.undulator_table = undulator_table


#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False, remove_round_folders=True, remove_rawrays=True)