import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit

def gaussian_2d(coords, A, x0, z0, sx, sz, offset):

    x, z = coords

    return (
        offset
        + A * np.exp(
            -(
                ((x - x0)**2)/(2*sx**2)
                + ((z - z0)**2)/(2*sz**2)
            )
        )
    ).ravel()

# ============================================================
# LOAD FILE
# ============================================================

filename = "Flux_Face_UY_001.txt"

with open(filename, "r", encoding="utf-8") as f:
    lines = f.readlines()

# ============================================================
# CLEAN DATA
# ============================================================

clean_lines = []

for line in lines:

    # replace decimal commas with dots
    line = line.replace(",", ".")

    # replace tabs with spaces
    line = line.replace("\t", " ")

    # remove duplicate spaces
    line = " ".join(line.split())

    clean_lines.append(line)

# remove header
clean_lines = clean_lines[1:]

# ============================================================
# PARSE NUMERICAL DATA
# ============================================================

data = [] # initialize array 
# example line form file: -2.2142e-2(X)  0.0(Y)  -265.0(Z)  1.53e-3(UY) - without the stuff in the commata
# every node in the surface with its coordinates and the deformation normal to the surface
for line in clean_lines: # loop for the lines in the .txt 

    parts = line.split() # Split One line into four columns using spaces

    if len(parts) < 4: #check if ervery line as four parts (X,Y,Z,UY)
        continue

    try: #Conversion of the strings to floats
        x = float(parts[0]) 
        y = float(parts[1])
        z = float(parts[2])
        uy = float(parts[3])

        data.append([x, z, uy]) # Only X.Z. and UY are needed in this processing

    except:
        continue

data = np.array(data) #Create numpy array 

# ============================================================
# EXTRACT COLUMNS
# ============================================================

x = data[:,0]
z = data[:,1]
h = data[:,2]

# convert mm -> nm
h_nm = h * 1e6

# ============================================================
# CREATE REGULAR GRID
# ============================================================

nx = 400 # Points in X
nz = 800 # Points in Z

xi = np.linspace(np.min(x), np.max(x), nx)
zi = np.linspace(np.min(z), np.max(z), nz)

X, Z = np.meshgrid(xi, zi)

H = griddata(
    (x, z),
    h_nm,
    (X, Z),
    method='cubic'
)

# ============================================================
# REMOVE RIGID BODY MOTION
# plane fit: h = a + bx + cz
# ============================================================
# The total defomation of the surface still contains the translation of the mirror body normal to the optical surface and the rotation around Z which also leads to translation in Y
valid = ~np.isnan(H) # Outside the FEM-region the interpolation fails, therefore we have to check for "dead" pixels // ~is a logical not 
# Fitting of an rigig body plane (with tilt and translation effect) to extract it in the end
A = np.column_stack([
    np.ones(np.sum(valid)), # Matrix of ones for a constan offset a
    X[valid], # b*x for a linear tilt in saggital direction 
    Z[valid] # c*z for a linear tilt in meridional directio 
])

coeff, _, _, _ = np.linalg.lstsq( # Least Square Fit for the coefficients of the plane
    A,
    H[valid],
    rcond=None
)

plane = ( 
    coeff[0]
    + coeff[1]*X
    + coeff[2]*Z
) # Calcualtes Best fiti rigid body plane 

Hcorr = H - plane # Removed Rigid Body Deformation of the optical surface 

# ============================================================
# COMPUTE SLOPES
# ============================================================
# Computating the Slopes is ususally more interesting than the total height (normal to the optical surface) of the surface.
# Slope = change in height/ change variable along the surface

dz = zi[1] - zi[0] #change in count variable in z
dx = xi[1] - xi[0] #change in count varibale in x

slope_z = np.gradient(Hcorr, dz, axis=0) # =delta H (along Z-axis) / dz 
slope_x = np.gradient(Hcorr, dx, axis=1)

# convert nm/mm -> urad
slope_z_urad = slope_z 
slope_x_urad = slope_x 

# ============================================================
# RMS SLOPE
# ============================================================


