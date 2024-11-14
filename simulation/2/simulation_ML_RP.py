import os
from raypyng import Simulate

from multilayer_lib import AndreyML
from params import order, energy_rp as energy, SlitSize
from params import nrays_rp as nrays, ml_index, repeat_rp as repeat
from params import ncpu_rp as ncpu, rml_file_name

this_file_dir=os.path.dirname(os.path.realpath(__file__))
rml_file = os.path.join('rml/'+rml_file_name+'.rml')

sim = Simulate(rml_file, hide=True)

rml=sim.rml
beamline = sim.rml.beamline


# Andrey ML
aml = AndreyML(excel_file_name=os.path.join('ML_eff','grating_eff_5000.xlsx'))
cff = aml.get_cff_for_ML(ind=ml_index, order=order, energy=energy)
# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.CPMU20.photonEnergy:energy, 
            beamline.PG.cFactor:cff}, 
            {beamline.ExitSlit.totalHeight:SlitSize},
            {beamline.PG.orderDiffraction:order},
            {beamline.CPMU20.numberRays:nrays}
        ]

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = 'RP_ML'

# turn off reflectivity
sim.reflectivity(reflectivity=False)
# repeat the simulations as many time as needed
sim.repeat = repeat

sim.analyze = False # let RAY-UI analyze the results
sim.raypyng_analysis=True # let raypyng analyze the results

## This must be a list of dictionaries
sim.exports  =  [{beamline.CPMU20:['RawRaysOutgoing']},
                {beamline.DetectorAtFocus:['RawRaysOutgoing']}
                ]

sim.run(multiprocessing=ncpu, force=False)
