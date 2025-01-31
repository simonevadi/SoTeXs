from raypyng import Simulate
from multilayer_helper import AndreyML

# define the values of the parameters to scan 
from params import ml_order as order,  ml_energy_flux as energy
from params import ml_SlitSize as SlitSize, ml_grating as grating 
from params import ml_index as index, ml_table
from params import ml_nrays_flux as nrays, ml_rounds_flux as rounds
from params import ml_ncpu_flux as ncpu, ml_sim_name_flux as sim_name
from params import ml_rml_file_path, ml_cff as cff

sim = Simulate(ml_rml_file_path, hide=True)

rml=sim.rml
beamline = sim.rml.beamline
# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.ExitSlit.totalHeight:SlitSize},
            {beamline.CPMU20.photonEnergy:energy, 
             beamline.PG.cFactor:cff}, 
            {beamline.PG.orderDiffraction:order},
            {beamline.CPMU20.numberRays:nrays}, 
        ]

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = sim_name

# turn off reflectivity
# sim.reflectivity(reflectivity=True)

# repeat the simulations as many time as needed
sim.repeat = rounds

sim.analyze = False # let RAY-UI analyze the results
sim.raypyng_analysis = True # let RAY-UI analyze the results

## This must be a list of dictionaries
sim.exports  =  [{beamline.CPMU20:['RawRaysOutgoing']},
                 {beamline.DetectorAtFocus:['RawRaysOutgoing']}]


# create the rml files
#sim.rml_list()

#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False)
