import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.optimize import curve_fit

# ------------------------------------------------------------
# 0. Einstellungen
# ------------------------------------------------------------
FILENAME = "mirror.dat"
THETA_DEG = 0.7        # Kippwinkel des Spiegels (nur für Info)
L_MIRROR_X = 520.0     # mm, Spiegel-Länge (x-Richtung)
L_MIRROR_Z = 35.0      # mm, Spiegel-Breite (z-Richtung)

# ------------------------------------------------------------
# 1. Daten einlesen
# ------------------------------------------------------------
data = np.genfromtxt(FILENAME, skip_header=1)

x = data[:, 0]   # [mm]
y = data[:, 1]   # [mm]
z = data[:, 2]   # [mm]
P = data[:, 3]   # [W/mm^2]

# Eindeutige Koordinaten
x_vals = np.unique(x)
y_vals = np.unique(y)
z_vals = np.unique(z)

nx = len(x_vals)
ny = len(y_vals)
nz = len(z_vals)

""" print(f"nx = {nx}, ny = {ny}, nz = {nz}")
print(f"x-range: {x_vals.min():.1f} .. {x_vals.max():.1f} mm "
      f"(Δx ≈ {x_vals.ptp():.1f} mm)")
print(f"z-range: {z_vals.min():.1f} .. {z_vals.max():.1f} mm "
      f"(Δz ≈ {z_vals.ptp():.1f} mm)") """

if nx * nz != len(P):
    raise ValueError(f"Grid mismatch: nx*nz = {nx*nz}, N = {len(P)}")

# 2D-Arrays in (z, x) – Reihenfolge der Daten: z langsam, x schnell
X = x.reshape(nz, nx)
Y = y.reshape(nz, nx)
Z = z.reshape(nz, nx)
P_xz = P.reshape(nz, nx)

dx = x_vals[1] - x_vals[0]   # [mm]
dz = z_vals[1] - z_vals[0]   # [mm]
dA = dx * dz                 # [mm^2]

print(f"dx = {dx:.3f} mm, dz = {dz:.3f} mm, dA = {dA:.3f} mm²")

# ------------------------------------------------------------
# 2. Plots: Footprint in x–z und Projektion in y–z
# ------------------------------------------------------------
# a) Footprint in x–z (zeigt 900 mm × 20 mm)
plt.figure(figsize=(5, 4))
pc = plt.pcolormesh(x_vals, z_vals, P_xz, shading="auto")
plt.xlabel("x [mm]")
plt.ylabel("z [mm]")
plt.title("Leistungsdichte auf dem Spiegel (x–z)")
cbar = plt.colorbar(pc)
cbar.set_label("P [W/mm²]")
plt.tight_layout()
plt.show()

# b) Projektion wie dein erster Plot: y–z
#    (hier nutzen wir die Tatsache, dass Y/Z die gleiche Shape wie P_xz haben)
plt.figure(figsize=(5, 4))
pc2 = plt.pcolormesh(y_vals, z_vals, P_xz, shading="auto")
plt.xlabel("y [mm]")
plt.ylabel("z [mm]")
plt.title("Leistungsdichte auf dem Spiegel (y–z Projektion)")
cbar2 = plt.colorbar(pc2)
cbar2.set_label("P [W/mm²]")
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 3. 3D-Plot des gekippten Spiegels (wie deine Mirror.png)
# ------------------------------------------------------------
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, projection="3d")

norm = plt.Normalize(P_xz.min(), P_xz.max())
colors = cm.plasma(norm(P_xz))

surf = ax.plot_surface(
    X,          # x [mm]
    Z,          # z [mm]
    Y,          # y [mm] (zeigt die ~0.7°-Neigung)
    facecolors=colors,
    linewidth=0,
    antialiased=True
)

m = cm.ScalarMappable(cmap=cm.plasma, norm=norm)
m.set_array(P_xz)
cbar3 = fig.colorbar(m, ax=ax, pad=0.15)
cbar3.set_label("P [W/mm²]")

ax.set_xlabel("x [mm]")
ax.set_ylabel("z [mm]")
ax.set_zlabel("y [mm]")
ax.set_title("Mirror (heat load on tilted surface)")

