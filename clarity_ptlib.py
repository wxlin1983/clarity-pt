import os
import csv

#def set_filename(self, folderpath):
#        timenow = imp
#        timenow = timenow.split(":")
#        timenow = str(timenow[0])+"-"+str(timenow[1])+"-"+str(timenow[2])
#        self.filename = folderpath + "/" + "cla_" + self.dev_id[-4:] + ".csv"
#        try:
#            with open(self.filename, 'a') as file_to_write:
#                writer = csv.DictWriter(file_to_write, fieldnames=self.fieldnames, lineterminator='\n')
#                writer.writeheader()
#            return 1
#        except:
#            messagebox.showerror('Failed', 'Failed to write to file at: '+ str(self.filename))
#            return 0

def makefieldnames():
    fieldnames = ['time', '#/cm3', "ug/m3", "thresh", "firmware"]
    for i in range(0, 256):
        fieldnames.append(str(i))
    return fieldnames

def write2file(filename, fieldnames, data):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a') as file_to_update:
        updater = csv.DictWriter(file_to_update, fieldnames=fieldnames, lineterminator='\n')
        if not file_exists:
            updater.writeheader()
        updater.writerow(dict(zip(fieldnames,data)))
        
#def pt_connect_sensor(dev_id, port, baudrate):
#    sensor = serial.Serial(
#        port=port,
#        baudrate=baudrate,
#        timeout=2.5
#        )
#    try:
#        if not sensor.isOpen():
#            sensor.open()
#    except:
#        serial.close()
#        messagebox.showerror('Connection error', 'Could not connect to device: ' + str(dev_id[-4:]))
#        return None
#    return sensor

#def pt_read_data(sensor_obj, dev_id):
#    while True:
#        byte1_int = int.from_bytes((sensor_obj.read(size=1)), byteorder='little')
#        if (byte1_int == 66):
#            reading = sensor_obj.read(size=31)
#            if reading[0] == 0x4d:
#                mass_conc_1_0 = int.from_bytes(reading[9:11], byteorder='big')
#                mass_conc_2_5 = int.from_bytes(reading[11:13], byteorder='big')
#                mass_conc_10 = int.from_bytes(reading[13:15], byteorder='big')
#                num_conc_0_3 = int.from_bytes(reading[15:17], byteorder='big')
#                num_conc_0_5 = int.from_bytes(reading[17:19], byteorder='big')
#                num_conc_1_0 = int.from_bytes(reading[19:21], byteorder='big')
#                num_conc_2_5 = int.from_bytes(reading[21:23], byteorder='big')
#                num_conc_5_0 = int.from_bytes(reading[23:25], byteorder='big')
#                num_conc_10 = int.from_bytes(reading[25:27], byteorder='big')
#                to_return = [mass_conc_1_0, mass_conc_2_5, mass_conc_10, 
#                            num_conc_0_3, num_conc_0_5, num_conc_1_0, 
#                            num_conc_2_5, num_conc_5_0, num_conc_10]
#                return to_return

#self.uncalib_fieldnames = ['time', '#/cm3', "ug/m3", "thresh", "firmware"]
#for i in range(0, self.bin_num):
#            self.uncalib_fieldnames.append(str(i))
