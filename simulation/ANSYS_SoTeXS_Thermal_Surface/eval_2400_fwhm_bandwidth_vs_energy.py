import os
import pandas as pd
import matplotlib.pyplot as plt

base_dir = os.path.dirname(os.path.abspath(__file__))
cases = [
    ('2400_nodef', 'RAYPy_Simulation_ansys_2400_nodef'),
    ('2400_profile001', 'RAYPy_Simulation_ansys_2400_profile001'),
    ('2400_profile002', 'RAYPy_Simulation_ansys_2400_profile002'),
    ('2400_profile003', 'RAYPy_Simulation_ansys_2400_profile003'),
    ('2400_profile004', 'RAYPy_Simulation_ansys_2400_profile004'),
]

fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
for label, folder in cases:
    m1_df = pd.read_csv(os.path.join(base_dir, folder, 'M1_hor_foc_RawRaysOutgoing.csv')).sort_values('CPMU20.photonEnergy')
    ex_in_df = pd.read_csv(os.path.join(base_dir, folder, 'ExitSlit_RawRaysIncoming.csv')).sort_values('CPMU20.photonEnergy')
    ex_out_df = pd.read_csv(os.path.join(base_dir, folder, 'ExitSlit_RawRaysOutgoing.csv')).sort_values('CPMU20.photonEnergy')
    axs[0].plot(m1_df['CPMU20.photonEnergy'], m1_df['HorizontalFocusFWHM'], marker='o', label=label)
    axs[1].plot(ex_in_df['CPMU20.photonEnergy'], ex_in_df['VerticalFocusFWHM'], marker='o', label=label)
    axs[2].plot(ex_out_df['CPMU20.photonEnergy'], ex_out_df['Bandwidth'], marker='o', label=label)
axs[0].set_ylabel('M1_hor_foc Horizontal FWHM [mm]'); axs[0].grid(True, alpha=0.3); axs[0].legend(); axs[0].set_title('2400: Horizontal FWHM at M1_hor_foc')
axs[1].set_ylabel('ExitSlit Incoming Vertical FWHM [mm]'); axs[1].grid(True, alpha=0.3); axs[1].legend(); axs[1].set_title('2400: Vertical FWHM at ExitSlit Incoming')
axs[2].set_xlabel('Photon Energy [eV]'); axs[2].set_ylabel('ExitSlit Outgoing Bandwidth [eV]'); axs[2].grid(True, alpha=0.3); axs[2].legend(); axs[2].set_title('2400: Bandwidth at ExitSlit Outgoing')
plt.tight_layout()
out_png = os.path.join(base_dir, 'results', 'plots', 'eval_2400_fwhm_bandwidth_vs_energy.png')
plt.savefig(out_png, dpi=180)
print('Saved figure:', out_png)

fig2, ax2 = plt.subplots(figsize=(8, 6))
case_colors = plt.cm.tab10.colors
for i, (label, folder) in enumerate(cases):
    det_file = os.path.join(base_dir, folder, 'DetectorAtFocus_RawRaysOutgoing.csv')
    if not os.path.exists(det_file):
        raise FileNotFoundError(f'Missing required file: {det_file}')
    det_df = pd.read_csv(det_file)
    avg_hc = det_df['HorizontalCenter'].mean()
    avg_vc = det_df['VerticalCenter'].mean()
    ax2.scatter(
        avg_hc,
        avg_vc,
        color=case_colors[i % len(case_colors)],
        s=90,
        alpha=0.9,
        edgecolors='none',
        label=label,
    )

ax2.set_xlabel('HorizontalCenter [mm]')
ax2.set_ylabel('VerticalCenter [mm]')
ax2.set_title('2400: DetectorAtFocus center scatter (colored by energy)')
ax2.grid(True, alpha=0.3)
ax2.legend()
fig2.tight_layout()
out_png2 = os.path.join(base_dir, 'results', 'plots', 'eval_2400_detector_center_scatter.png')
fig2.savefig(out_png2, dpi=180)
print('Saved figure:', out_png2)


fig3, axs3 = plt.subplots(2, 1, figsize=(9, 8), sharex=True)
for i, (label, folder) in enumerate(cases):
    det_file = os.path.join(base_dir, folder, 'DetectorAtFocus_RawRaysOutgoing.csv')
    if not os.path.exists(det_file):
        raise FileNotFoundError(f'Missing required file: {det_file}')
    det_df = pd.read_csv(det_file).sort_values('CPMU20.photonEnergy')
    color = case_colors[i % len(case_colors)]
    axs3[0].plot(det_df['CPMU20.photonEnergy'], det_df['HorizontalFocusFWHM'], marker='o', color=color, label=label)
    axs3[1].plot(det_df['CPMU20.photonEnergy'], det_df['VerticalFocusFWHM'], marker='o', color=color, label=label)

axs3[0].set_ylabel('HorizontalFocusFWHM [mm]')
axs3[0].set_title('2400: DetectorAtFocus Horizontal FWHM vs Energy')
axs3[0].grid(True, alpha=0.3)
axs3[0].legend()

axs3[1].set_xlabel('Photon Energy [eV]')
axs3[1].set_ylabel('VerticalFocusFWHM [mm]')
axs3[1].set_title('2400: DetectorAtFocus Vertical FWHM vs Energy')
axs3[1].grid(True, alpha=0.3)
axs3[1].legend()

fig3.tight_layout()
out_png3 = os.path.join(base_dir, 'results', 'plots', 'eval_2400_detector_focus_fwhm_vs_energy.png')
fig3.savefig(out_png3, dpi=180)
print('Saved figure:', out_png3)
