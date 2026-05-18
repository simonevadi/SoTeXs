from pathlib import Path
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

TARGET_DAT_SIZE_MB = 40
BYTES_PER_VALUE_LINE = 24
HEADER_BYTES_ESTIMATE = 256
MAX_RAW_POINTS_FOR_INTERP = 300000


def parse_ansys_file(path: Path):
    rows = []
    with path.open('r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            normalized = ' '.join(line.replace(',', '.').replace('\t', ' ').split())
            if not normalized:
                continue
            parts = normalized.split(' ')
            if len(parts) < 4:
                continue
            try:
                x = float(parts[0])
                z = float(parts[2])
                uy = float(parts[3])
            except ValueError:
                continue
            rows.append((x, z, uy))

    if not rows:
        raise ValueError(f'No numeric data parsed from {path}')

    data = np.array(rows, dtype=float)
    return data[:, 0], data[:, 1], data[:, 2]


def _infer_step(values: np.ndarray) -> float:
    s = np.sort(np.unique(values))
    if len(s) < 2:
        return 0.0
    d = np.diff(s)
    d = d[np.abs(d) > 1e-10]
    if len(d) == 0:
        return 0.0
    step = float(np.percentile(np.abs(d), 10))
    return step if step > 0 else float(np.median(np.abs(d)))


def reduce_raw_points_for_speed(x, z, uy_mm, max_points: int = MAX_RAW_POINTS_FOR_INTERP):
    n = len(x)
    if n <= max_points:
        return x, z, uy_mm

    x_step = _infer_step(x)
    z_step = _infer_step(z)
    if x_step <= 0 or z_step <= 0:
        idx = np.linspace(0, n - 1, max_points, dtype=int)
        return x[idx], z[idx], uy_mm[idx]

    ratio = (n / float(max_points)) ** 0.5
    coarse_x = x_step * ratio
    coarse_z = z_step * ratio

    xq = np.round(x / coarse_x).astype(np.int64)
    zq = np.round(z / coarse_z).astype(np.int64)
    key = np.stack([xq, zq], axis=1)
    uniq, inv = np.unique(key, axis=0, return_inverse=True)

    sx = np.zeros(len(uniq), dtype=float)
    sz = np.zeros(len(uniq), dtype=float)
    sh = np.zeros(len(uniq), dtype=float)
    cnt = np.zeros(len(uniq), dtype=float)
    np.add.at(sx, inv, x)
    np.add.at(sz, inv, z)
    np.add.at(sh, inv, uy_mm)
    np.add.at(cnt, inv, 1.0)

    return sx / cnt, sz / cnt, sh / cnt


def build_regular_grid(x, z, uy_mm, src_name: str):
    def snap(values: np.ndarray, step: float) -> np.ndarray:
        if step <= 0:
            return values.copy()
        return np.round(values / step) * step

    x, z, uy_mm = reduce_raw_points_for_speed(x, z, uy_mm)
    x_snapped = snap(x, _infer_step(x))
    z_snapped = snap(z, _infer_step(z))

    x_vals = np.array(sorted(np.unique(x_snapped)))
    z_vals = np.array(sorted(np.unique(z_snapped)))

    acc = {}
    cnt = {}
    for xi, zi, hi in zip(x_snapped, z_snapped, uy_mm):
        k = (xi, zi)
        acc[k] = acc.get(k, 0.0) + hi
        cnt[k] = cnt.get(k, 0) + 1

    H_mm = np.full((len(x_vals), len(z_vals)), np.nan, dtype=float)
    z_index = {v: i for i, v in enumerate(z_vals)}
    x_index = {v: i for i, v in enumerate(x_vals)}
    for (xv, zv), s in acc.items():
        H_mm[x_index[xv], z_index[zv]] = s / cnt[(xv, zv)]

    if np.isnan(H_mm).any():
        Xg, Zg = np.meshgrid(x_vals, z_vals, indexing='ij')
        points = np.column_stack([x_snapped, z_snapped])
        lin = griddata(points, uy_mm, (Xg, Zg), method='linear')
        near = griddata(points, uy_mm, (Xg, Zg), method='nearest')
        H_mm = np.where(np.isnan(H_mm), lin, H_mm)
        H_mm = np.where(np.isnan(H_mm), near, H_mm)

    if np.isnan(H_mm).any():
        missing = int(np.isnan(H_mm).sum())
        raise ValueError(f'{src_name}: grid still contains {missing} NaN points after interpolation')

    return x_vals, z_vals, H_mm


def estimate_spacing(vals: np.ndarray) -> float:
    if len(vals) < 2:
        return 0.0
    diffs = np.diff(vals)
    positive = diffs[np.abs(diffs) > 1e-12]
    if len(positive) == 0:
        return 0.0
    return float(np.median(np.abs(positive)))


def plot_outputs(stem: str, x_vals, z_vals, H_nm, plots_dir: Path):
    t0 = time.perf_counter()
    X, Z = np.meshgrid(x_vals, z_vals, indexing='ij')

    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111)
    pcm = ax.pcolormesh(X, Z, H_nm, shading='auto')
    cbar = fig.colorbar(pcm, ax=ax)
    cbar.set_label('UY deformation [nm]')
    ax.set_xlabel('X [mm]')
    ax.set_ylabel('Z [mm]')
    ax.set_title(f'{stem} deformation map')
    fig.tight_layout()
    fig.savefig(plots_dir / f'{stem}_heatmap.png', dpi=180)
    plt.close(fig)
    print(f'    [plot] {stem}: heatmap saved ({len(x_vals)}x{len(z_vals)}) in {time.perf_counter() - t0:.1f}s')

    t1 = time.perf_counter()
    fig3d = plt.figure(figsize=(10, 7))
    ax3d = fig3d.add_subplot(111, projection='3d')
    # Decimate 3D mesh for speed while preserving overall shape.
    step_x = max(1, len(x_vals) // 250)
    step_z = max(1, len(z_vals) // 250)
    X3 = X[::step_x, ::step_z]
    Z3 = Z[::step_x, ::step_z]
    H3 = H_nm[::step_x, ::step_z]
    surf = ax3d.plot_surface(X3, Z3, H3, cmap='viridis', linewidth=0, antialiased=True)
    cbar3d = fig3d.colorbar(surf, ax=ax3d, shrink=0.7, aspect=14)
    cbar3d.set_label('UY deformation [nm]')
    ax3d.set_xlabel('X [mm]')
    ax3d.set_ylabel('Z [mm]')
    ax3d.set_zlabel('UY [nm]')
    ax3d.set_title(f'{stem} deformation surface')
    fig3d.tight_layout()
    fig3d.savefig(plots_dir / f'{stem}_surface3d.png', dpi=180)
    plt.close(fig3d)
    print(
        f'    [plot] {stem}: 3d surface saved '
        f'({X3.shape[0]}x{X3.shape[1]} mesh) in {time.perf_counter() - t1:.1f}s'
    )

def extract_centerline(x_vals, z_vals, H_nm):
    center_ix = len(x_vals) // 2
    return z_vals, H_nm[center_ix, :], x_vals[center_ix]


def plot_combined_centerlines(centerlines, plots_dir: Path):
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)
    for stem, z_vals, center_vals, center_x in centerlines:
        ax.plot(z_vals, center_vals, lw=1.5, label=f'{stem} (x={center_x:.6g} mm)')

    ax.set_xlabel('Z [mm]')
    ax.set_ylabel('UY [nm]')
    ax.set_title('Centerline Comparison')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(plots_dir / 'centerline_comparison.png', dpi=180)
    plt.close(fig)


def _max_points_from_size(target_size_mb: float) -> int:
    target_bytes = int(target_size_mb * 1024 * 1024)
    return max(100, (target_bytes - HEADER_BYTES_ESTIMATE) // BYTES_PER_VALUE_LINE)


def _resample_grid(x_vals, z_vals, H_nm, max_points: int):
    t0 = time.perf_counter()
    nx = len(x_vals)
    nz = len(z_vals)
    total = nx * nz
    if total <= max_points:
        print(f'    [resample] grid already within limit: {nx}x{nz} ({total:,} pts)')
        return x_vals, z_vals, H_nm

    scale = (max_points / float(total)) ** 0.5
    new_nx = max(2, int(np.floor(nx * scale)))
    new_nz = max(2, int(np.floor(nz * scale)))
    ix = np.linspace(0, nx - 1, new_nx, dtype=int)
    iz = np.linspace(0, nz - 1, new_nz, dtype=int)
    x_new = x_vals[ix]
    z_new = z_vals[iz]
    H_new = H_nm[np.ix_(ix, iz)]

    print(
        f'    [resample] {nx}x{nz} -> {new_nx}x{new_nz} '
        f'({total:,} -> {new_nx * new_nz:,} pts) in {time.perf_counter() - t0:.1f}s'
    )

    return x_new, z_new, H_new


def prepare_git_safe_export_grid(x_vals, z_vals, H_nm):
    max_points = _max_points_from_size(TARGET_DAT_SIZE_MB)
    print(f'    [resample] target ~{TARGET_DAT_SIZE_MB}MB => max {max_points:,} grid points')
    return _resample_grid(x_vals, z_vals, H_nm, max_points)


def write_ray_profile(stem: str, x_vals, z_vals, H_nm, ray_out_dir: Path):
    t0 = time.perf_counter()
    nx = len(x_vals)
    nz = len(z_vals)
    dx = estimate_spacing(x_vals)
    dz = estimate_spacing(z_vals)

    out_file = ray_out_dir / f'{stem}_ray_profile.dat'
    with out_file.open('w', encoding='utf-8') as f:
        f.write(f'{nx}\t{nz}\t{dx:.12g}\t{dz:.12g}\n')
        for ix in range(nx):
            for iz in range(nz):
                f.write(f'{H_nm[ix, iz]:.12g}\n')
    print(f'    [write] {stem}: wrote {nx*nz:,} values in {time.perf_counter() - t0:.1f}s')

    size_mb = out_file.stat().st_size / (1024 * 1024)
    if size_mb > TARGET_DAT_SIZE_MB:
        print(f'    [write] {stem}: {size_mb:.1f}MB exceeds target, applying guardrail coarsening...')
        x2, z2, h2 = _resample_grid(x_vals, z_vals, H_nm, int(nx * nz * 0.7))
        nx2 = len(x2)
        nz2 = len(z2)
        dx2 = estimate_spacing(x2)
        dz2 = estimate_spacing(z2)
        with out_file.open('w', encoding='utf-8') as f:
            f.write(f'{nx2}\t{nz2}\t{dx2:.12g}\t{dz2:.12g}\n')
            for ix in range(nx2):
                for iz in range(nz2):
                    f.write(f'{h2[ix, iz]:.12g}\n')
        size_mb = out_file.stat().st_size / (1024 * 1024)
    print(f'    [write] {stem}: final file size {size_mb:.1f}MB')
