from pathlib import Path
import numpy as np
import pandas as pd

ncpu = 'auto'
nrays = 1e5
rounds = 5
force = True
remove_round_folders = False
remove_rawrays = True

BASE_DIR = Path(__file__).resolve().parent
RML_DIR = BASE_DIR / 'rml'
UNDULATOR_PATH = Path(__file__).resolve().parents[2] / 'undulator' / 'CPMU20.csv'

energies_1200 = [500, 750, 1000, 1250, 1500]
simulation_prefix_1200 = 'ansys_1200_pt'

ml_grating_file = Path(__file__).resolve().parents[2] / 'ML_eff' / 'ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLbGR.dat'
grating = pd.read_csv(ml_grating_file, sep='\s+')

# Pick 7 equally distributed energy/cff couples directly from the ML table.
grating_window = grating[(grating['Energy'] >= 500.0) & (grating['Energy'] <= 6000.0)].copy()
grating_window = grating_window.sort_values('Energy').reset_index(drop=True)
idx = np.linspace(0, len(grating_window) - 1, 7, dtype=int)
sampled = grating_window.iloc[idx]
energies_2400 = sampled['Energy'].to_numpy()
cf_values_2400 = sampled['Cff'].to_numpy()

simulation_prefix_2400 = 'ansys_2400'
order_2400 = 2
exit_slit_2400 = 0.03
