import pandas as pd
import numpy as np
from raypyng import Simulate

# define the values of the parameters to scan 
from params import hb_1200_order as order
from params import hb_1200_SlitSize as SlitSize
from params import hb_1200_cff as cff
from params import ncpu

sim = Simulate('rml/sotexs_1200_07.rml', hide=True)

rml=sim.rml
beamline = sim.rml.beamline

energy = np.arange(500, 2000.1, 500)    
rounds = 20
nrays  = 1e5
# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.ExitSlit.openingHeight:SlitSize},
            {beamline.CPMU20.photonEnergy:energy},
            {beamline.PG.cFactor:cff}, 
            {beamline.PG.orderDiffraction:order},
            {beamline.CPMU20.numberRays:nrays}, 
            {beamline.M1.slopeErrorMer:[1, 0.5, 0]}, 
            {beamline.PremirrorM2.slopeErrorMer:[0.2, 0.05, 0]}, 
            {beamline.PG.slopeErrorMer:[0.2, 0.05, 0]}, 
            {beamline.M3.slopeErrorSag:[2, 1, 0.5, 0]}, 
            {beamline.KB_ver.slopeErrorMer:[0.2, 0.05, 0]}, 
            {beamline.KB_hor.slopeErrorMer:[0.2, 0.05, 0]}, 
        ]

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = '1200_slopes'

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
sim.run(multiprocessing=ncpu, force=False, remove_round_folders=True, remove_rawrays=True)