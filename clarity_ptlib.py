import os
import csv
import serial
import time
import numpy


def cla_makefieldnames():
    fieldnames = ['time', '#/cm3', "ug/m3", "thresh", "firmware"]
    for i in range(0, 256):
        fieldnames.append(str(i))
    return fieldnames


def write2file(filename, fieldnames, data):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a') as file_to_update:
        updater = csv.DictWriter(
            file_to_update, fieldnames=fieldnames, lineterminator='\n')
        if not file_exists:
            updater.writeheader()
        updater.writerow(dict(zip(fieldnames, data)))


def str5(n):
    if not (type(n) is int):
        raise ValueError('str5: input is not an integer.')
    if n < 0 or n > 99999:
        raise ValueError('str5: input is too big or too small.')
    else:
        return ('00000' + str(n))[-5:]


def mk2write(data, laser_th, th, cv, fSample):

    hist_arr = numpy.zeros(256, dtype=numpy.float64)

    nChan = 2
    OutputDiagnosis = True

    if nChan == 2:

        [ai0, ai1] = numpy.split(data, nChan)

        t1 = numpy.arange(numpy.size(ai0))
        t1 = t1[ai1 > laser_th]
        ai0_cut = ai0[ai1 > laser_th]

        # Calculate the total sample time
        tSample = sum(ai1 > laser_th) / fSample
        if tSample < 0.4 * 0.1:  # if the data is not enough, skip this data
            print('Data not sufficient, skip.')
            return False, numpy.asarray([])

        # Output diagnosis message
        if OutputDiagnosis:
            print('current threshold voltage: ', th)
            print('device dark voltage mean: ',
                  numpy.mean(ai0[ai1 < laser_th]))
            print('device dark voltage std: ', numpy.std(ai0[ai1 < laser_th]))
            if numpy.amax(ai0) > cv:
                print('some measured voltage, ', numpy.amax(ai0),
                      ', is higher than the set clipping value,', cv, '.')

        # Find peaks for channel
        climbing = False
        num_peaks = 0
        width_count = 0

        for x in range(numpy.size(ai0_cut) - 1):
            if (climbing & (ai0_cut[x + 1] < ai0_cut[x])):
                climbing = False
                if (t1[x + 1] - t1[x] == 1):
                    if(width_count > 1):
                        num_peaks = num_peaks + 1
                        index = int(round(255 * (ai0_cut[x] - th) / (cv - th)))
                        hist_arr[index] = hist_arr[index] + 1
                else:
                    width_count = 0
            elif(ai0_cut[x + 1] > ai0_cut[x]):
                climbing = True

            if(ai0_cut[x] < th):
                width_count = 0
            else:
                width_count = width_count + 1

        # Normalize the sample time to 1s
        hist_arr = numpy.around(hist_arr / tSample)

        # Build and save data
        return True, numpy.append(numpy.asarray([time.time(), 0, 0, 0, 0]), hist_arr)
