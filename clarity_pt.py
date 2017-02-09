from PyDAQmx import *
from os.path import expanduser

import numpy
import clarity_ptlib
import matplotlib.pyplot as plt

# Options
OutputDiagnosis = False
SaveEachData2CSV = True
ShowFigure = False

# Generate output fieldnames
home = expanduser("~")
filefolder = home + \
    '\\Dropbox (Clarity Movement)\\Hardware R&D\\P1 sensor\\Calibration\\2017_02_08_plantower noise background measurement 2\\'
filename = 'pt_aaaa.csv'
cla_fn = clarity_ptlib.cla_makefieldnames()

# Declaration of variable passed by reference
nChan = 2
nSample = 500000
fSample = 50000
nAcquisition = 1

# Thredshold and Clipping Value
laser_th = 3
th = 0.1
cv = 3.6

taskHandle = TaskHandle()
read = int32()
data = numpy.zeros((nChan * nSample,), dtype=numpy.float64)

try:

    # DAQmx Configure Code
    DAQmxCreateTask("", byref(taskHandle))
    DAQmxCreateAIVoltageChan(taskHandle, b'Dev2/ai0:1',
                             "", DAQmx_Val_Diff, -0.5, 5, DAQmx_Val_Volts, None)
    DAQmxCfgSampClkTiming(taskHandle, "", fSample,
                          DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, nSample)

    for ii in range(nAcquisition):

        print('Taking data: ', ii + 1, ' of ', nAcquisition)

        # DAQmx Start Code
        DAQmxStartTask(taskHandle)
        DAQmxReadAnalogF64(taskHandle, nSample, nSample / fSample + 1,
                           DAQmx_Val_GroupByChannel, data, nSample * nChan, byref(read), None)
        DAQmxStopTask(taskHandle)

        isSuccessful, towrite = clarity_ptlib.mk2write(
            data, laser_th, th, cv, fSample)

        if isSuccessful:
            clarity_ptlib.write2file(filename, cla_fn, towrite)

        if SaveEachData2CSV:
            data2 = data.reshape((nChan, nSample)).T
            numpy.savetxt(
                filefolder + 'data_normal_0.5_gain_shielding_on_fan_off.csv', data2, delimiter=',')

except DAQError as err:
    print("DAQmx Error Code: ", err.error)

finally:
    if taskHandle:
        # DAQmx Stop Code
        DAQmxClearTask(taskHandle)
