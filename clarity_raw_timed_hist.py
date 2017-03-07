import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import clarity_libraw

from os.path import expanduser

maxindex = 11000

# Generate output fieldnames
home = expanduser("~")
filefolder = home + \
    '\\Dropbox (Clarity Movement)\\Hardware R&D\\P1 sensor\\Calibration\\2017_03_06 EMI New vs Old Design\\raw data\\'

filenames = ['00000-with emc.npy', '00000-without emc.npy']

alldata = []
for fn in filenames:
    alldata.append(np.load(filefolder + fn).T)

y0, dy = clarity_libraw.gety0dy(alldata[0][0])


def getvhist(data, indx):
    x = clarity_libraw.niv2ig(data[indx], y0, dy).astype(np.int16)
    x = x[x > 0]
    v = clarity_libraw.nii2vg(np.array(range(maxindex)), y0, dy)
    hist_arr = np.zeros(maxindex, dtype=np.int32)
    for index in x:
        hist_arr[index] += 1
    return np.concatenate((hist_arr.reshape(1, -1), v.reshape(1, -1)), axis=0)

vhist0 = getvhist(alldata[0], 1)
vhist1 = getvhist(alldata[1], 1)

vhist0[0] = vhist0[0] / np.sum(vhist0[0])
vhist1[0] = vhist1[0] / np.sum(vhist1[0])

plotrange = range(800, 3000)
plt.semilogy(vhist0[1][plotrange], vhist0[0][plotrange])
plt.semilogy(vhist1[1][plotrange], vhist1[0][plotrange])
plt.show()
