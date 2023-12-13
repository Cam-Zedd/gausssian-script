#!python3
# -*- coding: utf-8 -*-

'''
Code to plot several spectra from Gaussian TD-DFT calculations. 

###### What you need to modify ####

filetoparser = files to be read (list)
name = names to give in the plot (list)
sigma = value for gaussian shapes (taken w.r.t energy)

##### Plot ####
You can remove the normalization 
'''
### import

import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time

######## CAM's LAYOUT

SMALL_SIZE = 24
BIGGER_SIZE = 32
plt.rcParams.update({'font.size': SMALL_SIZE,
					 'axes.titlesize':BIGGER_SIZE, 'axes.edgecolor':'black','axes.labelsize':BIGGER_SIZE, 'axes.linewidth':2,
					 'xtick.labelsize':SMALL_SIZE, 'xtick.major.size':10, 'xtick.major.width':2, 'lines.markersize':10,'patch.linewidth':3.0,
					 'ytick.labelsize':SMALL_SIZE, 'ytick.major.size':10, 'ytick.major.width':2, 'ytick.minor.size':6, 'ytick.minor.width':1})
plt.rcParams['axes.xmargin'] = 0 

####### Timings ########

start_time = time.time()

######## FILES TO BE READ ########

filetoparser = ["1-TDabs.log","2-TDabs.log","3-TDabs.log","4-TDabs.log","5-TDabs.log"] # all the files needed

######## COMPOUND NAMES ######

name = ["1", "2", "3", "4", "5"]

######## START THE LISTS #########

eV, nm, f, minnm, maxnm, mineV, maxeV = ([[]for _ in range(len(filetoparser))] for _ in range(7))

######## Colors #######

c=["dodgerblue","coral","seagreen","darkorchid","red","dimgrey","orangered","peru","limegreen","slateblue","fushia"]

######## Gaussian function

'''
Adapted from Michael Dommett code
'''

def spec(E,f,sigma,x):
    _E = np.array(E) #energy
    _f = np.array(f) #oscillateur strengths (here intensity)
    spectrum=np.zeros((len(x),)) #tuple (n,), matrix with dimension 1 of n length
    for i, E1 in enumerate(x):
        tot =  _f.dot(np.exp(-((((_E-E1)/sigma)**2))))
        spectrum[i] = tot
    return spectrum #prepare spectrum for the values to be plotted
sigma=0.1	
#valsigma=[0.1, 0.3, 0.5, 0.7, 0.1]

######## LOOP OVER THE FILES TO FILL THE LISTS AND PLOT ########

fig,ax1 = plt.subplots()
for i in range(len(filetoparser)):
	for line in open(filetoparser[i], "r"):
		if "Excited State  " in line: #let's find what we need
			#print(line.split()) #print all the required data on prompt for user
			eV[i].append(float(line.split()[4])) 
			nm[i].append(float(line.split()[6]))
			f[i].append(float(line.split("f=")[1][:5]))#("f=")[1]) #float
	minnm[i] = min(nm[i]) #one value, no need a list of list
	maxnm[i] = max(nm[i])
	mineV[i] = min(eV[i])
	maxeV[i] = max(eV[i])
	#sigma=valsigma[i]
	x=np.linspace(mineV[i]/1.1,maxeV[i]*1.1,num=2000)
	spectrum=spec(eV[i],f[i],sigma,x)
	ax1.plot(1240/x,spectrum/max(spectrum),"--", label=f"{name[i]}",color=c[i], lw=3)
	ax1.vlines(nm[i], 0, f[i], color=c[i], lw=3, linestyles='solid')

ax1.legend(loc='upper left', frameon=False)
ax1.set_xlabel(r" $\lambda$ (nm)")
ax1.set_ylabel(r"f (oscillator strength)")
ax1.set_xlim(min(minnm)/1.1,max(maxnm)*1.1)
ax1.set_ylim(0,1.05)	

print("--- %s seconds ---" % (time.time() - start_time))

fig,ax2 = plt.subplots()
for i in range(len(filetoparser)):
	for line in open(filetoparser[i], "r"):
		if "Excited State  " in line: #let's find what we need
			#print(line.split()) #print all the required data on prompt for user
			eV[i].append(float(line.split()[4])) 
			nm[i].append(float(line.split()[6]))
			f[i].append(float(line.split("f=")[1][:5]))#("f=")[1]) #float
	minnm[i] = min(nm[i]) #one value, no need a list of list
	maxnm[i] = max(nm[i])
	mineV[i] = min(eV[i])
	maxeV[i] = max(eV[i])
	#sigma=valsigma[i]
	x=np.linspace(mineV[i]/1.1,maxeV[i]*1.1,num=2000)
	spectrum=spec(eV[i],f[i],sigma,x)
	ax2.plot(1240/x,spectrum/max(spectrum), label=f"{name[i]}",color=c[i], lw=3)

ax2.legend(loc='upper left', frameon=False)
ax2.set_xlabel(r" $\lambda$ (nm)")
ax2.set_ylabel(r"f (oscillator strength)")
ax2.set_xlim(min(minnm)/1.1,max(maxnm)*1.1)
ax2.set_ylim(0,1.05)	

print("--- %s seconds ---" % (time.time() - start_time))	

plt.show()
