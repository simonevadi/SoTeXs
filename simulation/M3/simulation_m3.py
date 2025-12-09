from raypyng import Simulate

from params import sotexs_1200_file_path as rml_file
from params import sotexs_1200_sim_name as sim_name
from params import undulator_spectra as undulator
from params import nrays
from params import energy, rounds, ncpu, m3_radius
from params import exit_slit_height

sim = Simulate(rml_file, hide=True)

rml=sim.rml
beamline = sim.rml.beamline

# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.CPMU20.photonEnergy:energy},
            {beamline.CPMU20.energySpread:0},
            {beamline.CPMU20.numberRays:nrays},
            {beamline.M3.radius: m3_radius},
            {beamline.ExitSlit.openingHeight:exit_slit_height},  
        ]

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = sim_name

# repeat the simulations as many time as needed
sim.repeat = rounds

sim.analyze = False # don't let RAY-UI analyze the results
sim.raypyng_analysis=True # let raypyng analyze the results

sim.reflectivity(False)

sim.undulator_table=undulator

## This must be a list of dictionaries
# sim.exports  =  [{beamline.DetectorAtExitSlit:['RawRaysOutgoing']}]
sim.exports  =  [{beamline.ExitSlit:['RawRaysIncoming']}]

#uncomment to run the simulations
# sim.run(multiprocessing=ncpu, force=False, remove_rawrays=True, remove_round_folders=True)
sim.run(multiprocessing=ncpu, force=False, remove_rawrays=True, remove_round_folders=True)
