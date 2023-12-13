#!python3
# -*- coding: utf-8 -*-

'''
Code to plot anharmonic IR and RAMAN spectra from G16

###### What you need to modify ####

filetoparser = files to be read (list)
name = names to give in the plot (list)
sigma or valsigma = value for gaussian/lorentzian shapes

'''

# Modules

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time

######### Timings #########

start_time = time.time()

######## CAM's LAYOUT #########

SMALL_SIZE = 24
BIGGER_SIZE = 32
plt.rcParams.update({'font.size': SMALL_SIZE,
                     'axes.titlesize': BIGGER_SIZE,
                     'axes.edgecolor': 'black',
                     'axes.labelsize': BIGGER_SIZE,
                     'axes.linewidth': 2,
                     'xtick.labelsize': SMALL_SIZE,
                     'xtick.major.size': 10,
                     'xtick.major.width': 2,
                     'lines.markersize': 10,
                     'patch.linewidth': 3.0,
                     'ytick.labelsize': SMALL_SIZE,
                     'ytick.major.size': 10,
                     'ytick.major.width': 2,
                     'ytick.minor.size': 6,
                     'ytick.minor.width': 1})
plt.rcParams['axes.xmargin'] = 0


######### FILES TO BE READ #########

filetoparser = ["optim-PBE0-S0-FREQ-ANH-RAMAN-double.log"]

######### COMPOUND NAMES #########

name = [r"PBE", r"PBE0", r"Mgo", r"IR-alone", r"TiO2_rutile"]

######### START THE LISTS #########

energycm, IRintensityharm, IRintensityanh, intens, energyRaman, Ramanintensityharm, Ramanintensityanh, intensityRamanTot, maxintensity, maxintensityRamanTot, mincm, maxcm, minraman, maxraman = (
    [[]for _ in range(len(filetoparser))] for _ in range(14))

######### Colors #########

c = [
    "dodgerblue",
    "coral",
    "seagreen",
    "darkorchid",
    "red",
    "dimgrey",
    "orangered",
    "peru",
    "limegreen",
    "slateblue",
]

######### Gaussian function #########


def spec(E, f, sigma, x):
    E = np.array(E)
    f = np.array(f)
    x = np.array(x)

    # Compute the spectrum using vectorized operations
    delta_E = (E - x[:, np.newaxis]) / sigma
    spectrum = np.sum(f * np.exp(-delta_E**2), axis=1)

    return spectrum


def plot_lorentzian(E, f, sigma, x):
    E = np.array(E)
    f = np.array(f)
    x = np.array(x)
    spectrum_lz = np.sum(f / np.pi * sigma /
                         ((E - x[:, np.newaxis])**2 + sigma**2), axis=1)
    return spectrum_lz


sigma = 5
valsigma = [10, 10]
num = 5000  # linspace


######### FILES TO BE READ #########

fig3, ax3 = plt.subplots()  # IR
fig1, ax1 = plt.subplots()  # RAMAN

