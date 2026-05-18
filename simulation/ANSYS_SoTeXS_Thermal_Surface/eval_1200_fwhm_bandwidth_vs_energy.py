import os
import pandas as pd
import matplotlib.pyplot as plt

base_dir = os.path.dirname(os.path.abspath(__file__))
cases = [
    ('1200_nodef', 'RAYPy_Simulation_ansys_1200_pt_nodef'),
    ('1200_profile001', 'RAYPy_Simulation_ansys_1200_pt_profile001'),
    ('1200_profile002', 'RAYPy_Simulation_ansys_1200_pt_profile002'),
    ('1200_profile003', 'RAYPy_Simulation_ansys_1200_pt_profile003'),
    ('1200_profile004', 'RAYPy_Simulation_ansys_1200_pt_profile004'),
]
fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
for label, folder in cases:
    m1_df = pd.read_csv(os.path.join(base_dir, folder, 'M1_hor_foc_RawRaysOutgoing.csv')).sort_values('CPMU20.photonEnergy')
    ex_in_df = pd.read_csv(os.path.join(base_dir, folder, 'ExitSlit_RawRaysIncoming.csv')).sort_values('CPMU20.photonEnergy')
    ex_out_df = pd.read_csv(os.path.join(base_dir, folder, 'ExitSlit_RawRaysOutgoing.csv')).sort_values('CPMU20.photonEnergy')
    axs[0].plot(m1_df['CPMU20.photonEnergy'], m1_df['HorizontalFocusFWHM'], marker='o', label=label)
    axs[1].plot(ex_in_df['CPMU20.photonEnergy'], ex_in_df['VerticalFocusFWHM'], marker='o', label=label)
    axs[2].plot(ex_out_df['CPMU20.photonEnergy'], ex_out_df['Bandwidth'], marker='o', label=label)
axs[0].set_ylabel('M1_hor_foc Horizontal FWHM [mm]'); axs[0].grid(True, alpha=0.3); axs[0].legend(); axs[0].set_title('1200: Horizontal FWHM at M1_hor_foc')
axs[1].set_ylabel('ExitSlit Incoming Vertical FWHM [mm]'); axs[1].grid(True, alpha=0.3); axs[1].legend(); axs[1].set_title('1200: Vertical FWHM at ExitSlit Incoming')
axs[2].set_xlabel('Photon Energy [eV]'); axs[2].set_ylabel('ExitSlit Outgoing Bandwidth [eV]'); axs[2].grid(True, alpha=0.3); axs[2].legend(); axs[2].set_title('1200: Bandwidth at ExitSlit Outgoing')
plt.tight_layout()
out_png = os.path.join(base_dir, 'results', 'plots', 'eval_1200_fwhm_bandwidth_vs_energy.png')
plt.savefig(out_png, dpi=180)
# plt.show()
print('Saved figure:', out_png)
