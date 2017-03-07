import numpy as np
import pandas as pd
import clarity_libraw

from os.path import expanduser

# Generate output fieldnames
home = expanduser("~")
filefolder = home + \
    '\\Dropbox (Clarity Movement)\\Hardware R&D\\P1 sensor\\Calibration\\2017_03_06 EMI New vs Old Design\\raw data\\'

filenames = ['00000-with emc.npy', '00000-without emc.npy', '00000.npy']

alldata = []
for fn in filenames:
    alldata.append(np.load(filefolder + fn).T)

y0, dy = clarity_libraw.gety0dy(alldata[0][0])

x = clarity_libraw.niv2ig(alldata[0][0], y0, dy).astype(np.int16)