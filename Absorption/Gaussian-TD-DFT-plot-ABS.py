#!python3
# -*- coding: utf-8 -*-
### import
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
import sys


##################################### file read #################################
### read the file and store the data
excitation=[] #declare
for line in open(sys.argv[1], "r"): #open file, read, for line sys.argv[1] is my argument
	if "Excited State  " in line: #let's find what we need
		print(line.split()) #print all the required data on prompt for user
		eV = float(line.split()[4]) #float
		nm=float(line.split()[6])#float
		# Trouver la partie contenant "f=" et extraire la valeur numérique après "f="
		for part in line.split():
			if "f=" in part:
				f = float(part.split("=")[1])
				break #pour sortir de la boucle et empêcher le "none"
			else:
				f = ""
		excitation.append([eV,nm,f]) #let's stock everyone  ##array
		#print(eV) #print all value of eV through the loop
print(excitation)
	
### change to an nparray and  transpose for plotting
excitation=np.array(excitation) #prepare for plot and transpose
excplot=excitation.transpose() #new variable for plotting


### Gaussian function
'''
Adapted from Michael Dommett code
'''
def spec(E,f,sigma,x):
    spectrum=[]
    for E1 in x:
        tot=0
        for E2,os in zip(E,f):
            tot+=os*np.exp(-((((E2-E1)/sigma)**2)))
        spectrum.append(tot)
    return spectrum #prepare spectrum for the values to be plotted

### set up the min and max value for x plot
mineV=np.amin(excplot[0])
maxeV=np.amax(excplot[0])
minnm=np.amin(excplot[1])
maxnm=np.amax(excplot[1])

### x and sigma	change sigma for HWHM
x=np.linspace(mineV/1.1,maxeV*1.1,num=2000)
try: 
	sigma=float(sys.argv[2])
except: #IndexError
	sigma=0.1
### plot
#Cam's layout
SMALL_SIZE = 18
BIGGER_SIZE = 22
plt.rcParams.update({'font.size': SMALL_SIZE,
					 'axes.titlesize':BIGGER_SIZE, 'axes.edgecolor':'black','axes.labelsize':BIGGER_SIZE, 'axes.linewidth':2,
					 'xtick.labelsize':SMALL_SIZE, 'xtick.major.size':10, 'xtick.major.width':2, 'lines.markersize':10,'patch.linewidth':3.0,
					 'ytick.labelsize':SMALL_SIZE, 'ytick.major.size':10, 'ytick.major.width':2, 'ytick.minor.size':6, 'ytick.minor.width':1})


#######plot in eV
fig1, ax = plt.subplots()
spectrum=spec(excplot[0],excplot[2],sigma,x)
ax.plot(x,spectrum,"--k")
ax.vlines(excplot[0], 0, excplot[2], label='TD-DFT oscillator strengths', color='r', lw=2, linestyles='solid')
ax.set_xlim(mineV/1.1,maxeV*1.1)
ax.set_ylim(0,max(spectrum)*1.1)
ax.legend(loc='upper left', frameon=False)
ax.set_xlabel(r"Energy (eV)")
ax.set_ylabel(r"f (oscillator strength)")


#######plot in nm
fig2,ax2 = plt.subplots()
ax2.vlines(excplot[1], 0, excplot[2], label='TD-DFT oscillator strengths', color='b', lw=2, linestyles='solid')
ax2.plot(1240/x,spectrum,"--k")
ax2.set_xlim(minnm/1.1,maxnm*1.1)
ax2.set_ylim(0,max(spectrum)*1.1)
ax2.legend(loc='upper left', frameon=False)
ax2.set_xlabel(r" $\lambda$ (nm)")
ax2.set_ylabel(r"f (oscillator strength)")


plt.show()