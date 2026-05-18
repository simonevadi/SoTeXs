import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit

fname = "power_distro_perp_screen.dat"

data = np.genfromtxt(fname, skip_header=1)

y = data[:, 0]   # [mm]
z = data[:, 1]   # [mm]
P_perp = data[:, 2]   # [W/mm^2]


y_vals = np.unique(y)
z_vals = np.unique(z)
ny, nz = len(y_vals), len(z_vals)

print("ny, nz =", ny, nz)


Y, Z = np.meshgrid(y_vals, z_vals)         
P_grid = P_perp.reshape(nz, ny)             

# 90 Grad Schirm plotten
plt.figure(figsize=(5, 4))
pc = plt.pcolormesh(Y, Z, P_grid, shading="auto")
plt.xlabel("y [mm]")
plt.ylabel("z [mm]")
plt.title("Leistungsdichte auf senkrechtem Schirm (90°)")
cbar = plt.colorbar(pc)
cbar.set_label("P⊥ [W/mm²]")
plt.tight_layout()
plt.show()


# PLot auf 0,7 grad schirm
theta_deg = 0.7
theta = math.radians(theta_deg)
sin_theta = math.sin(theta)

X_tilt = Y / sin_theta         
P_tilt = P_grid * sin_theta     

plt.figure(figsize=(6, 4))
pc = plt.pcolormesh(X_tilt, Z, P_tilt, shading="auto")
plt.xlabel("x (entlang Schirm) [mm]")
plt.ylabel("z [mm]")
plt.title(f"Leistungsdichte auf {theta_deg}° geneigtem Schirm")
cbar = plt.colorbar(pc)
cbar.set_label("P_mirror [W/mm²]")
plt.tight_layout()
plt.show()

# Deltas Schritt
dy = y_vals[1] - y_vals[0]
dz = z_vals[1] - z_vals[0]

# Total 
P_tot_perp = P_grid.sum() * dy * dz

# Total 0,7 gradschirm
dx = dy / sin_theta
P_tot_tilt = P_tilt.sum() * dx * dz

print("P_total (90°-Schirm):", P_tot_perp, "W")
print("P_total (0.7°-Schirm):", P_tot_tilt, "W")

# Fit with BlaBlaDor 

def super_gauss2d(coords, A, x0, z0, sigma_x, sigma_z, p_x, p_z, offset):
    """
    2D-Super-Gauss:
    P = offset + A * exp( -(|(x-x0)/sigma_x|^p_x + |(z-z0)/sigma_z|^p_z) )
    """
    x, z = coords
    dx = (x - x0) / sigma_x
    dz = (z - z0) / sigma_z
    return offset + A * np.exp(- (np.abs(dx)**p_x + np.abs(dz)**p_z))

# 1D-Arrays
x_data = X_tilt.ravel()
z_data = Z.ravel()
P_data = P_tilt.ravel()

# grobe Startwerte
P_min = P_data.min()
P_max = P_data.max()

A0 = P_max - P_min
offset0 = P_min

imax = np.argmax(P_data)
x0_0 = x_data[imax]
z0_0 = z_data[imax]

sigma_x0 = (x_data.max() - x_data.min()) / 4.0
sigma_z0 = (z_data.max() - z_data.min()) / 4.0

p0 = (A0, x0_0, z0_0, sigma_x0, sigma_z0, 2.0, 2.0, offset0)
print("Startwerte 2D-Gauss:", p0)

# sinnvolle Grenzen (sigma > 0, Exponenten z.B. 0.5 ... 10)
lower = [0,    -np.inf, -np.inf,  1e-6,  1e-6,  0.5,  0.5, -np.inf]
upper = [np.inf, np.inf,  np.inf, np.inf, np.inf, 10.0, 10.0, np.inf]

popt, pcov = curve_fit(
    super_gauss2d,
    (x_data, z_data),
    P_data,
    p0=p0,
    bounds=(lower, upper),
    maxfev=60000
)

A_s, x0_s, z0_s, sig_x_s, sig_z_s, p_x_s, p_z_s, offset_s = popt

print("\nFit-Parameter (2D-Gauss auf 0,7°-Schirm):")
print(f"A       = {A_s:.5f} W/mm²")
print(f"x0      = {x0_s:.3f} mm")
print(f"z0      = {z0_s:.3f} mm")
print(f"sigma_x = {sig_x_s:.3f} mm")
print(f"sigma_z = {sig_z_s:.3f} mm")
print(f"p_x     = {p_x_s:.3f}")
print(f"p_z     = {p_z_s:.3f}")
print(f"offset  = {offset_s:.5f} W/mm²")

# Gefittete Verteilung im Gitter
P_fit = super_gauss2d((X_tilt, Z), *popt)
res = P_tilt - P_fit
mse = np.mean(res**2)
# print(f"MSE (Super-Gauss, tilted screen) = {mse:.4e} (W/mm²)²")

fig, axes = plt.subplots(1, 3, figsize=(15, 4), constrained_layout=True)

# Original
im0 = axes[0].pcolormesh(X_tilt, Z, P_tilt, shading="auto")
axes[0].set_title("Original (0,7° Schirm)")
axes[0].set_xlabel("x [mm]")
axes[0].set_ylabel("z [mm]")
plt.colorbar(im0, ax=axes[0], label="P_tilt [W/mm²]")

# 2D-Gauss-Fit
im1 = axes[1].pcolormesh(X_tilt, Z, P_fit, shading="auto")
axes[1].set_title("2D-Gauss Fit")
axes[1].set_xlabel("x [mm]")
axes[1].set_ylabel("z [mm]")
plt.colorbar(im1, ax=axes[1], label="P_fit [W/mm²]")

# Fehler 
im2 = axes[2].pcolormesh(X_tilt, Z, res, shading="auto")
axes[2].set_title("Abweichung 2D-Gauss zu CPMU20 Daten")
axes[2].set_xlabel("x [mm]")
axes[2].set_ylabel("z [mm]")
plt.colorbar(im2, ax=axes[2], label="ΔP [W/mm²]")

plt.show()
