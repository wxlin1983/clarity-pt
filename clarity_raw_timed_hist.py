import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import clarity_libraw

from os.path import expanduser

plotrange = range(800, 1600)
maxindex = 11000
plt.clf()

# Generate output fieldnames
home = expanduser("~")
filefolder = home + \
    '\\Dropbox (Clarity Movement)\\Hardware R&D\\P1 sensor\\Calibration\\2017_03_06 EMI New vs Old Design\\raw data\\'

filenames = ['w emi.npy', 'wo emi.npy']

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

vhist0 = getvhist(alldata[0][1])
vhist1 = getvhist(alldata[1][1])

vhist0[0] = vhist0[0] / np.sum(vhist0[0])
vhist1[0] = vhist1[0] / np.sum(vhist1[0])

woemc, = plt.semilogy(vhist1[1][plotrange], vhist1[0][
                      plotrange], label='WITHOUT EMI')
wemc, = plt.semilogy(vhist0[1][plotrange], vhist0[
                     0][plotrange], label='WITH EMI')
plt.xlabel('Raw Voltage (V)')
plt.ylabel('Normalized Counts')
plt.legend(handles=[woemc, wemc])
plt.title('1707-00010 New PD')
plt.savefig(filefolder + 'hist-new.png')
plt.clf()

vhist0 = getvhist(alldata[0][0])
vhist1 = getvhist(alldata[1][0])

vhist0[0] = vhist0[0] / np.sum(vhist0[0])
vhist1[0] = vhist1[0] / np.sum(vhist1[0])

woemc, = plt.semilogy(vhist1[1][plotrange], vhist1[0][
                      plotrange], label='WITHOUT EMI')
wemc, = plt.semilogy(vhist0[1][plotrange], vhist0[
                     0][plotrange], label='WITH EMI')
plt.xlabel('Raw Voltage (V)')
plt.ylabel('Normalized Counts')
plt.legend(handles=[woemc, wemc])
plt.title('1707-00010 Old PD')
plt.savefig(filefolder + 'hist-old.png')
plt.clf()