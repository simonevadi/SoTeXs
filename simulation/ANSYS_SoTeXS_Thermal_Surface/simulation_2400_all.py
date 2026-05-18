import pandas as pd
from raypyng import Simulate

from sim_params import (
    RML_DIR,
    UNDULATOR_PATH,
    ncpu,
    nrays,
    rounds,
    force,
    remove_round_folders,
    remove_rawrays,
    energies_2400,
    cf_values_2400,
    simulation_prefix_2400,
    order_2400,
    exit_slit_2400,
)

# Comment out entries you do not want to run.
SIMULATION_RMLS = [
    ('nodef', 'sotexs_2400.rml'),
    ('profile001', 'sotexs_2400_profile001.rml'),
    ('profile002', 'sotexs_2400_profile002.rml'),
    ('profile003', 'sotexs_2400_profile003.rml'),
    ('profile004', 'sotexs_2400_profile004.rml'),
]

for label, rml_name in SIMULATION_RMLS:
    print(f'[START] 2400 {label} ({rml_name})')
    sim = Simulate(str(RML_DIR / rml_name), hide=True)
    beamline = sim.rml.beamline

    sim.params = [
        {beamline.ExitSlit.openingHeight: [exit_slit_2400]},
        {beamline.CPMU20.photonEnergy: energies_2400, beamline.PG.cFactor: cf_values_2400},
        {beamline.PG.orderDiffraction: [order_2400]},
        {beamline.CPMU20.numberRays: nrays},
    ]

    sim.simulation_name = f'{simulation_prefix_2400}_{label}'
    sim.repeat = rounds
    sim.analyze = False
    sim.raypyng_analysis = True
    sim.reflectivity = False

    sim.undulator_table = pd.read_csv(UNDULATOR_PATH)
    sim.exports = [
        {beamline.M1_hor_foc: ['RawRaysOutgoing']},
        {beamline.ExitSlit: ['RawRaysOutgoing', 'RawRaysIncoming']},
        {beamline.DetectorAtFocus: ['RawRaysOutgoing']},
    ]

    sim.run(
        multiprocessing=ncpu,
        force=force,
        remove_round_folders=remove_round_folders,
        remove_rawrays=remove_rawrays,
    )
    print(f'[DONE] 2400 {label}')
