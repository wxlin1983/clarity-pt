import time
import clarity_ptlib
import numpy

nAcquisition = 100

# PT Sensor connection setting
comnamelist = ['COM4']
ptlist = []
for comname in comnamelist:
    ptlist.append(clarity_ptlib.pt_connect_sensor('',comname,9600))

# purge old pt data in the buffer
for pt in ptlist:
    clarity_ptlib.pt_flush(pt)
        
fieldnames=clarity_ptlib.pt_makefieldnames()
for ii in range(nAcquisition):

    print('Taking data: ',ii + 1,' of ',nAcquisition)
    
    pt_datalist = []
    for pt in ptlist:
        pt_datalist.append(clarity_ptlib.pt_read_data(pt,''))
    jj = 0
    for pt_data in pt_datalist:
        towrite = numpy.append(numpy.asarray([time.time()]),pt_data)
        clarity_ptlib.write2file('ptdata_' + comnamelist[jj] + '.csv', fieldnames, towrite)
        jj = jj + 1

    print(pt_datalist[0])