from raypyng import Simulate
import numpy as np
import os
from andrey_lib import AndreyML

this_file_dir=os.path.dirname(os.path.realpath(__file__))
rml_file_name = 'battery_FLUX_forML_IrCrB4C'
rml_file = os.path.join('rml/'+rml_file_name+'.rml')

sim = Simulate(rml_file, hide=True)

rml=sim.rml
beamline = sim.rml.beamline

# cpu
ncpu=20

# define the values of the parameters to scan 
order     = 2
energy    = np.arange(500, 5001,500)
SlitSize  = np.array([0.05,0.04,0.03,0.02,0.01])
nrays     = 1000000 

# Andrey ML
aml = AndreyML(excel_file_name=os.path.join('ML_eff','grating_eff_5000.xlsx'))
cff = aml.get_cff_for_ML(ind='MLBG_mfm_first', order=2, energy=np.arange(500, 5001,500))
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
sim.simulation_name = 'RP_'+rml_file_name

# turn off reflectivity
sim.reflectivity(reflectivity=False)
# repeat the simulations as many time as needed
sim.repeat = 10

sim.analyze = True # let RAY-UI analyze the results
## This must be a list of dictionaries
sim.exports  =  [{beamline.CPMU20:['ScalarElementProperties']},
                {beamline.DetectorAtFocus:['ScalarBeamProperties']}
                ]


# create the rml files
#sim.rml_list()

#uncomment to run the simulations
sim.run(multiprocessing=ncpu, force=True)
