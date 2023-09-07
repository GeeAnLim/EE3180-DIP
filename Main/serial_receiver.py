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
import data_manager
import datetime


try:
    import queue
except ImportError:
    import Queue as queue

init_logging()
communicator = SerialCommunicator(port='COM3')
communicator.start()
print('The Base ID of your module is %s.' % enocean.utils.to_hex_string(communicator.base_id))

# endless loop receiving radio packets
while communicator.is_alive():
    try:
        # Loop to empty the queue...
        packet = communicator.receive.get(block=True, timeout=1)

        if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.BS4:

            # Get temperature from eep packet
            for k in packet.parse_eep(0x02, 0x05):
                temperature = packet.parsed[k].get('value')

            # Get sensor_id as a unique 6-character string
            packet_id = packet.data[6:]
            packet_id.append('')
            for i in range(len(packet_id) - 1):
                packet_id[len(packet_id) - 1] += str(hex(packet_id[i]).split('x')[-1])
            sensor_id = packet_id[len(packet_id) - 1]
            
            # Write data into data_manager.py
            if data_manager.write_data(sensor_id, temperature):
                print('Received data from ' + sensor_id + ', WE NEED TIME')

    except queue.Empty:
        continue
    except KeyboardInterrupt:
        break
    except Exception:
        traceback.print_exc(file=sys.stdout)
        break

if communicator.is_alive():
    communicator.stop()
