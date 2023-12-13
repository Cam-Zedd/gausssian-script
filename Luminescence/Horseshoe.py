# -*- coding: utf-8 -*-

"""
CIE Chromaticity Diagrams Plotting
==================================
Necessary package: colour science 

via pip:
pip install colour-science

or 

https://pypi.org/project/colour-science/
https://github.com/colour-science/colour/
"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import colour
from colour.plotting import *
import numpy as np
import pandas as pd
#import pyvalence_kernel.basic_functions as bf

SMALL_SIZE = 24
BIGGER_SIZE = 28
plt.rcParams.update({'font.size': SMALL_SIZE,
                     'axes.titlesize': BIGGER_SIZE, 'axes.edgecolor': 'black', 'axes.labelsize': BIGGER_SIZE, 'axes.linewidth': 2,
                     'xtick.labelsize': SMALL_SIZE, 'xtick.major.size': 10, 'xtick.major.width': 2, 'lines.markersize': 10, 'patch.linewidth': 3.0,
                     'ytick.labelsize': SMALL_SIZE, 'ytick.major.size': 10, 'ytick.major.width': 2, 'ytick.minor.size': 6, 'ytick.minor.width': 1})

#direc = './'  # YOUR PATH
#filename = 'creneau_rouge.csv'  # YOUR FILENAME

########################################################################
#                       AUXILIARY FUNCTIONS
########################################################################
# CIE1931
#cie = np.loadtxt('./CIE1931.csv', delimiter=',')  # LOAD CIE BASE FUNCTIONS

# Linear interpolation


#def lin_int(grid, fpoints, x):
#    try:
#        return fpoints[list(grid).index(x)]
#    except ValueError:
#        try:
#            k = [x <= xk for xk in grid].index(True)  # xk-1<x<xk
#        except ValueError:
#            return 0
#        if (k > 0) and k < len(grid):
#            return fpoints[k-1]+(x-grid[k-1])*(fpoints[k]-fpoints[k-1])/(grid[k]-grid[k-1])
#        else:
#            return 0
#
## Indicator function
#
#
#def ind(x0, x1, x):
#    if (x0 <= x) and (x <= x1):
#        return True
#    else:
#        return False
#
#########################################################################
##                       MAIN FUNCTION
#########################################################################
#
#
#def spectrum_to_cie(simulation, gridheader, spectrheader, energy=True, plot=False, wlmin=400, wlmax=800):
#    '''
#    Calculates the CIE coordinates from the given spectrum using Beck's procedure doi.org/10.1002/qua.20326.
#    Parameters
#    ----------
#    simulation : spectrum as a pandas dataframe.
#    gridheader : wavelength/energy header as a string.
#    spectrheader : intensity header as a string.
#    energy : True if intensity vs energy, False if vs wavelength.
#    plot : boolean, if True display spectrum.
#    wlmin : minimum of wavelength range for integration.
#    wlmin : maximum of wavelength range for integration.
#    -------
#    tuple
#        X, Y, Z in CIE coordinates.
#    Example
#    --------
#    >>> spectrum_to_cie(exptemp1, 'lambda','I', False, False, 400, 800)
#    '''
#    print('Integration from ', wlmin, 'to ', wlmax, 'nm.')
#    if energy is True:
#        simulation = simulation.sort_values(by=0, ascending=False)
#        simulation = simulation.reset_index(drop=True)
#        wavegrid = (1240/simulation[gridheader])  # wavelength grid
#    else:
#        wavegrid = simulation[gridheader]
#    dlambda = wavegrid[1:]-wavegrid[:-1]
#    norm_spectr = simulation[spectrheader]/max(simulation[spectrheader])
#    treated_spectr = max(norm_spectr)-min(norm_spectr)-norm_spectr
#    if plot is True:
#        labels = ['X', 'Y', 'Z']
#        for i in range(1, 4):
#            fig = plt.figure()
#            ax1 = fig.add_subplot(311)
#            ax2 = fig.add_subplot(312)
#            ax3 = fig.add_subplot(313)
#            fig.show()
#            ax1.set_title('%s (CIE)' % labels[i-1], fontsize=30)
#            ax2.set_title('sim spectrum', fontsize=30)
#            ax3.set_title('%s*spectr' % labels[i-1], fontsize=30)
#            ax1.plot(wavegrid, [lin_int(cie[:, 0], cie[:, i], dwave)
#                     for dwave in wavegrid], lw=3)
#            ax2.plot(wavegrid, [lin_int(wavegrid, norm_spectr, dwave)
#                     for dwave in wavegrid], "--", lw=3)
#            ax2.plot(wavegrid, [lin_int(wavegrid, treated_spectr, dwave)
#                     for dwave in wavegrid], lw=3)
#            ax3.plot(wavegrid, [lin_int(cie[:, 0], cie[:, i], dwave)*lin_int(
#                wavegrid, treated_spectr, dwave) for dwave in wavegrid], lw=3)
#            for ax in [ax1, ax2, ax3]:
#                ax.set_xlim(wlmin, wlmax)
#    return [sum([ind(wlmin, wlmax, dwave)*lin_int(cie[:, 0], cie[:, i], dwave)*lin_int(wavegrid, treated_spectr, dwave) for dwave in range(wlmin, wlmax, 1)]) for i in range(1, 4)]
#
########################################################################
#                     PLOT IN CIE COORDINATES
########################################################################


# Read spectrum CSV
#spectrum = pd.read_csv(direc+filename, header=None,
#                       delim_whitespace=False, sep=",", verbose=True)
#print('Fichier contenant le spectre : ' + direc+filename)
##print('Spectrum = :' + spectrum)
## Plot the *CIE 1931 Chromaticity Diagram*.
## integrate intensity from 360 nm to 760 nm in this case
#xex, yex, zex = spectrum_to_cie(spectrum, 0, 1, False, False, 590, 760)
#print(xex)
#print(yex)
#print(zex)


fig, ax = plot_chromaticity_diagram_CIE1931(
    standalone=False, show_spectral_locus=True)
#ax.plot(xex/(xex+yex+zex),yex/(xex+yex+zex), 'o', color='red', label='RED')
ax.plot(0.164806, 0.095083, 's', color='black', label='Exp.')
ax.plot(0.171971, 0.120323, 's', color='red', label='Sim.')
#ax.plot(0.26, 0.35, 'd', color='black', label='Exp. 77K')
#ax.plot(0.35, 0.50, 's', color='black', label='Exp. 298K')
#ax.plot(0.26, 0.32, 'd', color='red', label='Sim. $T_1 + T_2$')
#ax.plot(0.39, 0.56, 's', color='red', label='Sim. $T_1$')
#print('Coordonee 1 : ')
#print(xex/(xex+yex+zex))
#print('Coordonee 2 : ')
#print(yex/(xex+yex+zex))
ax.set_title('')
plt.xlim(-0.1, 0.85)
plt.ylim(-0.05, 0.9)
plt.xticks(np.arange(0, 1, 0.2))
legend = ax.legend(loc='upper right', frameon=False)  # , fontsize='x-large')
plt.tight_layout()
plt.show()
