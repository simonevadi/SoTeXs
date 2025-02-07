from raypyng import Simulate

# define the values of the parameters to scan 
from params import hb_1200_order as order,  hb_1200_energy_rp as energy
from params import hb_1200_SlitSize as SlitSize, hb_1200_grating as grating 
from params import hb_1200_blaze as blaze, hb_1200_cff as cff
from params import hb_1200_nrays_rp as nrays, hb_1200_rounds_rp as rounds
from params import hb_1200_ncpu_rp as ncpu, hb_1200_sim_name_rp as sim_name
from params import hb_1200_file_path

sim = Simulate(hb_1200_file_path, hide=True)

rml=sim.rml
beamline = sim.rml.beamline


params = [  
            {beamline.ExitSlit.totalHeight:SlitSize},
            {beamline.CPMU20.photonEnergy:energy},
            {beamline.PG.cFactor:cff}, 
            {beamline.PG.orderDiffraction:order},
            {beamline.CPMU20.numberRays:nrays}, 
        ]

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = sim_name

# turn off reflectivity
sim.reflectivity(reflectivity=False)

# repeat the simulations as many time as needed
sim.repeat = rounds

sim.analyze = False # let RAY-UI analyze the results
sim.raypyng_analysis = True # let RAY-UI analyze the results

## This must be a list of dictionaries
sim.exports  =  [
    {beamline.DetectorAtFocus:['RawRaysOutgoing']}
    ]


# create the rml files
#sim.rml_list()

#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=False, remove_round_folders=True, remove_rawrays=True)
