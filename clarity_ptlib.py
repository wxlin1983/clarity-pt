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

def pt_makefieldnames():
    fieldnames = ['time', 'mass_conc_1_0', 'mass_conc_2_5', 'mass_conc_10', 'num_conc_0_3', 'num_conc_0_5', 'num_conc_1_0', 'num_conc_2_5', 'num_conc_5_0', 'num_conc_10']
    return fieldnames

def write2file(filename, fieldnames, data):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a') as file_to_update:
        updater = csv.DictWriter(file_to_update, fieldnames=fieldnames, lineterminator='\n')
        if not file_exists:
            updater.writeheader()
        updater.writerow(dict(zip(fieldnames,data)))

def str5(n):
    if not (type(n) is int):
        raise ValueError('str5: input is not an integer.')
    if n < 0 or n > 99999:
        raise ValueError('str5: input is too big or too small.')
    else:
        return ('00000' + str(n))[-5:]

def pt_connect_sensor(dev_id, port, baudrate):
    sensor = serial.Serial(port=port,
        baudrate=baudrate,
        timeout=2.5)
    try:
        if not sensor.isOpen():
            sensor.open()
    except:
        serial.close()
        messagebox.showerror('Connection error', 'Could not connect to device: ' + str(dev_id[-4:]))
        return None
    return sensor

def pt_read_data(sensor_obj, dev_id):
    while True:
        byte1_int = int.from_bytes((sensor_obj.read(size=1)), byteorder='little')
        if (byte1_int == 66):
            reading = sensor_obj.read(size=31)
            if reading[0] == 0x4d:
                mass_conc_1_0 = int.from_bytes(reading[9:11], byteorder='big')
                mass_conc_2_5 = int.from_bytes(reading[11:13], byteorder='big')
                mass_conc_10 = int.from_bytes(reading[13:15], byteorder='big')
                num_conc_0_3 = int.from_bytes(reading[15:17], byteorder='big')
                num_conc_0_5 = int.from_bytes(reading[17:19], byteorder='big')
                num_conc_1_0 = int.from_bytes(reading[19:21], byteorder='big')
                num_conc_2_5 = int.from_bytes(reading[21:23], byteorder='big')
                num_conc_5_0 = int.from_bytes(reading[23:25], byteorder='big')
                num_conc_10 = int.from_bytes(reading[25:27], byteorder='big')
                to_return = [mass_conc_1_0, mass_conc_2_5, mass_conc_10, 
                            num_conc_0_3, num_conc_0_5, num_conc_1_0, 
                            num_conc_2_5, num_conc_5_0, num_conc_10]
                return to_return
            
def pt_flush(sensor_obj):
    print("Flushing buffer for",sensor_obj.port)
    millis0 = int(round(time.time() * 1000))
    bufferempty = False
    while (not bufferempty):
        pt_read_data(sensor_obj,'')
        millis1 = int(round(time.time() * 1000))
        if millis1 - millis0 > 500:
            bufferempty = True
            print("Buffer flushed")
        else:
            millis0 = millis1
    return

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
        if tSample < 0.4 * 0.1: # if the data is not enough, skip this data
            print('Data not sufficient, skip.')
            return False, numpy.asarray([])

        # Output diagnosis message
        if OutputDiagnosis:
            print('current threshold voltage: ', th)
            print('device dark voltage mean: ', numpy.mean(ai0[ai1 < laser_th]))
            print('device dark voltage std: ', numpy.std(ai0[ai1 < laser_th]))
            if numpy.amax(ai0) > cv:
                print('some measured voltage, ',numpy.amax(ai0),', is higher than the set clipping value,',cv,'.')

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
        return True, numpy.append(numpy.asarray([time.time(),0,0,0,0]),hist_arr)