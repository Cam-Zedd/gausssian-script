#!python3
# -*- coding: utf-8 -*-

### import

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time

'''
Code to plot several spectra from Gaussian Vibronic calculations. 

###### What you need to modify ####

filetoparser = files to be read (list)
name = names to give in the plot (list)
sigma = value for gaussian shapes

##### Plot ####
Maximum for vibronic vertical line is 0.5 of the maximum to read easily the data
You can remove the normalization 
'''

######### Timings #########

start_time = time.time()

######## CAM's LAYOUT #########

SMALL_SIZE = 24
BIGGER_SIZE = 32
plt.rcParams.update({'font.size': SMALL_SIZE,
					 'axes.titlesize':BIGGER_SIZE, 'axes.edgecolor':'black','axes.labelsize':BIGGER_SIZE, 'axes.linewidth':2,
					 'xtick.labelsize':SMALL_SIZE, 'xtick.major.size':10, 'xtick.major.width':2, 'lines.markersize':10,'patch.linewidth':3.0,
					 'ytick.labelsize':SMALL_SIZE, 'ytick.major.size':10, 'ytick.major.width':2, 'ytick.minor.size':6, 'ytick.minor.width':1})
plt.rcParams['axes.xmargin'] = 0 

######### FILES TO BE READ #########

#filetoparser = ["6-AH-reverse.log","7-AH-reverse.log","8-AH-reverse.log","9-AH-reverse.log","10-AH-reverse.log"] # all the files needed
filetoparser = ["AH_T0_M062x.log"]

######### COMPOUND NAMES #########

#name = ["6", "7", "8", "9", "10"]
name = ["compound_Z"]

######### START THE LISTS #########

energycm, intensity, intens, maxintensity, mincm, maxcm, = ([[]for _ in range(len(filetoparser))] for _ in range(6))

######### Colors #########

c=["dodgerblue","coral","seagreen","darkorchid","red","dimgrey","orangered","peru","limegreen","slateblue","fushia"]

######### Gaussian function #########

'''
Adapted from Michael Dommett code
def spec(E,f,sigma,x):
    spectrum=[]
    for E1 in x:
        tot=0
        for E2,os in zip(E,f):
            tot+=os*np.exp(-((((E2-E1)/sigma)**2)))
        spectrum.append(tot)
    return spectrum #prepare spectrum for the values to be plotted
sigma=0.1	
'''

def spec(E,f,sigma,x):
    _E = np.array(E) #energy
    _f = np.array(f) #oscillateur strengths (here intensity)
    spectrum=np.zeros((len(x),)) #tuple (n,), matrix with dimension 1 of n length
    for i, E1 in enumerate(x):
        tot =  _f.dot(np.exp(-((((_E-E1)/sigma)**2))))
        spectrum[i] = tot
    return spectrum #prepare spectrum for the values to be plotted
sigma=165	
#valsigma=[0.1, 0.3, 0.5, 0.7, 0.1]  #useful to tune HWHM for different compounds.

######### THE CODE #########
 
fig,ax1 = plt.subplots()
for i in range(len(filetoparser)):
	with open(filetoparser[i], "r") as f:
		line=f.readline() #read the line
		while 'Final Spectrum' not in line: #Go until Final Spectrum without stocking
			line=f.readline() #let's continue
			#print(line)    
		while '---------' not in line: #Go until the first '---------' pattern
			line=f.readline() #let's continue
			#print(line)   
		line=f.readline() #let's continue - last pattern
		while '---------' not in line: #Go until the second '---------' pattern
			#print(filetoparser[i],line)
			intens=float(line.split()[1].replace("D","E")) #replace D by E for power.
			if intens > 0.1:
				energycm[i].append(float(line.split()[0]))
				intensity[i].append(intens)
			line=f.readline() #Let's continue through	
	mincm[i] = min(energycm[i])
	maxcm[i] = max(energycm[i])
	maxintensity[i] = max(intensity[i])
	x=np.linspace(5000,25000,num=5000)
	print(f"printing the convoluted spectrum of {name[i]}")
	spectrum=spec(energycm[i],intensity[i],sigma,x)
	ax1.plot(x,spectrum/max(spectrum),"-", label=f"{name[i]}",color=c[i], lw=3)
	print(f"spectrum of {name[i]} achieved in :" "%s seconds" % (time.time() - start_time))
	print(f"printing the vlines spectra of {name[i]}")
	ax1.vlines(energycm[i], 0, intensity[i]/(2*np.array(maxintensity[i])), color=c[i], lw=2, linestyles='solid')# label='', color=c[0], lw=2, linestyles='solid'

######### To be tuned as you wish #########

ax1.legend(loc='upper left', frameon=False)
ax1.set_xlim(min(mincm)/1.1,max(maxcm)*1.1)
ax1.set_ylim(0,1.05)	
ax1.set_xlabel(r"Energy (cm$^{-1}$)")
ax1.set_ylabel(r"Normalized Intensity")

print("--- %s seconds ---" % (time.time() - start_time))

plt.show()

