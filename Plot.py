import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.optimize import curve_fit

def sigmoid_model(x, bottom, top, IC50, hill):
    return bottom + (top - bottom)/(1 + np.power(IC50/x, hill))

def plot_curve(data, ax, compound, yticks, norm_swtich, text_pos, fontsizes):
    # Plot the IC50 curve of one compound.
    # The input data should not contain the max nor the min values.
    conc = data.columns
    mean = data.loc['Mean']
    stdev = data.loc['Stdev']
    # Plotting the data
    ax.errorbar(conc, mean, stdev, color = 'b', fmt = 'o', capsize = 6)
    # Fit the curve with sigmoidal model.
    try:
        popt, pcov = curve_fit(sigmoid_model, conc, mean, sigma = stdev)
        perr = np.sqrt(np.diag(pcov))
        x_calc = 1.5*conc[0]*np.ones(100)/np.power(3, np.linspace(0, 10, 100))
        y_calc = sigmoid_model(x_calc, *popt)
        ax.plot(x_calc, y_calc)
        if popt[2] >= perr[2]:
            text = ('IC50 = ' + str('%.2f ' % popt[2]) + u'\u00B1 ' + str('%.2f ' % perr[2]) + ' nM\n' +
                    'Hill slope = ' + str('%.2f ' % popt[3]) + u'\u00B1 ' + str('%.2f ' % perr[3]))
        else:
            text = 'Data could not be reliably fitted.'
        ax.text(text_pos[0], text_pos[1], text, fontsize = fontsizes['text'], transform=plt.gcf().transFigure)
    except:
        pass
    # Set figure styles
    ax.set_xscale('log')
    ax.set_yticks(yticks)
    ax.tick_params(labelsize = fontsizes['ticks'])
    ax.set_title(compound, fontsize = fontsizes['title'])
    ax.set_xlabel('Concentration (nM)', fontsize = fontsizes['xlabel'])
    if norm_swtich == True:
        ax.set_ylabel('Normalized BCL6 activity %', fontsize = fontsizes['ylabel'])
    else:
        ax.set_ylabel('TR-FRET ratio x 1000', fontsize = fontsizes['ylabel'])
    
    
