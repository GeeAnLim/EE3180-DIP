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


        # USEFUL PART START

        if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.BS4:

            # GET TEMPERATURE
            # parse packet with given FUNC and TYPE
            for k in packet.parse_eep(0x02, 0x05):
                temperature = packet.parsed[k].get('value')

            # GET SENSOR_ID
            packet_sender = packet.data[6:]
            for i in range(len(packet_sender)):
                packet_sender[i] = hex(packet_sender[i]).split('x')[-1]
            sensor_id = '%s%s%s%s' % 

        # USEFUL PART END

    except queue.Empty:
        continue
    except KeyboardInterrupt:
        break
    except Exception:
        traceback.print_exc(file=sys.stdout)
        break

if communicator.is_alive():
    communicator.stop()