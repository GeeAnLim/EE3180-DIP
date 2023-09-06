#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from enocean.consolelogger import init_logging
import enocean.utils
from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.packet import RadioPacket
from enocean.protocol.constants import PACKET, RORG
import sys
import traceback

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
        if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.VLD:
            packet.select_eep(0x14, 0x41)
            print('selected')
            packet.parse_eep()
            print('parsed')
            for k in packet.parsed:
                print('%s: %s' % (k, packet.parsed[k]))
            print('printed')
        if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.BS4:
            # parse packet with given FUNC and TYPE
            for k in packet.parse_eep(0x02, 0x05):
                print('%s: %s' % (k, packet.parsed[k]))
        if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.BS1:
            # alternatively you can select FUNC and TYPE explicitely
            packet.select_eep(0x00, 0x01)
            # parse it
            packet.parse_eep()
            for k in packet.parsed:
                print('%s: %s' % (k, packet.parsed[k]))
        if packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.RPS:
            for k in packet.parse_eep(0x02, 0x02):
                print('%s: %s' % (k, packet.parsed[k]))
    except queue.Empty:
        continue
    except KeyboardInterrupt:
        break
    except Exception:
        traceback.print_exc(file=sys.stdout)
        break

if communicator.is_alive():
    communicator.stop()
