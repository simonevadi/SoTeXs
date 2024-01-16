from raypyng import Simulate
import numpy as np
import os
from andrey_lib import AndreyML

from params import order, energy_flux as energy, SlitSize
from params import nrays_flux as nrays, index, repeat_flux as repeat
from params import ncpu_rp as ncpu


this_file_dir=os.path.dirname(os.path.realpath(__file__))
rml_file_name = 'battery_FLUX_forML_IrCrB4C'
rml_file = os.path.join('rml/'+rml_file_name+'.rml')

sim = Simulate(rml_file, hide=True)

rml=sim.rml
beamline = sim.rml.beamline


# Andrey ML
aml = AndreyML(excel_file_name=os.path.join('ML_eff','grating_eff_5000.xlsx'))
cff = aml.get_cff_for_ML(ind=index, order=order, energy=energy)
# define a list of dictionaries with the parameters to scan
params = [  
            # set two parameters: "alpha" and "beta" in a dependent way. 
            {beamline.CPMU20.photonEnergy:energy, 
            beamline.PG.cFactor:cff}, 
            # set a range of  values 
            {beamline.ExitSlit.totalHeight:SlitSize},
            # set values 
            {beamline.PG.orderDiffraction:order},
            {beamline.CPMU20.numberRays:nrays}
        ]

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = 'FLUX_'+rml_file_name

# repeat the simulations as many time as needed
sim.repeat = repeat

sim.analyze = True # let RAY-UI analyze the results
## This must be a list of dictionaries
sim.exports  =  [{beamline.CPMU20:['ScalarElementProperties']},
                {beamline.DetectorAtFocus:['ScalarBeamProperties']}
                ]


# create the rml files
#sim.rml_list()

#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=True)
