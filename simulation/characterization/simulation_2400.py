import pandas as pd

from raypyng import Simulate

# define the values of the parameters to scan 
from params import ml_order as order,  ml_energy as energy
from params import ml_SlitSize as SlitSize
from params import ml_nrays as nrays, rounds_ml as rounds
from params import ncpu
from params import ml_cff as cff
from params import efficiency

sim = Simulate('rml/sotexs_2400.rml', hide=True)

rml=sim.rml
beamline = sim.rml.beamline
# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.ExitSlit.openingHeight:SlitSize},
            {beamline.CPMU20.photonEnergy:energy, 
             beamline.PG.cFactor:cff}, 
            {beamline.PG.orderDiffraction:order},
            {beamline.CPMU20.numberRays:nrays}, 
        ]

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = '2400'

# turn off reflectivity
# sim.reflectivity(reflectivity=True)

# repeat the simulations as many time as needed
sim.repeat = rounds

sim.analyze = False # let RAY-UI analyze the results
sim.raypyng_analysis = True # let RAY-UI analyze the results

## This must be a list of dictionaries
sim.exports  =  [{beamline.DetectorAtFocus:['RawRaysOutgoing']}]

undulator_table = pd.read_csv('undulator/CPMU20.csv')
sim.undulator_table = undulator_table

sim.efficiency = efficiency

# create the rml files
#sim.rml_list()

#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False, remove_round_folders=False, remove_rawrays=True)