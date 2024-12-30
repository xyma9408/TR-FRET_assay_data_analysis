import pandas as pd
import numpy as np
from openpyxl import load_workbook

def read_plate_layout(path, start = 1, end = 16):
    # Given the path for plate layout xlsx in correct format and returns the following:
    # 1. The plate layout as a numpy 2D-array with hexadecimal color codes;
    # 2. The compound name each hexadecimal color code stands for in a dictionary;
    # 3. The concentration layout as a numpy 2D-array.
    layout_wb = load_workbook(path)
    layout = layout_wb['layout']
    legend = layout_wb['legend']
    layout_colors = []
    layout_concentrations = []
    cells = layout['A' + str(start) : 'X' + str(end)]
    for i in range(end - start + 1):
        row_colors = []
        row_concentration = []
        for j in range(24):
            if cells[i][j].fill.start_color.type == 'theme':
                row_colors.append('Theme=' + str(cells[i][j].fill.start_color.theme) + ' tint=' 
                                  + str(cells[i][j].fill.start_color.tint))
            elif cells[i][j].fill.start_color.type == 'rgb':
                row_colors.append(str(cells[i][j].fill.start_color.rgb))
            else:
                row_colors.append('None')
            row_concentration.append(float(cells[i][j].value))
        layout_colors.append(row_colors)
        layout_concentrations.append(row_concentration)
    layout_colors = np.array(layout_colors)
    layout_concentrations = np.array(layout_concentrations)
    # Now process legends
    num_colors = len(legend['A'])
    color_dict = {}
    for i in range(num_colors):
        if legend['A'][i].fill.start_color.type == 'theme':
            color_dict['Theme=' + str(legend['A'][i].fill.start_color.theme) + ' tint=' 
                                  + str(legend['A'][i].fill.start_color.tint)] = legend['B'][i].value
        elif legend['A'][i].fill.start_color.type == 'rgb':
            color_dict[str(legend['A'][i].fill.start_color.rgb)] = legend['B'][i].value
        else:
            color_dict['None'] = legend['B'][i].value
    return layout_colors, color_dict, layout_concentrations

def raw_data_to_FRET_ratio(path, start = 1, end = 16):
    # Given the path for raw data xlsx in correct forat and returns the 1000x FRET ratio
    # as a numpy 2D-array
    raw_data = pd.read_excel(path)
    plate_data = raw_data.iloc[34:66, 2:26].reset_index(drop = True)
    em_620 = plate_data[plate_data.index % 2 == 0].reset_index(drop = True)
    em_665 = plate_data[plate_data.index % 2 == 1].reset_index(drop = True)
    FRET_ratio = (np.array(em_665)/np.array(em_620)*1000)[start-1:end, :]
    return FRET_ratio

def split_by_compound(FRET_ratio, layout_colors, layout_concentrations, color_dict, normalize = False):
    # Split the FRET_ratio data into data for each compound as a dictionary, where the
    # keys are the compound names and the values are the data for that compound as a pandas
    # DataFrame with x columns (x represent the number of concentrations) and y + 2 rows 
    # (y represent the number of replicates) with the 'mean' and 'stdev' row being the 
    # mean and standard deviation of each concentration.
    data_by_compound = {}
    for color in color_dict.keys():
        tempdata = FRET_ratio[layout_colors == color]
        concentrations = layout_concentrations[layout_colors == color]
        conc_set = list(set(concentrations))
        conc_set.sort(reverse = True)
        num_conc = len(conc_set)
        num_rep = int(len(tempdata)/num_conc)
        concentrations_data = np.zeros((num_conc, num_rep))
        for i in range(num_conc):
            conc_data = tempdata[concentrations == conc_set[i]]
            concentrations_data[i] = conc_data
        concentrations_data = pd.DataFrame(data = concentrations_data.transpose(), columns = conc_set)
        # If normalization is required
        if normalize == True:
            max = concentrations_data[0]
            min = concentrations_data[-1]
            for i in range(num_conc):
                concentrations_data.iloc[:,i] = (concentrations_data.iloc[:,i] - min)/(max - min) * 100
        # End of normalization
        concentrations_data.loc['Mean'] = concentrations_data.mean()
        concentrations_data.loc['Stdev'] = concentrations_data.std()
        data_by_compound[color_dict[color]] = concentrations_data
    return data_by_compound