try:  # Seitenverhältnis halbwegs realistisch
    ax.set_box_aspect((X.ptp(), Z.ptp(), Y.ptp()))
except AttributeError:
    pass

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 4. 2D-Fits in y–z: Gauss & Super-Gauss
#    (wir fitten P(y,z), weil der Spot dort schön elliptisch ist)
# ------------------------------------------------------------
Y_yz, Z_yz = np.meshgrid(y_vals, z_vals)  # gleiche Shape wie P_xz
P_yz = P_xz.copy()

y_data = Y_yz.ravel()
z_data = Z_yz.ravel()
P_data = P_yz.ravel()

# --- einfacher 2D-Gauß ---
def gauss2d(coords, A, y0, z0, sigma_y, sigma_z, offset):
    y, z = coords
    return offset + A * np.exp(
        -(((y - y0)**2) / (2*sigma_y**2)
          + ((z - z0)**2) / (2*sigma_z**2))
    )

# Startwerte
P_min = P_data.min()
P_max = P_data.max()
A0 = P_max - P_min
offset0 = P_min

imax = np.argmax(P_data)
y0_0 = y_data[imax]
z0_0 = z_data[imax]

sigma_y0 = (y_vals.max() - y_vals.min()) / 4.0
sigma_z0 = (z_vals.max() - z_vals.min()) / 4.0

p0_gauss = (A0, y0_0, z0_0, sigma_y0, sigma_z0, offset0)

popt_gauss, _ = curve_fit(
    gauss2d, (y_data, z_data), P_data,
    p0=p0_gauss, maxfev=20000
)
A_g, y0_g, z0_g, sig_y_g, sig_z_g, offset_g = popt_gauss

print("\n--- 2D-Gauss-Fit (y,z) ---")
print(f"A       = {A_g:.3f} W/mm²")
print(f"y0      = {y0_g:.3f} mm")
print(f"z0      = {z0_g:.3f} mm")
print(f"sigma_y = {sig_y_g:.3f} mm")
print(f"sigma_z = {sig_z_g:.3f} mm")
print(f"offset  = {offset_g:.3f} W/mm²")

P_fit_gauss = gauss2d((Y_yz, Z_yz), *popt_gauss)
res_gauss = P_yz - P_fit_gauss
mse_gauss = np.mean(res_gauss**2)
print(f"MSE Gauss = {mse_gauss:.4f} (W/mm²)²")

# --- Super-Gauss (verallgemeinerter Gauß) ---
def super_gauss2d(coords, A, y0, z0, sigma_y, sigma_z, p_y, p_z, offset):
    y, z = coords
    dy = (y - y0) / sigma_y
    dz = (z - z0) / sigma_z
    return offset + A * np.exp(- (np.abs(dy)**p_y + np.abs(dz)**p_z))

p0_super = (A0, y0_0, z0_0, sigma_y0, sigma_z0, 2.0, 2.0, offset0)

popt_super, _ = curve_fit(
    super_gauss2d,
    (y_data, z_data), P_data,
    p0=p0_super,
    maxfev=60000
)

A_s, y0_s, z0_s, sig_y_s, sig_z_s, p_y_s, p_z_s, offset_s = popt_super

print("\n--- Super-Gauss-Fit (y,z) ---")
print(f"A       = {A_s:.3f} W/mm²")
print(f"y0      = {y0_s:.3f} mm")
print(f"z0      = {z0_s:.3f} mm")
print(f"sigma_y = {sig_y_s:.3f} mm")
print(f"sigma_z = {sig_z_s:.3f} mm")
print(f"p_y     = {p_y_s:.3f}")
print(f"p_z     = {p_z_s:.3f}")
print(f"offset  = {offset_s:.3f} W/mm²")

P_fit_super = super_gauss2d((Y_yz, Z_yz), *popt_super)
res_super = P_yz - P_fit_super
mse_super = np.mean(res_super**2)
print(f"MSE Super-Gauss = {mse_super:.4f} (W/mm²)²")

# Vergleichs-Plots Original / Gauss / Super-Gauss / Residuen
fig, axes = plt.subplots(2, 3, figsize=(15, 7), constrained_layout=True)

