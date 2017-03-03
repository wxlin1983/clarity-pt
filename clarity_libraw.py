import os
import csv
import time
import numpy as np
import pandas as pd

# hello world
def niv2i(v):
    y0 = 5.5166106903928235e-05
    dy = 0.00032257093698717654
    return (v - y0) / dy


def nii2v(myint):
    y0 = 5.5166106903928235e-05
    dy = 0.00032257093698717654
    return myint * dy + y0


def cla_makefieldnames():
    fieldnames = ['time', '#/cm3', "ug/m3", "thresh", "firmware"]
    for i in range(0, 256):
        fieldnames.append(str(i))
    return fieldnames


def str5(n):
    if not (type(n) is int):
        raise ValueError('str5: number input is not an integer.')
    if n < 0 or n > 99999:
        raise ValueError('str5: number input is too big or too small.')
    else:
        return ('00000' + str(n))[-5:]


def str3(n):
    if not (type(n) is int):
        raise ValueError('str3: number input is not an integer.')
    if n < 0 or n > 999:
        raise ValueError('str3: number input is too big or too small.')
    else:
        return ('000' + str(n))[-3:]


def write2file(filename, fieldnames, data):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a') as file_to_update:
        updater = csv.DictWriter(
            file_to_update, fieldnames=fieldnames, lineterminator='\n')
        if not file_exists:
            updater.writeheader()
        for jj in range(data.shape[0]):
            updater.writerow(dict(zip(fieldnames, data[jj])))


def readfnlist(fn_list):
    # fn_list should be a list of a list of filenames
    # returns a list of numpy arrays
    alllist = [[]] * len(fn_list)
    for ii in range(len(fn_list)):
        tmp = []
        for jj in range(len(fn_list[ii])):
            tmp += np.load(fn_list[ii][jj]).tolist()
        alllist[ii] = np.array(tmp)
    return alllist


def hist8bit(datai, header, th, cv, **kwargs):

    OutputDiagnosis = False
    timestamp = time.time()
    for key in kwargs.keys():
        if key == "timestamp":
            timestamp = kwargs.get(key)
        else:
            raise ValueError("Input argument not supported: " + key)

    hist_arr = np.zeros(256, dtype=np.float64)

    # Find peaks for channel
    for indx in range(hist_arr.shape[0]):

        indxleft = int(round(niv2i(indx * (cv - th) / 255 + th)))
        indxright = int(round(niv2i((indx + 1) * (cv - th) / 255 + th)))

        if indxleft < 0:
            indxleft = 0
        elif indxleft > 32767:
            indxleft = 32767

        if indxright < 0:
            indxright = 0
        elif indxright > 32767:
            indxright = 32767

        hist_arr[indx] = np.sum(datai[indxleft:indxright])

    # Build and save data
    return np.append(header, hist_arr)


def mkhist(data, **kwargs):

    # data should be ndarray of which entry between 0 and 2**15 - 1, sampled
    # for 1 second.
    OutputDiagnosis = False
    timestamp = time.time()

    for key in kwargs.keys():
        if key == "timestamp":
            timestamp = kwargs.get(key)
        elif key == "diagnosis":
            OutputDiagnosis = kwargs.get(key)
        else:
            raise ValueError("Input argument not supported: " + key)

    hist_arr = np.zeros(2**15, dtype=np.int16)

    # Output diagnosis message
    if OutputDiagnosis:
        if np.sum(data < 0) / len(data) > 0.005:
            print('mkhist: More than 0.5% of data are negative.')

    data = data[data >= 0]

    # Find peaks for channel
    climbing = False
    width_count = 0

    for x in range(np.size(data) - 1):

        if not climbing:
            if (data[x + 1] > data[x]):
                width_count = 0
                climbing = True
        else:
            if (data[x + 1] >= data[x]):
                width_count = width_count + 1
            else:
                climbing = False
                if(width_count > 1):
                    index = data[x]
                    hist_arr[index] = hist_arr[index] + 1

    # Build and save data
    return [timestamp, 0, 0, 0, 0], hist_arr.tolist()
