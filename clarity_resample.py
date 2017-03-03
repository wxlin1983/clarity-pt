import clarity_libraw
import re

from os.path import expanduser
from os import walk
from os import path
from os.path import isfile

import matplotlib.pyplot as plt
import numpy as np

# Options
OutputDiagnosis = True
SaveEachData2CSV = True
ShowFigure = False

# Generate Output Fieldnames
filefolder = 'C:\\Users\\james\\Desktop\\clarity-pmrawhist\\'
califolder = 'C:\\Users\\james\\Dropbox (Clarity Movement)\\Hardware R&D\\P1 sensor\\Calibration\\'

#filerawfolder = califolder + '2017_03_03_MVP test airflow 2\\raw data - 1488567851\\'
filerawfolder = califolder + '2017_03_03_MVP test airflow 2\\raw data - 1488567854\\'


filefolder = '.\\'
filerawfolder = filefolder + 'raw data - 1488492697\\'

# for time reference
#filenames = ['mvp_1707-00010oldpd', 'mvp_1707-00010newpd']
filenames = ['mvp_1707-00009oldpd', 'mvp_1707-00009newpd']

# Threshold and Clipping Value of Old & New PD
th = [[3.1, 4.0, 3.6], [3.1, 3.6]]
cv = [3.6, 3.6]

# Create the Fieldnames
cla_fn = clarity_libraw.cla_makefieldnames()

# Read files in the given folder
fn_header = [[] for i in range(len(filenames))]
fn_hist = [[] for i in range(len(filenames))]

fn_header_re = []
fn_hist_re = []

for fn in filenames:
    fn_header_re.append(re.compile(
        "^" + fn + "_header_[0-9][0-9][0-9]\.(npy)$"))
    fn_hist_re.append(re.compile("^" + fn + "_hist_[0-9][0-9][0-9]\.(npy)$"))

if (path.isdir(filerawfolder)):
    for root, dirs, files in walk(filerawfolder):
        for b in sorted(files):
            for ii in range(len(filenames)):
                if fn_header_re[ii].match(b.lower()):
                    (fn_header[ii]).append(filerawfolder + b)
                if fn_hist_re[ii].match(b.lower()):
                    fn_hist[ii].append(filerawfolder + b)

allheader = clarity_libraw.readfnlist(fn_header)
alldata = clarity_libraw.readfnlist(fn_hist)

for k in range(len(th[0])):
    for ii in range(len(allheader)):
        tmp = []
        for jj in range(len(alldata[ii])):
            print('\rresampling: ', jj, end='\r')
            tmp.append(clarity_libraw.hist8bit(
                alldata[ii][jj], allheader[ii][jj], th[ii][k], cv[ii]).tolist())
        print('\n')
        clarity_libraw.write2file(filefolder + filenames[ii] + '_th' + str(th[ii][k]) +
                                  '.csv', cla_fn, np.array(tmp))