slope_rms_sagittal = np.nanstd(slope_z_urad) 
slope_rms_meridional = np.nanstd(slope_x_urad)

print()
print("========================================")
print("Meridional slope RMS [urad]")
print(slope_rms_meridional)

print()
print("Sagittal slope RMS [urad]")
print(slope_rms_sagittal)
print("========================================")

# ============================================================
# PLOT HEIGHT MAP
# ============================================================

plt.figure(figsize=(10,6))

plt.contourf(
    X,
    Z,
    Hcorr,
    levels=100
)

plt.ylabel("Sagittal Z [mm]")
plt.xlabel("Meridional X [mm]")

cbar = plt.colorbar()
cbar.set_label("Residual height [nm]")

plt.title("Thermoelastic deformation")

plt.tight_layout()
plt.show()

# ============================================================
# 3D SURFACE PLOT
# ============================================================

""" fig = plt.figure(figsize=(12,8))

ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(
    X,
    Z,
    Hcorr,
    rstride=2,
    cstride=2,
    linewidth=0,
    antialiased=True
)

ax.set_xlabel("Sagittal X [mm]")
ax.set_ylabel("Meridional Z [mm]")
ax.set_zlabel("Residual height [nm]")

ax.set_title("Thermoelastic surface deformation")

fig.colorbar(
    surf,
    shrink=0.6,
    aspect=12,
    label="Height [nm]"
)

plt.tight_layout()
plt.show() """

# ============================================================
# MERIDIONAL CENTER PROFILE
# ============================================================

center_idx = nx // 2
center_idz = nz // 2
plt.figure(figsize=(10,5))

plt.plot(
    zi,
    Hcorr[:,center_idx]
)

plt.xlabel("Sagittal Z [mm]")
plt.ylabel("Residual height [nm]")

plt.title("Sagittal center profile")

plt.grid(True)

plt.tight_layout()
plt.show()

# ============================================================
# MERIDIONAL SLOPE PROFILE
# ============================================================

plt.figure(figsize=(10,5))

plt.plot(
    zi,
    slope_z_urad[:,center_idx]
)

plt.xlabel("Sagittal Z [mm]")
plt.ylabel("Slope [urad]")

plt.title("Sagittal slope")

plt.grid(True)

plt.tight_layout()
plt.show()




# ============================================================
# 2D GAUSSIAN FUNCTION
# ============================================================

valid = ~np.isnan(Hcorr)

xfit = X[valid]
zfit = Z[valid]
hfit = Hcorr[valid]

# ============================================================
# INITIAL GUESS
# ============================================================

A0 = np.nanmax(Hcorr)

x0_0 = 0
z0_0 = 0

sx0 = 5
sz0 = 100

offset0 = 0

p0 = [
    A0,
    x0_0,
    z0_0,
    sx0,
    sz0,
    offset0
]

popt, pcov = curve_fit(
    gaussian_2d,
    (xfit, zfit),
    hfit,
    p0=p0
)

A_fit, x0_fit, z0_fit, sx_fit, sz_fit, offset_fit = popt

print()
print("====================================")
print("GAUSSIAN THERMAL DISTORTION FIT")
print("====================================")

print(f"Amplitude A      : {A_fit:.3f} nm")
print(f"Center X0        : {x0_fit:.3f} mm")
print(f"Center Z0        : {z0_fit:.3f} mm")
print(f"Sigma X          : {sx_fit:.3f} mm")
print(f"Sigma Z          : {sz_fit:.3f} mm")

print("====================================")

# ============================================================
# RECONSTRUCT FITTED GAUSSIAN
# ============================================================

Hfit = gaussian_2d(
    (X, Z),
    *popt
).reshape(X.shape)


# ============================================================
# PLOT FITTED GAUSSIAN
# ============================================================

""" plt.figure(figsize=(10,6))

plt.contourf(
    X,
    Z,
    Hfit,
    levels=100
)

plt.xlabel("Sagittal X [mm]")
plt.ylabel("Meridional Z [mm]")

cbar = plt.colorbar()
cbar.set_label("Fitted height [nm]")

plt.title("Gaussian approximation of thermal distortion")

plt.tight_layout()
plt.show() """