for i in range(len(filetoparser)):
    with open(filetoparser[i], 'r') as f:
        # FIRST for IR
        print(f"gathering IR data for file:{filetoparser[i]}")
        line = f.readline()
        while "Anharmonic Infrared Spectroscopy" not in line:
            line = f.readline()
        line = f.readline()
        while "Mode(n)" not in line:
            line = f.readline()
        line = f.readline()
        print("1st line of fundamentals",)
        print(line)
        while not line.isspace():  # seek the space
            energycm[i].append(float(line.split()[2]))
            IRintensityharm[i].append(float(line.split()[3]))
            IRintensityanh[i].append(float(line.split()[4]))
            line = f.readline()
        line = f.readline()
        while "Mode(n)" not in line:
            line = f.readline()
        line = f.readline()
        print("1st line of overtones ",)
        print(line)
        while not line.isspace():  # seek the space
            energycm[i].append(float(line.split()[-2]))
            IRintensityanh[i].append(float(line.split()[-1]))
            line = f.readline()
        line = f.readline()
        while "Mode(n)" not in line:
            line = f.readline()
        line = f.readline()
        print("1stline of CB ",)
        print(line)
        while not line.isspace():  # seek the space
            energycm[i].append(float(line.split()[-2]))
            IRintensityanh[i].append(float(line.split()[-1]))
            line = f.readline()
        line = f.readline()

        #################### PLOT IR ###############

        print("for file", filetoparser[i])
        mincm[i] = min(energycm[i])
        maxcm[i] = max(energycm[i])
        maxintensity[i] = max(IRintensityanh[i])
        x = np.linspace(0.01, maxcm[i] * 1.2, num)
        print("for file", filetoparser[i], "named", name[i])
        print("Starting to plot IR")
        spectrum = spec(energycm[i], IRintensityanh[i], sigma, x)
        ax3.plot(
            x,
            spectrum /
            np.max(spectrum),
            "-",
            label=f"{name[i]}",
            color=c[i],
            lw=3)
        print(
            f"IR spectrum of {name[i]} achieved in :"
            "%s seconds" %
            (time.time() - start_time))
        # Store IR in CSV
        fname = filetoparser[i]
        with open(f"{fname}-IR.csv", "w") as g:
            g.write("E(cm-1),I")
            for o in range(num):
                g.write(f'\n{x[o]},{spectrum[o]/spectrum.max()}')

        # RAMAN
        if "Raman" or "RAMAN" in line:
            print(f"gathering RAMAN data for file:{filetoparser[i]}")
            while "Anharmonic Raman Spectroscopy" not in line:
                line = f.readline()
            line = f.readline()
            while "Mode(n)" not in line:
                line = f.readline()
            line = f.readline()
            print("1st line of fundamentals",)
            print(line)
            while not line.isspace():  # seek the space
                energyRaman[i].append(float(line.split()[2]))
                Ramanintensityharm[i].append(float(line.split()[3]))
                Ramanintensityanh[i].append(float(line.split()[4]))
                line = f.readline()
            line = f.readline()
            while "Mode(n)" not in line:
                line = f.readline()
            line = f.readline()
            print("1st line of overtones ",)
            print(line)
            while not line.isspace():  # seek the space
                energyRaman[i].append(float(line.split()[-2]))
                Ramanintensityanh[i].append(float(line.split()[-1]))
                line = f.readline()
            line = f.readline()
            while "Mode(n)" not in line:
                line = f.readline()
            line = f.readline()
            print("1stline of CB ",)
            print(line)
            while not line.isspace():  # seek the space
                energyRaman[i].append(float(line.split()[-2]))
                Ramanintensityanh[i].append(float(line.split()[-1]))
                line = f.readline()
            line = f.readline()

            # Starting RAMAN
        print("for file", filetoparser[i])
        minraman[i] = np.min(energyRaman[i])
        maxraman[i] = np.max(energyRaman[i])
        maxintensity[i] = max(Ramanintensityanh[i])
        x = np.linspace(0.01, maxcm[i] * 1.2, num)
        print("for file", filetoparser[i], "named", name[i])
        print("Starting to plot RAMAN")
        spectrum = spec(energyRaman[i], Ramanintensityanh[i], sigma, x)
        ax1.plot(
            x,
            spectrum /
            np.max(spectrum),
            "-",
            label=f"{name[i]}",
            color=c[i],
            lw=3)
        print(
            f"RAMAN spectrum of {name[i]} achieved in :"
            "%s seconds" %
             (time.time() - start_time))
        # Store IR in CSV
        fname = filetoparser[i]
        with open(f"{fname}-RAMAN.csv", "w") as g:
            g.write("E(cm-1),I")
            for o in range(num):
                g.write(f'\n{x[o]},{spectrum[o]/spectrum.max()}')

maxcm = list(filter(None, maxcm))
maxraman = list(filter(None, maxraman))


ax3.legend(loc='upper left', frameon=False)
ax3.set_xlim(0, max(maxcm) * 1.1)
ax3.set_ylim(0, 1.05)
ax3.set_xlabel(r"Energy (cm$^{-1}$)")
ax3.set_ylabel(r"Normalized Intensity")

ax1.legend(loc='upper left', frameon=False)
ax1.set_xlim(0, max(maxraman) * 1.1)
ax1.set_ylim(0, 1.05)
ax1.set_xlabel(r"RAMAN shift (cm$^{-1}$)")
ax1.set_ylabel(r"Normalized Intensity")

print("--- The process took %s seconds ---" % (time.time() - start_time))


plt.show()
