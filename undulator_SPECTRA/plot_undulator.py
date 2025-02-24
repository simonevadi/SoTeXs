import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
from edges import all_elements

und = pd.read_csv('CPMU20-6mm.csv', sep=',')

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
from edges import all_elements

und = pd.read_csv('CPMU20-6mm.csv', sep=',')

# Set larger font sizes
plt.rcParams.update({'font.size': 20})  # Adjusts the base font size
plt.rcParams.update({'axes.labelsize': 20})  # X and Y labels
plt.rcParams.update({'axes.titlesize': 22})  # Title
plt.rcParams.update({'xtick.labelsize': 14})  # X tick labels
plt.rcParams.update({'ytick.labelsize': 20})  # Y tick labels


# plot all elements
fig, (axs) = plt.subplots(1, 1,figsize=(24,12))


ax=axs
for harm in [1,3,5,7,9]:
    ax.plot(und[f'Harmonic Energy (eV){harm}'],
             und[f'Harmonic: {harm}'],
             label=f'Harmonic {harm}')
ax.set_xlabel('Energy [eV]')
ax.set_ylabel('Photons/sec/0.1Amp')

colors = [
    'red', 'orange', 'yellow', 'pink', 'magenta', 'cyan', 'lightblue',
    'blue', 'green', 'purple', 'brown', 'black', 'white', 'gray',
    'violet', 'turquoise', 'indigo', 'teal', 'lavender', 'gold',
    'silver', 'beige', 'maroon'
]

colors = sns.color_palette("viridis", 23)

# Retrieve the current y-axis limits
ymin, ymax = ax.get_ylim()

# Plot rectangles for each element range
index=0
for element in all_elements.keys():
    element_dict = all_elements[element]
    for edge_index in element_dict.keys():

        edge_dict = element_dict[edge_index]
        edge  = edge_dict['Energy[eV]']
        start = edge - 10
        end   = edge + 50
        priority  = edge_dict['Priority']
        if priority == 1:
            priority = 0.9
        else:
            priority = 0.3

        # Calculate the width of the rectangle
        width = end - start

        # Create a rectangle patch with a low alpha for transparency
        rect = Rectangle((start, ymin), width, ymax-ymin,
                        color=colors[index], alpha=priority, 
                        label=f'{element}: {start}-{end} eV')
        ax.add_patch(rect)
        ax.axvline(edge, ymin=ymin, ymax=ymax, linestyle='dashed')
        index+=1


ax.set_xlim(0,6000)
# Add labels, title, or other formatting as needed
ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=14)


# Create a twin x-axis on top and add sorted element labels at their edge positions
edges_info = []
for element, edges in all_elements.items():
    for edge_type, data in edges.items():
        edges_info.append((data["Energy[eV]"], f'{element} ({edge_type})'))

# Sort the edges by their energy value
edges_info.sort(key=lambda x: x[0])
edge_positions, edge_labels = zip(*edges_info)

ax_top = ax.twiny()
ax_top.set_xlim(ax.get_xlim())
ax_top.set_xticks(edge_positions)

ax_top.set_xticklabels(edge_labels, rotation=45, ha='center')
for label in ax_top.get_xticklabels():
    print(label.get_text())
    if label.get_text() == "Fe (L3)" or label.get_text() == "Mo (L3)":
        label.set_y(1.05)  # Adjust this value as needed to move it upward

ax_top.set_xlabel("Element Edge Positions")


plt.tight_layout()
plt.savefig('CMPU20_harmonics_all_elements.png')
# plt.show()








