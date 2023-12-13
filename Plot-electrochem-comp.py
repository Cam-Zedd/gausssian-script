#!python3
# -*- coding: utf-8 -*-
# %matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time
from scipy.optimize import curve_fit

start_time = time.time()

# plot parameters
SMALL_SIZE = 26
BIGGER_SIZE = 32
plt.rcParams.update({'font.size': SMALL_SIZE,
                     'axes.titlesize': BIGGER_SIZE,
                     'axes.edgecolor': 'black',
                     'axes.labelsize': BIGGER_SIZE,
                     'axes.linewidth': 2,
                     'xtick.labelsize': SMALL_SIZE,
                     'xtick.major.size': 10,
                     'xtick.major.width': 2,
                     'lines.markersize': 8,
                     'patch.linewidth': 3.0,
                     'ytick.labelsize': SMALL_SIZE,
                     'ytick.major.size': 10,
                     'ytick.major.width': 2,
                     'ytick.minor.size': 6,
                     'ytick.minor.width': 1})
plt.rcParams['axes.xmargin'] = 0

# complex names
complexes = ['allthenames...', 'IrL2', 'IrL3', 'IrL4', 'IrL5', 'IrL6', 'IrL7', 'IrL8',
             'IrL9', 'IrL10']

# data
calc = [
    [-5.70,
     -5.82,
     -5.83,
     -5.54,
     -5.96,
     -5.59,
     -6.10,
     -5.41,
     -5.72,
     -5.76, ],  # HOMO
    [-2.51,
     -2.55,
     -2.54,
     -2.49,
     -2.57,
     -2.49,
     -2.61,
     -2.48,
     -2.52,
     -2.56, ],  # LUMO
    [3.20, 3.27, 3.30, 3.06, 3.40, 3.10, 3.49, 2.93, 3.20, 3.20, ],  # GAP
]

exp = [
    [0.89, 0.99, 0.99, 0.86, 1.14, 0.87, 1.23, 0.76, 1.06, 0.98, ],  # OXY
    [-1.87, -1.80, -1.82, -1.84, -1.81, -1.87, -1.75, -1.86, -1.80, -1.81, ],  # RED
    [],  # GAP
]

for i in range(len(exp[0])):
    exp[2].append(exp[0][i] - exp[1][i])  # value of exp gap

# Coefficient R2
"""
*Other way
r_squared = []
for i in range(len(exp)):
    r_squared_i = np.corrcoef(calc[i], exp[i])**2
    r_squared.append("{:.2f}".format(r_squared_i[0, 1]))
"""

r_squared = [
    f"{np.corrcoef(c, e)[0, 1] ** 2:.2f}"
    for c, e in zip(calc, exp)
]

print("--- %s seconds --- until r2" % (time.time() - start_time))

titre = ["Oxydation energy vs. -HOMO", "Reduction energy vs. LUMO",
         "Gap reduction/oxydation vs. computed gap"]

# plot
for j in range(len(exp)):
    fig, ax = plt.subplots()
    for i in range(len(exp[0])):
        plt.scatter(calc[j][i], exp[j][i])
        plt.xlim(min(calc[j]) - 0.05, max(calc[j]) + 0.05)
        plt.xlabel('Computed (eV)')
        plt.ylabel('Experimental (V)')
        ax.set_aspect(1.0 / ax.get_data_ratio(), adjustable='box')
    plt.title(titre[j])
    fit = np.polyfit(calc[j], exp[j], 1) #fit
    p = np.poly1d(fit) #polynome 1D
    labelfit = "{:.4f}".format(fit[0]) + "x + " + "{:.4f}".format(fit[1]) #store p labels
    line1, = ax.plot(calc[j], p(calc[j]), "r--", label = f'{labelfit}') #plot p with legend
    line0, = ax.plot([], [], ' ', label=f'$R^2$= {r_squared[j]}') #plot R2 with legend
    pr_legend = ax.legend(handles = [line1,line0], loc=(1.05, 0), frameon = False) #gather legends
ax.legend(complexes+[line1.get_label()]+[line0.get_label()], loc=(1.05, 0), frameon=False) #gather legends for last
print("--- %s seconds --- before plt(show)" % (time.time() - start_time))
plt.show()