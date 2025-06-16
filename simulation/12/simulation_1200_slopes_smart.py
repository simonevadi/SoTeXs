import pandas as pd
import numpy as np
from raypyng import Simulate

# define the values of the parameters to scan 
from params import hb_1200_order as order
from params import hb_1200_SlitSize as SlitSize
from params import hb_1200_cff as cff
from params import ncpu
from build_params import make_slopes_params

sim = Simulate('rml/sotexs_1200_07.rml', hide=True)

rml=sim.rml
beamline = sim.rml.beamline

energy = np.arange(500, 2000.1, 1500)    
rounds = 1
nrays  = 2e5

slopes = {beamline.M1.slopeErrorMer:  np.arange(0.3,1.1, 0.1), 
            beamline.M1.slopeErrorSag:np.arange(1.5, 2.1, 0.1), 
            beamline.PremirrorM2.slopeErrorMer:np.arange(0.05, 0.2, 0.05), 
            beamline.PremirrorM2.slopeErrorSag:np.arange(0.5, 1.1, 0.1),
            beamline.PG.slopeErrorMer:np.arange(0.05, 0.21, 0.05), 
            beamline.PG.slopeErrorSag:np.arange(0.5, 1.1, 0.1), 
            beamline.M3.slopeErrorSag:np.arange(0.5, 2.1, 0.5), 
            beamline.M3.slopeErrorMer:np.arange(0.3, 0.61, 0.3), 
            beamline.KB_ver.slopeErrorMer:np.arange(0.05, 2.1, 0.05), 
            beamline.KB_ver.slopeErrorSag:np.arange(0.1, 0.31, 0.1), 
            beamline.KB_hor.slopeErrorMer:np.arange(0.05, 2.1, 0.05), 
            beamline.KB_hor.slopeErrorSag:np.arange(0.1, 0.31, 0.1)
            }

slopes_dict = make_slopes_params(slopes)
# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.ExitSlit.openingHeight:SlitSize},
            {beamline.CPMU20.photonEnergy:energy},
            {beamline.PG.cFactor:cff}, 
            {beamline.PG.orderDiffraction:order},
            {beamline.CPMU20.numberRays:nrays}, 
        ]

params.append(slopes_dict)  # append the slopes dictionary to the list of parameters

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = '1200_slopes_smart'

# turn off reflectivity
sim.reflectivity(reflectivity=False)

# repeat the simulations as many time as needed
sim.repeat = rounds

sim.analyze = False # let RAY-UI analyze the results
sim.raypyng_analysis = True # let RAY-UI analyze the results
## This must be a list of dictionaries
sim.exports  =  [{beamline.DetectorAtFocus:['RawRaysOutgoing']}]

undulator_table = pd.read_csv('undulator/CPMU20.csv')
sim.undulator_table = undulator_table


#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False, remove_round_folders=False, remove_rawrays=False)