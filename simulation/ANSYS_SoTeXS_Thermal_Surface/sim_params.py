from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RML_DIR = BASE_DIR / 'rml'
UNDULATOR_PATH = Path(__file__).resolve().parents[2] / 'undulator' / 'CPMU20.csv'

energies = [500, 750, 1000, 1250, 1500, 1750, 2000]
ncpu = 'auto'
nrays = 5e5
rounds = 1
force = True
remove_round_folders = True
remove_rawrays = True
simulation_prefix = 'ansys_1200_pt'
