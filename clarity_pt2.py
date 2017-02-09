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
filename1 = 'pt_0010.csv'
filename2 = 'pt_0011.csv'
cla_fn = clarity_ptlib.cla_makefieldnames()

# Declaration of variable passed by reference
nChan = 2
nSample = 50000
fSample = 50000.0
nAcquisition = 3600 * 10

# Thredshold and Clipping Value
laser_th = 3
th = 0.1
cv = 3.6

# Setting NiDAQmx Handle
taskHandle1 = TaskHandle()
taskHandle2 = TaskHandle()

# Initializing Data Buffer
read = int32()
data1 = numpy.zeros((nChan * nSample,), dtype=numpy.float64)
data2 = numpy.zeros((nChan * nSample,), dtype=numpy.float64)

try:

    # DAQmx Configure Code
    DAQmxCreateTask("", byref(taskHandle1))
    DAQmxCreateAIVoltageChan(taskHandle1, b'Dev1/ai0:1',
                             "", DAQmx_Val_Diff, -0.5, 5, DAQmx_Val_Volts, None)
    DAQmxCfgSampClkTiming(taskHandle1, "", fSample,
                          DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, nSample)

    DAQmxCreateTask("", byref(taskHandle2))
    DAQmxCreateAIVoltageChan(taskHandle2, b'Dev2/ai0:1',
                             "", DAQmx_Val_Diff, -0.5, 5, DAQmx_Val_Volts, None)
    DAQmxCfgSampClkTiming(taskHandle2, "", fSample,
                          DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, nSample)

    for ii in range(nAcquisition):

        print('Taking data: ', ii + 1, ' of ', nAcquisition)

        # DAQmx Start Code
        DAQmxStartTask(taskHandle1)
        DAQmxReadAnalogF64(taskHandle1, nSample, nSample / fSample + 1,
                           DAQmx_Val_GroupByChannel, data1, nSample * nChan, byref(read), None)
        DAQmxStopTask(taskHandle1)

        DAQmxStartTask(taskHandle2)
        DAQmxReadAnalogF64(taskHandle2, nSample, nSample / fSample + 1,
                           DAQmx_Val_GroupByChannel, data2, nSample * nChan, byref(read), None)
        DAQmxStopTask(taskHandle2)

        isSuccessful, towrite = mk2write(data1, laser_th, th, cv, fSample)
        if isSuccessful:
            clarity_ptlib.write2file(filefolder + filename1, cla_fn, towrite)
        isSuccessful, towrite = mk2write(data2, laser_th, th, cv, fSample)
        if isSuccessful:
            clarity_ptlib.write2file(filefolder + filename2, cla_fn, towrite)

        if SaveEachData2CSV:
            data1g = data1.reshape((nChan, nSample)).T
            data2g = data2.reshape((nChan, nSample)).T
            numpy.savetxt(filefolder + 'data1-' +
                          clarity_ptlib.str5(ii) + '.csv', data1g, delimiter=',')
            numpy.savetxt(filefolder + 'data2-' +
                          clarity_ptlib.str5(ii) + '.csv', data2g, delimiter=',')

except DAQError as err:
    print("DAQmx Error Code: ", err.error)

finally:

    # DAQmx Stop Code
    if taskHandle1:
        DAQmxClearTask(taskHandle1)

    if taskHandle2:
        DAQmxClearTask(taskHandle2)
