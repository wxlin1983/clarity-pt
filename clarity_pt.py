from PyDAQmx import *
import numpy
import time
import clarity_ptlib
import pickle
import matplotlib.pyplot as plt

# Options
OutputDiagnosis = False
SaveEachData2CSV = True
SaveEachData2Pickle = False
ConnectPTSensor = False
ShowFigure = False

# Generate output fieldnames
filename = 'pt_aaaa.csv'
cla_fn = clarity_ptlib.cla_makefieldnames()
pt_fn = clarity_ptlib.pt_makefieldnames()

comnamelist = ['COM4']

# PT Sensor connection setting
ptlist = []
if ConnectPTSensor:
    for comname in comnamelist:
        ptlist.append(clarity_ptlib.pt_connect_sensor('',comname,9600))
        
# purge old pt data in the buffer
for pt in ptlist:
    clarity_ptlib.pt_flush(pt)

# Declaration of variable passed by reference
nChan = 2
nSample = 50000
fSample = 50000.0
nAcquisition = 3600*10

# Thredshold and Clipping Value
laser_th = 3
th = 0.1
cv = 3.6

taskHandle = TaskHandle()
read = int32()
data = numpy.zeros((nChan * nSample,), dtype=numpy.float64)

try:

    # DAQmx Configure Code
    DAQmxCreateTask("",byref(taskHandle))
    DAQmxCreateAIVoltageChan(taskHandle,b'Dev1/ai0:1',"",DAQmx_Val_Diff,-0.5,5,DAQmx_Val_Volts,None)
    #DAQmxCreateAIVoltageChan(taskHandle,b'Dev1/ai0',"",DAQmx_Val_Diff,-0.5,5,DAQmx_Val_Volts,None)
    DAQmxCfgSampClkTiming(taskHandle,"",fSample,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,nSample)

    for ii in range(nAcquisition):

        print('Taking data: ',ii + 1,' of ',nAcquisition)
        
        # DAQmx Start Code
        DAQmxStartTask(taskHandle)
        DAQmxReadAnalogF64(taskHandle,nSample,nSample / fSample + 1,DAQmx_Val_GroupByChannel,data,nSample * nChan,byref(read),None)
        DAQmxStopTask(taskHandle)

        isSuccessful, towrite = mk2write(data1, laser_th, th, cv, fSample)
        if isSuccessful:
            clarity_ptlib.write2file(filename, cla_fn, towrite)
        
        if ConnectPTSensor:
            jj = 0
            for pt in ptlist:
                towrite2 = numpy.append(numpy.asarray([time.time(),]),clarity_ptlib.pt_read_data(pt,''))
                #print(towrite2)
                clarity_ptlib.write2file('ptdata_' + comnamelist[jj] + '.csv', pt_fn, towrite2)
                jj = jj + 1
                
        if SaveEachData2CSV:
            numpy.savetxt('data' + clarity_ptlib.str5(ii) + '.csv', data, delimiter=',')
            
        if SaveEachData2Pickle:
            pickle.dump(data, open('data' + clarity_ptlib.str5(ii) + '.p', "wb"))

except DAQError as err:
    print("DAQmx Error Code: ", err.error)

finally:
    if taskHandle:
        # DAQmx Stop Code
        DAQmxClearTask(taskHandle)