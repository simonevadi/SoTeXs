import pandas as pd
from raypyng import Simulate

from sim_params import (
    RML_DIR,
    UNDULATOR_PATH,
    ncpu,
    nrays_distance_scan,
    rounds_distance_scan,
    force,
    remove_round_folders,
    remove_rawrays,
    distance_scan_energies,
    distance_image_plane_values,
    simulation_prefix_distance_scan,
)

sim = Simulate(str(RML_DIR / 'sotexs_1200_Pt.rml'), hide=True)
beamline = sim.rml.beamline

sim.params = [
    {beamline.CPMU20.photonEnergy: distance_scan_energies},
    {beamline.M1_hor_foc.distanceImagePlane: distance_image_plane_values},
    {beamline.CPMU20.numberRays: nrays_distance_scan},
]

sim.simulation_name = simulation_prefix_distance_scan
sim.repeat = rounds_distance_scan
sim.analyze = False
sim.raypyng_analysis = True
sim.undulator_table = pd.read_csv(UNDULATOR_PATH)
sim.exports = [
    {beamline.M1_hor_foc: ['RawRaysOutgoing']},
]
sim.reflectivity = False

sim.run(
    multiprocessing=ncpu,
    force=force,
    remove_round_folders=remove_round_folders,
    remove_rawrays=remove_rawrays,
)
