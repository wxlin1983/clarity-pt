from PyDAQmx import *
import numpy
import time
import clarity_ptlib

# Declaration of variable passed by reference
nChan = 2
nSample = 50000
fSample = 50000.0

# Thredshold and Clipping Value
laser_th = 3
th = 0.18
cv = 3.6
hist_arr = numpy.zeros(256, dtype=numpy.float64)

# Generate output fieldnames
filename = 'output.csv'
fieldnames = clarity_ptlib.makefieldnames()

taskHandle = TaskHandle()
read = int32()
data = numpy.zeros((nChan * nSample,), dtype=numpy.float64)

try:
    # DAQmx Configure Code
    DAQmxCreateTask("",byref(taskHandle))
    DAQmxCreateAIVoltageChan(taskHandle,b'Dev1/ai0:1',"",DAQmx_Val_Cfg_Default,-0.5,2.5,DAQmx_Val_Volts,None)
    DAQmxCfgSampClkTiming(taskHandle,"",fSample,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,nSample)
    

    for ii in range(20):

        print('Take data: ',ii)

        # Reset histogram to zero
        hist_arr.fill(0)
                
        # DAQmx Start Code
        DAQmxStartTask(taskHandle)
        DAQmxReadAnalogF64(taskHandle,nSample,nSample / fSample + 1,DAQmx_Val_GroupByChannel,data,nSample * nChan,byref(read),None)
        DAQmxStopTask(taskHandle)

        [ai0, ai1] = numpy.split(data, nChan)

        t = numpy.arange(numpy.size(ai0))
        t = t[ai1 > laser_th]
        ai0_cut = ai0[ai1 > laser_th]

        # Calculate the total sample time
        tSample = sum(ai1 > laser_th) / fSample

        #print('current threshold voltage: ', th)
        #print('device dark voltage: ', numpy.mean(ai0[ai1 < laser_th]))

        if numpy.amax(ai0) > cv:
            print('some measured voltage, ',numpy.amax(ai0),', is higher than the set clipping value,',cv,'.')

        climbing = False
        num_peaks = 0
        width_count = 0

        for x in range(numpy.size(ai0_cut) - 1):
            if (climbing & (ai0_cut[x + 1] < ai0_cut[x])):
                climbing = False
                if (t[x + 1] - t[x] == 1):
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
        towrite = numpy.append(numpy.asarray([time.time(),0,0,0,0]),hist_arr)
        clarity_ptlib.write2file(filename, fieldnames, towrite)

        #numpy.savetxt('ai0'+str(ii)+'.csv', ai0, delimiter=',')
        #numpy.savetxt('ai1'+str(ii)+'.csv', ai1, delimiter=',')
        numpy.savetxt('data'+str(ii)+'.csv', data, delimiter=',')
        #numpy.savetxt('hist'+str(ii)+'.csv', hist_arr, delimiter=',')

except DAQError as err:
    print("DAQmx Error Code: ", err.error)

finally:
    if taskHandle:
        # DAQmx Stop Code
        DAQmxClearTask(taskHandle)