im0 = axes[0, 0].pcolormesh(y_vals, z_vals, P_yz, shading="auto")
axes[0, 0].set_title("Original")
axes[0, 0].set_xlabel("y [mm]")
axes[0, 0].set_ylabel("z [mm]")
plt.colorbar(im0, ax=axes[0, 0], label="P [W/mm²]")

im1 = axes[0, 1].pcolormesh(y_vals, z_vals, P_fit_gauss, shading="auto")
axes[0, 1].set_title("2D-Gauss-Fit")
axes[0, 1].set_xlabel("y [mm]")
axes[0, 1].set_ylabel("z [mm]")
plt.colorbar(im1, ax=axes[0, 1], label="P [W/mm²]")

im2 = axes[0, 2].pcolormesh(y_vals, z_vals, P_fit_super, shading="auto")
axes[0, 2].set_title("Super-Gauss-Fit")
axes[0, 2].set_xlabel("y [mm]")
axes[0, 2].set_ylabel("z [mm]")
plt.colorbar(im2, ax=axes[0, 2], label="P [W/mm²]")

im3 = axes[1, 1].pcolormesh(y_vals, z_vals, res_gauss, shading="auto")
axes[1, 1].set_title("Residuum: Gauss")
axes[1, 1].set_xlabel("y [mm]")
axes[1, 1].set_ylabel("z [mm]")
plt.colorbar(im3, ax=axes[1, 1], label="ΔP [W/mm²]")

im4 = axes[1, 2].pcolormesh(y_vals, z_vals, res_super, shading="auto")
axes[1, 2].set_title("Residuum: Super-Gauss")
axes[1, 2].set_xlabel("y [mm]")
axes[1, 2].set_ylabel("z [mm]")
plt.colorbar(im4, ax=axes[1, 2], label="ΔP [W/mm²]")

axes[1, 0].axis("off")
plt.show()

# ------------------------------------------------------------
# 5. Leistungsintegration & mittlere Wärmelast auf 520 x 35 mm
# ------------------------------------------------------------
# Gesamtleistung über kompletten Footprint (x–z)
P_total = P_xz.sum() * dA
print(f"\nTotal power on footprint: {P_total:.2f} W")

# Mittelpunkt des Footprints (für zentrierten Spiegel)
x_c = x_vals.mean()
z_c = z_vals.mean()
print(f"Footprint center: x_c = {x_c:.1f} mm, z_c = {z_c:.1f} mm")

# Spiegelgrenzen (zentriert auf den Footprint)
x_min_m = x_c - L_MIRROR_X / 2
x_max_m = x_c + L_MIRROR_X / 2
z_min_m = z_c - L_MIRROR_Z / 2
z_max_m = z_c + L_MIRROR_Z / 2

print(f"Mirror extent in x: [{x_min_m:.1f}, {x_max_m:.1f}] mm "
      f"(L = {L_MIRROR_X} mm)")
print(f"Mirror extent in z: [{z_min_m:.1f}, {z_max_m:.1f}] mm "
      f"(L = {L_MIRROR_Z} mm)")

# Maske: Punkte, die auf dem Spiegel liegen
mask_mirror = (
    (X >= x_min_m) & (X <= x_max_m) &
    (Z >= z_min_m) & (Z <= z_max_m)
)

P_mirror = P_xz[mask_mirror].sum() * dA      # [W]
A_mirror = L_MIRROR_X * L_MIRROR_Z           # [mm^2]
q_avg_full = P_mirror / A_mirror             # [W/mm^2]

A_illum = mask_mirror.sum() * dA             # beleuchtete Fläche auf Spiegel
q_avg_illum = P_mirror / A_illum             # [W/mm^2]

print(f"\nPower on mirror (within 520 x 35 mm): {P_mirror:.2f} W")
print(f"Average heat load over full mirror area: {q_avg_full:.4f} W/mm² "
      f"(= {q_avg_full*100:.2f} W/cm²)")
print(f"Average heat load over illuminated area: {q_avg_illum:.4f} W/mm² "
      f"(= {q_avg_illum*100:.2f} W/cm²)")
