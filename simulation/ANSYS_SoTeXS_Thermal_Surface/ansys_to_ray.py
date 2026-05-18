from pathlib import Path
from postprocess_optics import (
    parse_ansys_file,
    build_regular_grid,
    plot_outputs,
    write_ray_profile,
    extract_centerlines,
    plot_combined_centerlines,
    prepare_git_safe_export_grid,
)
try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / 'ANSYS_data' / 'Results'
OUTPUT_DIR = BASE_DIR / 'results'
PLOTS_DIR = OUTPUT_DIR / 'plots'
RAY_OUT_DIR = OUTPUT_DIR / 'ray_ui_import'
FILES = [
    'Flux_Face_UY_001.txt',
    'Flux_Face_UY_002.txt',
    'Flux_Face_UY_003.txt',
    'Flux_Face_UY_004.txt',
]
# Set to None for automatic y-limits.
SAGITTAL_YMIN = -50

PLOTS_DIR.mkdir(parents=True, exist_ok=True)
RAY_OUT_DIR.mkdir(parents=True, exist_ok=True)
centerlines = []
total_files = len(FILES)

print(f'Starting ANSYS-to-Ray conversion for {total_files} files')
print(f'Input folder: {RESULTS_DIR}')
print(f'Output plots: {PLOTS_DIR}')
print(f'Output Ray profiles: {RAY_OUT_DIR}')

iter_files = tqdm(FILES, desc='Converting files', unit='file') if tqdm else FILES

for idx, name in enumerate(iter_files, start=1):
    print(f'[{idx}/{total_files}] Reading {name}...')
    src = RESULTS_DIR / name
    if not src.exists():
        raise FileNotFoundError(f'Missing input file: {src}')

    x, z, uy_mm = parse_ansys_file(src)
    print(f'[{idx}/{total_files}] Building regular grid...')
    x_vals, z_vals, H_mm = build_regular_grid(x, z, uy_mm, name)
    H_nm = H_mm * 1e6
    stem = src.stem

    print(f'[{idx}/{total_files}] Resampling for git-safe export and plotting...')
    x_exp, z_exp, h_exp = prepare_git_safe_export_grid(x_vals, z_vals, H_nm)
    plot_outputs(stem, x_exp, z_exp, h_exp, PLOTS_DIR)
    mer_z, mer_vals, mer_x, sag_x, sag_vals, sag_z = extract_centerlines(x_exp, z_exp, h_exp)
    centerlines.append((stem, mer_z, mer_vals, mer_x, sag_x, sag_vals, sag_z))
    print(f'[{idx}/{total_files}] Writing Ray profile...')
    write_ray_profile(stem, x_exp, z_exp, h_exp, RAY_OUT_DIR)
    print(f'[{idx}/{total_files}] Done: {name}')

print('Generating combined centerline comparison...')
plot_combined_centerlines(centerlines, PLOTS_DIR, sagittal_ymin=SAGITTAL_YMIN)

print('Completed processing:', ', '.join(FILES))
print('Plots:', PLOTS_DIR)
print('Ray profiles:', RAY_OUT_DIR)
