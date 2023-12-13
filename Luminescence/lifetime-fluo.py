#!python3
# -*- coding: utf-8 -*-

'''
####  2021
Just insert the name of the file and the program will find the suitable "root" in the logfile. 
If no "root" found, the program will take the first. 

####  2020
This program allows one to simulate the fluorescence 
rate constant and lifetime after a TD-DFT computation

The whole equation of k_r is : 

k_r = (4/3)((\Delta E_{1-0})/c)^3(|µ_{1-0}|^2)

\Delta E_{1-0} is the energy difference between GS and ES
taken from electronic vertical emission (TD-DFT).


|µ_{1-0}|^2 is given in the Gaussian output
below the line :

<<<Ground to excited state transition electric dipole moments (Au):>>>
You need to look for the root of interest together with the column Dip. S.
It's already in a.u, therefore everything gonna be computed in a.u.


(see Rega et al, JPCA, 2012, 116, 7491 and Halet et al, ChemPhotoChem, 2020, 4, 173) 


# #####   variables to be entered by user
#
#vertical emission wavelength = vem
#dipS = |µ_{1-0}|^2
vem = 432 # 520 #nm
dipS = 0.4572 #41.1 # a.u.
#
# #### end of variables entered by user
'''

#################### JUST INSERT THE LOG FILE NAME ###############

with open("filename.log", "r") as f:
    line = f.readline()
    # print(line)
    while "----------------------------------------------------------------------" not in line:
        line = f.readline()
    line = f.readline()
    # print(line)
    while "----------------------------------------------------------------------" not in line:
        # print(line)
        if "root=".lower() in line.lower():
            ValRoot = int(line.lower().split("root=")[1][:1])  # take the root
            line = f.readline()
        else:
            ValRoot = 1  # if no root found ==> root = 1
        line = f.readline()
    line = f.readline()
    for line in f:
        # take the wavelength of the targeted root
        if f"Excited State   {ValRoot}" in line:
            vem = float((line.split()[6]))
        if f"transition electric dipole moments" in line:
            for i in range(ValRoot+1):  # ValRoot + 1 because need to pass 1 line
                # take the dipole strength of the targeted root
                dipS = (next(f, '').split()[4])

dipS = float(dipS)
print("|µ_{1-0}|^2 = ", dipS)
print("Electronic vertical emission wavelength = ", vem)
print("ROOT = ", ValRoot)

# Constant in a.u.
c = 137.04
t = 2.42*10**(-17)

# Unit conversion
DeltaEeV = 1240/vem
DeltaE_10_au = DeltaEeV/27.21

# k_r
k_r_au = (4/3)*((DeltaE_10_au/c)**3)*dipS
print("The rate constant, k_r, is =", format(
    k_r_au, "10.4E"), "a.u.")  # scientific format
k_r_sec = k_r_au/t
print("The rate constant, k_r, is =", format(
    k_r_sec, "10.4E"), "s-1")  # scientific format

# lifetime
tau = 1/k_r_sec
print("The fluorescence lifetime is =", format(
    tau, "10.4E"), "s")  # scientific format
