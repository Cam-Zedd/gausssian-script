import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sint

# CAM's TEMPLATE
SMALL_SIZE = 32
BIGGER_SIZE = 34
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

#Func to store data to be plotted
def func(myfile):
    data = np.loadtxt(myfile).transpose()
    _, n2 = data.shape
    n = int(n2**0.5)
    assert n**2 == n2
    x, y, c = data[3, :], data[4, :], data[5, :]
    x = x[0::n]
    y = y[0:n]
    c = c.reshape((n, n))
    interp = sint.RectBivariateSpline(x, y, c)
    lim_x = np.min(x), np.max(x)
    lim_y = np.min(y), np.max(y)
    xx = np.linspace(*lim_x, 1500)
    yy = np.linspace(*lim_y, 1500)
    X, Y = np.meshgrid(xx, yy)
    C = interp.ev(X, Y)
    return X, Y, C

############# PART TO BE FILLED BY USERS ################
files = ["densT0Sty-Lan-PBE0-wfn-data.txt",
         "densT0StyDimer-Lan-PBE0-wfn-data.txt",
         "densT0-Lan-PBE0-Ethyl-wfn-data.txt",
         "densT1-Lan-PBE0-Ethyl-wfn-data.txt"]
names = ['Sty-M-LC',
         'Sty-D-LC',
         'Eth-M-LC',
         'Eth-M-CC']
#############                             ################

## The plot
im = [i for i in range(len(files))]
fig, axes = plt.subplots(nrows=1, ncols=len(files))
for i, file in enumerate(files):
    # fig.tight_layout()
    print("working on file:", file)
    val1, val2, val3 = func(file)
    im[i] = axes[i].pcolormesh(
        val1,
        val2,
        val3,
        vmin=0.,#min_value on colorbar
        vmax=1.,#max_value on colorbar
        cmap="gnuplot2")
    axes[i].axis('off')
    axes[i].set_title(f'{names[i]}') 
fig.colorbar(im[-1], ax=axes[-1])
v = np.linspace(0, 1, 4, endpoint=True)
plt.show()


"""
by hand
#GSX, GSY, GSC = func("plane-GS.txt")
#StyMMX, StyMMY, StyMMC = func("densT0Sty-Lan-PBE0-wfn-data.txt") #styrene monomere
#StyDMX, StyDMY, StyDMC = func("densT0StyDimer-Lan-PBE0-wfn-data.txt") #styrene dimere
#ESLCX, ESLCY, ESLCC = func("densT0-Lan-PBE0-Ethyl-wfn-data.txt") #long
#ESCCX, ESCCY, ESCCC = func("densT1-Lan-PBE0-Ethyl-wfn-data.txt") #short

fig, (ax1, ax2, ax3, ax4) = plt.subplots(1,4)
#fig, (ax2, ax3) = plt.subplots(1,2)

im1 = ax1.pcolormesh(StyMMX, StyMMY, StyMMC, cmap="gnuplot2")
im2 = ax2.pcolormesh(StyDMX, StyDMY, StyDMC, cmap="gnuplot2")
im3 = ax3.pcolormesh(ESLCX, ESLCY, ESLCC, cmap="gnuplot2")
im4 = ax4.pcolormesh(ESCCX, ESCCY, ESCCC, cmap="gnuplot2")

#rect1 = patches.Rectangle((-2.77,2.485), 0.37,0.75, lw = 2, edgecolor = "r", facecolor = 'none') #ES
#ax3.add_patch(rect1)

v = np.linspace(0, 1, 6, endpoint=True)
#plt.colorbar(ticks=v)


ax1.axis('off')
ax2.axis('off')
ax3.axis('off')
ax4.axis('off')

ax1.set_title('Sty-M-LC')
ax2.set_title('Sty-D-LC')
ax3.set_title('Eth-M-LC')
ax4.set_title('Eth-M-CC')

fig.tight_layout()
fig.colorbar(im1, ax=ax1)
fig.colorbar(im2, ax=ax2)
fig.colorbar(im3, ax=ax3)
fig.colorbar(im4, ax=ax4)
plt.show()
"""
