import os
import pandas as pd
import matplotlib.pyplot as plt

from sim_params import simulation_prefix_distance_scan

base_dir = os.path.dirname(os.path.abspath(__file__))
scan_dir = os.path.join(base_dir, f'RAYPy_Simulation_{simulation_prefix_distance_scan}')
csv_file = os.path.join(scan_dir, 'M1_hor_foc_RawRaysOutgoing.csv')

df = pd.read_csv(csv_file)
df = df.sort_values(['CPMU20.photonEnergy', 'M1_hor_foc.distanceImagePlane'])

energies = sorted(df['CPMU20.photonEnergy'].dropna().unique())

plt.figure(figsize=(9, 5))
for e in energies:
    dfe = df[df['CPMU20.photonEnergy'] == e]
    plt.plot(
        dfe['M1_hor_foc.distanceImagePlane'],
        dfe['HorizontalFocusFWHM'],
        marker='o',
        label=f'{e:.3f} eV'
    )

plt.xlabel('M1_hor_foc.distanceImagePlane')
plt.ylabel('HorizontalFocusFWHM [mm]')
plt.title('1200 Distance Scan: Horizontal FWHM vs M1_hor_foc.distanceImagePlane')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

out_png = os.path.join(base_dir, 'results', 'plots', 'eval_distance_scan_1200.png')
plt.savefig(out_png, dpi=180)
# plt.show()
print('Saved figure:', out_png)
