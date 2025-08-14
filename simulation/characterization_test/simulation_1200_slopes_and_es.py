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
rounds = 100
nrays  = 2e5

slopes = {
    beamline.M1.slopeErrorMer:  (np.array([0.2, 0.5, 0.7, 2]), 0.5),
    beamline.M1.slopeErrorSag: (np.array([1.0, 1.5, 2.0, 5]), 1.5),
    beamline.PremirrorM2.slopeErrorMer: (np.array([0.03, 0.05, 0.07, 1.5]), 0.05),
    beamline.PremirrorM2.slopeErrorSag: (np.array([0.3, 0.5, 0.7, 2]), 0.5),
    beamline.PG.slopeErrorMer: (np.array([0.03, 0.05, 0.07, 1.5]), 0.05),
    beamline.PG.slopeErrorSag: (np.array([0.3, 0.5, 0.7, 2]), 0.5),
    beamline.M3.slopeErrorSag: (np.array([0.5, 1.0, 1.5, 4]), 1.0),
    beamline.M3.slopeErrorMer: (np.array([0.1, 0.3, 0.5, 4]), 0.3),
    beamline.KB_ver.slopeErrorMer: (np.array([0.03, 0.05, 0.07, 0.2]), 0.05),
    beamline.KB_ver.slopeErrorSag: (np.array([0.05, 0.1, 0.15, 0.5]), 0.1),
    beamline.KB_hor.slopeErrorMer: (np.array([0.03, 0.05,0.07]), 0.05),
    beamline.KB_hor.slopeErrorSag: (np.array([0.05, 0.1, 0.15, 0.5]), 0.1)
}
slopes_dict = make_slopes_params(slopes)
# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.ExitSlit.openingHeight:[0.03,0.02,0.01]},
            {beamline.CPMU20.photonEnergy:energy},
            {beamline.PG.cFactor:cff}, 
            {beamline.PG.orderDiffraction:order},
            {beamline.CPMU20.numberRays:nrays}, 
        ]

params.append(slopes_dict)  # append the slopes dictionary to the list of parameters

# import the parameters into the simulation
#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = '1200_slopes_and_exit_slit'

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