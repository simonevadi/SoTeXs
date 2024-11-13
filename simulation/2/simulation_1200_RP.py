import os
from raypyng import Simulate

from params import order, energy_flux as energy, SlitSize
from params import grating_1200 as grating, cff_1200 as cff
from params import nrays_flux as nrays, repeat_flux as repeat
from params import ncpu_rp as ncpu
from params import rml_file_name

this_file_dir=os.path.dirname(os.path.realpath(__file__))
rml_file = os.path.join('rml/'+rml_file_name+'.rml')

sim = Simulate(rml_file, hide=True)

rml=sim.rml
beamline = sim.rml.beamline

# define a list of dictionaries with the parameters to scan
params = [  
            {beamline.CPMU20.photonEnergy:energy},
            {beamline.PG.lineDensity:grating}, 
            {beamline.PG.cFactor:cff}, 
            {beamline.ExitSlit.totalHeight:SlitSize},
            {beamline.PG.orderDiffraction:order},
            {beamline.CPMU20.numberRays:nrays}
        ]

#and then plug them into the Simulation class
sim.params=params

# sim.simulation_folder = '/home/simone/Documents/RAYPYNG/raypyng/test'
sim.simulation_name = 'RP_1200'

# repeat the simulations as many time as needed
sim.repeat = repeat

sim.analyze = False # let RAY-UI analyze the results
sim.raypyng_analysis=True # let raypyng analyze the results

# reflectivity 100%
sim.reflectivity(reflectivity=False)

## This must be a list of dictionaries
sim.exports  =  [{beamline.CPMU20:['RawRaysOutgoing']},
                {beamline.DetectorAtFocus:['RawRaysOutgoing']}
                ]


sim.run(multiprocessing=ncpu, force=False)
