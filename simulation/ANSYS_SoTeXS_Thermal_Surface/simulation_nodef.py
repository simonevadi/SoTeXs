import pandas as pd
from raypyng import Simulate
from sim_params import (
    RML_DIR,
    UNDULATOR_PATH,
    energies,
    ncpu,
    nrays,
    rounds,
    force,
    remove_round_folders,
    remove_rawrays,
    simulation_prefix,
)

sim = Simulate(str(RML_DIR / 'sotexs_1200_Pt.rml'), hide=True)
beamline = sim.rml.beamline

sim.params = [
    {beamline.CPMU20.photonEnergy: energies},
    {beamline.CPMU20.numberRays: nrays},
]

sim.simulation_name = f'{simulation_prefix}_nodef'
sim.repeat = rounds
sim.analyze = False
sim.raypyng_analysis = True
sim.undulator_table = pd.read_csv(UNDULATOR_PATH)
sim.exports = [
    {beamline.ExitSlit: ['RawRaysOutgoing', 'RawRaysIncoming']},
    {beamline.M1_hor_foc: ['RawRaysOutgoing']},
]

sim.run(
    multiprocessing=ncpu,
    force=force,
    remove_round_folders=remove_round_folders,
    remove_rawrays=remove_rawrays,
)
