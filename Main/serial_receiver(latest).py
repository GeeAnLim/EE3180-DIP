# Will run by Raspberry Pi 4
# Receive sensor radio data at the serial port
# Decode sensor data and write into data_manager.py
from enocean.consolelogger import init_logging
import enocean.utils
from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.packet import RadioPacket
from enocean.protocol.constants import PACKET, RORG
import sys
import traceback
import os
from enocean.protocol.eep import EEP
from enocean.protocol import crc8
import xml.dom.minidom as MD
from datetime import datetime
import numpy
import pandas
import csv


try:
    import queue
except ImportError:
    import Queue as queue


with open('data_manager.csv', 'w') as csv_file:
    csvwriter = csv.writer(csv_file)
                
    Column_list = ["Date", "Time", "Address" ,"Sensor ID", "Temperature", "Acceleration X", "Acceleration Y", "Acceleration Z", "Magnet Contact"]



init_logging()
communicator = SerialCommunicator(port='COM3')
communicator.start()
print('The Base ID of your module is %s.' % enocean.utils.to_hex_string(communicator.base_id))

# endless loop receiving radio packets
while communicator.is_alive():
    try:
        # Loop to empty the queue...
        
        
        packet = communicator.receive.get(block=True, timeout=0.5)

        if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.VLD:
            
            # Obtain the sensor_id, its always located at the back of packet data but varies with packet type, for VLD, its the last 6th to last 2nd, thus [-5:-1]
            packet_id = packet.data[-5:-1]         
            packet_id.append('')
            for i in range(len(packet_id) - 1):
                packet_id[len(packet_id) - 1] += str(hex(packet_id[i]).split('x')[-1])
            
            sensor_id = packet_id[len(packet_id) - 1]
            print(sensor_id)                                                         #Display for testing(Success)

            if sensor_id == '42261f3':
                address = "Blk A01 #02-1234, S760A01"

            elif sensor_id == '42262a':
                address = "Blk B01 #02-1234, S760B01"

            elif sensor_id == '4226076':
                address = "Blk C01 #02-1234, S760C01"
            
            elif sensor_id == '4226087':
                address = "Blk D01 #02-1234, S760D01"

            elif sensor_id == '4226222':
                address = "Blk E01 #02-1234, S760E01"

            elif sensor_id == '42261EA':
                address = "Blk F01 #02-1234, S760F01"

            current_datetime = datetime.now()
            current_time = current_datetime.strftime("%H:%M:%S")
            current_day = current_datetime.strftime("%d/%m/%Y")

            # Get temperature from eep packet
            packet.select_eep(0x14, 0x41)
            packet.parse_eep()
            for k in packet.parsed:

                if k == 'TMP':
                    TMPdata = packet.parsed[k]
                    TMP = TMPdata['value']
                    print(TMP)
                
                elif k == 'ACX':
                    ACXdata = packet.parsed[k]
                    ACX = ACXdata['value']
                    #print(ACX)
                
                elif k == 'ACY':
                    ACYdata = packet.parsed[k]
                    ACY = ACYdata['value']
                    #print(ACY)
                
                elif k == 'ACZ':
                    ACZdata = packet.parsed[k]
                    ACZ = ACZdata['value']
                    #print(ACZ)

                elif k == 'CO':
                    COdata = packet.parsed[k]
                    CO = COdata['value']
                    #print(CO)
                

            print(current_time)
            print(current_day)

            

            
            csvwriter.writerow([current_day, current_time, address, sensor_id, TMP, ACX, ACY, ACZ, CO])




                #current_day.to_csv(csv_file, mode = 'a', index = False, header = False, columns = 1)
                #current_time.to_csv(csv_file, mode = 'a', index = False, header = False, columns = 2)
                #address.to_csv(csv_file, mode = 'a', index = False, header = False, columns = 3)
                #sensor_id.to_csv(csv_file, mode = 'a', index = False, header = False, columns = 4)
                #TMP.to_csv(csv_file, mode = 'a', index = False, header = False, columns = 5)
                #ACX.to_csv(csv_file, mode = 'a', index = False, header = False, columns = 6)
                #ACY.to_csv(csv_file, mode = 'a', index = False, header = False, columns = 7)
                #ACZ.to_csv(csv_file, mode = 'a', index = False, header = False, columns = 8)
                #CO.to_csv(csv_file, mode = 'a', index = False, header = False, columns = 9)
            
            
            


            

    except queue.Empty:
        continue
    except KeyboardInterrupt:
        break
    except Exception:
        traceback.print_exc(file=sys.stdout)
        break

if communicator.is_alive():
    communicator.stop()
