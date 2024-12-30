from Data_processing import read_plate_layout, raw_data_to_FRET_ratio, split_by_compound
from Plot import plot_curve
import matplotlib.pyplot as plt
import numpy as np

# Set file path
data_path = 'Data_08052024/Data_08052024.xlsx'
layout_path = 'Data_08052024/Layout_08052024.xlsx'
output_dir = 'Data_08052024/'

# Set the first and the last row
start = 3
end = 14

# Normalize or not?
norm_switch = True

# Specify plot options:
yticks = np.arange(-25, 151, 25)
text_pos = [0.15, 0.15]
fontsizes = {'text': 14,
             'xlabel': 14,
             'ylabel': 14,
             'ticks': 12,
             'title': 20}

FRET_ratio = raw_data_to_FRET_ratio(data_path, start, end)
layout_colors, color_dict, layout_concentrations = read_plate_layout(layout_path, start, end)
data_by_compound = split_by_compound(FRET_ratio, layout_colors, layout_concentrations, color_dict, normalize = norm_switch)

for compound in data_by_compound.keys():
    print(compound + '\n')
    print(data_by_compound[compound])
    print('\n')
    data_by_compound[compound].to_csv(output_dir + compound + '.csv')



for i, compound in enumerate(data_by_compound.keys()):
    fig, ax = plt.subplots()
    data = data_by_compound[compound].iloc[:,0:10]
    plot_curve(data, ax, compound, yticks, norm_switch, text_pos, fontsizes)
plt.show()