import os
import pandas as pd
import matplotlib.pyplot as plt

base_dir = os.path.dirname(os.path.abspath(__file__))

cases = [
    ('nodef', 'RAYPy_Simulation_ansys_1200_pt_nodef'),
    ('profile001', 'RAYPy_Simulation_ansys_1200_pt_profile001'),
    ('profile002', 'RAYPy_Simulation_ansys_1200_pt_profile002'),
    ('profile003', 'RAYPy_Simulation_ansys_1200_pt_profile003'),
    ('profile004', 'RAYPy_Simulation_ansys_1200_pt_profile004'),
]

fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

for label, folder in cases:
    m1_file = os.path.join(base_dir, folder, 'M1_hor_foc_RawRaysOutgoing.csv')
    ex_in_file = os.path.join(base_dir, folder, 'ExitSlit_RawRaysIncoming.csv')
    ex_out_file = os.path.join(base_dir, folder, 'ExitSlit_RawRaysOutgoing.csv')

    m1_df = pd.read_csv(m1_file)
    ex_in_df = pd.read_csv(ex_in_file)
    ex_out_df = pd.read_csv(ex_out_file)

    m1_df = m1_df.sort_values('CPMU20.photonEnergy')
    ex_in_df = ex_in_df.sort_values('CPMU20.photonEnergy')
    ex_out_df = ex_out_df.sort_values('CPMU20.photonEnergy')

    energy_m1 = m1_df['CPMU20.photonEnergy']
    m1_hfwhm = m1_df['HorizontalFocusFWHM']

    energy_ex_in = ex_in_df['CPMU20.photonEnergy']
    ex_in_vfwhm = ex_in_df['VerticalFocusFWHM']

    energy_ex_out = ex_out_df['CPMU20.photonEnergy']
    ex_out_bw = ex_out_df['Bandwidth']

    axs[0].plot(energy_m1, m1_hfwhm, marker='o', label=label)
    axs[1].plot(energy_ex_in, ex_in_vfwhm, marker='o', label=label)
    axs[2].plot(energy_ex_out, ex_out_bw, marker='o', label=label)

axs[0].set_ylabel('M1_hor_foc Horizontal FWHM [mm]')
axs[0].set_title('Horizontal FWHM at M1_hor_foc vs Energy')
axs[0].grid(True, alpha=0.3)
axs[0].legend()

axs[1].set_ylabel('ExitSlit Incoming Vertical FWHM [mm]')
axs[1].set_title('Vertical FWHM at ExitSlit RawRaysIncoming vs Energy')
axs[1].grid(True, alpha=0.3)
axs[1].legend()

axs[2].set_xlabel('Photon Energy [eV]')
axs[2].set_ylabel('ExitSlit Outgoing Bandwidth [eV]')
axs[2].set_title('Bandwidth at ExitSlit RawRaysOutgoing vs Energy')
axs[2].grid(True, alpha=0.3)
axs[2].legend()

plt.tight_layout()

out_png = os.path.join(base_dir, 'results', 'plots', 'eval_fwhm_bandwidth_vs_energy.png')
plt.savefig(out_png, dpi=180)
# plt.show()

print('Saved figure:', out_png)
