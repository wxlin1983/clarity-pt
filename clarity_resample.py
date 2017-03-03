import numpy as np
import clarity_ptlib
from pandas import DataFrame
from pandas import read_csv
import matplotlib.pyplot as plt
from os.path import expanduser
from PyDAQmx import *

from os import walk
from os import path
from os.path import isfile

# Options
OutputDiagnosis = True
SaveEachData2CSV = True
ShowFigure = False

# Generate output fieldnames
filefolder = '.\\'
filerawfolder = filefolder + 'raw data - 1488492697\\'

# for time reference
filenames = ['mvp_1707-00009oldpd', 'mvp_1707-00009newpd']

th = [0.31, 0.36]
cv = [3.6, 3.6]

cla_fn = clarity_ptlib.cla_makefieldnames()

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

allheader = clarity_ptlib.readfnlist(fn_header)
alldata = clarity_ptlib.readfnlist(fn_hist)

for ii in range(len(allheader)):
    tmp = []
    for jj in range(len(alldata[ii])):
        print('\r', filenames[ii], 'resampling:', jj, end='\r')
        tmp.append(clarity_ptlib.hist8bit(
            alldata[ii][jj], allheader[ii][jj], th[ii], cv[ii]).tolist())
    clarity_ptlib.write2file2(filefolder + filenames[ii] + '.csv', cla_fn, np.array(tmp))
