import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import clarity_libraw

from os.path import expanduser

plt.clf()

maxindex = 11000
plotrange = range(800, 1600)

# Generate output fieldnames
home = expanduser("~")
filefolder = home + \
    '\\Dropbox (Clarity Movement)\\Hardware R&D\\P1 sensor\\Calibration\\2017_03_06 EMI New vs Old Design\\raw data\\'

filenames = ['unnamed-01.npy']
# filenames = ['1707-00010.npy']

alldata = []
for fn in filenames:
    alldata.append(np.load(filefolder + fn).T)

y0, dy = clarity_libraw.gety0dy(alldata[0][0])


def getvhist(data):
    x = clarity_libraw.niv2ig(data, y0, dy).astype(np.int16)
    x = x[x > 0]
    v = clarity_libraw.nii2vg(np.array(range(maxindex)), y0, dy)
    hist_arr = np.zeros(maxindex, dtype=np.int32)
    for index in x:
        hist_arr[index] += 1
    return np.concatenate((hist_arr.reshape(1, -1), v.reshape(1, -1)), axis=0)

vhist0 = getvhist(alldata[0][0])
vhist1 = getvhist(alldata[0][1])

vhist0[0] = vhist0[0] / np.sum(vhist0[0])
vhist1[0] = vhist1[0] / np.sum(vhist1[0])

x = vhist0.T[plotrange].T
xmean = np.sum(x[0] * x[1]) / np.sum(x[0])
xstd = (np.sum(x[0] * ((x[1] - xmean)**2)) / np.sum(x[0]))**0.5
wemc, = plt.semilogy(vhist0[1][plotrange], vhist0[0][
                     plotrange], label='ORIGINAL PD, mean: ' + str(xmean)[0:5] + ', std: ' + str(xstd)[0:5])

x = vhist1.T[plotrange].T
xmean = np.sum(x[0] * x[1]) / np.sum(x[0])
xstd = (np.sum(x[0] * ((x[1] - xmean)**2)) / np.sum(x[0]))**0.5
woemc, = plt.semilogy(vhist1[1][plotrange], vhist1[0][
                      plotrange], label='NEW PD, mean: ' + str(xmean)[0:5] + ', std: ' + str(xstd)[0:5])

plt.xlabel('Raw Voltage (V)')
plt.ylabel('Normalized Counts')
plt.legend(handles=[woemc, wemc])
plt.title(filenames[0][:-4] + ' Background Noise')
plt.savefig(filefolder + filenames[0][:-4] + ' hist.png')
plt.clf()
