import struct
import binascii

from copy import deepcopy
from collections import namedtuple

from serial import Serial
from serial.tools import list_ports

from time import time
from time import sleep
from sched import scheduler

class CoreDevice(object):
    """BoxIO CoreDevice interface"""
    Request =     namedtuple('Request',     ['length', 'typeIntf', 'payload'])
    Response =    namedtuple('Response',    ['length', 'typeIntf', 'response_id', 'payload'])
    GpioEvent =   namedtuple('GpioEvent',   ['length', 'typeIntf', 'timestamp', 'port'])
    CanRequest =  namedtuple('CanRequest',  ['length', 'typeIntf', 'can_id', 'can_dlc', 'can_data'])
    CanEvent =    namedtuple('CanEvent',    ['length', 'typeIntf', 'timestamp', 'can_id', 'can_dlc', 'can_data'])
    GpioEventFormat  = '<BBIH'
    CanRequestFormat = '<BBIB{dlc}s'
    CanEventFormat   = '<BBIIB{dlc}s'

    def __init__(self, serialPort):
        self.serial_port = serialPort
    
    def open_connection(self):
        if self.serial_port is None:
            return False
        if (not self.serial_port.is_open):
            self.serial_port.open()
        return self.serial_port.is_open

    def close_connection(self):
        if self.serial_port is None:
            return False
        if self.serial_port.is_open:
            self.serial_port.close()
        return not self.serial_port.is_open

    def get_firmware_version(self):
        firmware_rq = CoreDevice.Request( 3, 0x62, 0x04 )
        rq_data = struct.pack('<BBB', *firmware_rq)
        self.serial_port.write( rq_data )
        self.serial_port.flush()

        receive_buffer = bytearray(64)
        size = self.serial_port.readinto(receive_buffer)
        response_data = receive_buffer[:size]
        Response = namedtuple('Response', ['length', 'typeIntf', 'response_id', 'payload'])

        response_fmt = '<BBB{}s'.format(response_data[0]-3)
        response = CoreDevice.Response( *struct.unpack(response_fmt, response_data) )

        return response

    def get_hardware_version(self):
        hardware_rq = CoreDevice.Request( 3, 0x62, 0x05 )
        rq_data = struct.pack('<BBB', *hardware_rq)
        self.serial_port.write( rq_data )
        self.serial_port.flush()

        receive_buffer = bytearray(64)
        size = self.serial_port.readinto(receive_buffer)
        response_data = receive_buffer[:size]

        response_fmt = '<BBB{}s'.format(response_data[0]-3)
        response = CoreDevice.Response( *struct.unpack(response_fmt, response_data) )

        return response

    def make_can_message(self, can_id, can_data):
        mTypeIntf = (0x2 << 4) | 0x0
        mLen = 2 + 4 + len(can_data)
        box_can_format = '<BBLB{}s'.format(len(can_data))
        data = struct.pack(box_can_format, mLen, mTypeIntf, can_id, len(can_data), can_data)
        return data

    def make_can_request(self, can_id, can_data):
        msgLen = 2 + 4 + len(can_data)
        msgTypeIntf = (0x2 << 4) | 0x0          # high nible: interface, low nible: type
        return CanRequest(msgLen, msgTypeIntf, can_id, len(can_data), can_data)

    def make_gpio_event(msg_data):
        unpkd = struct.unpack(CoreDevice.GpioEventFormat, msg_data)
        return CoreDevice.GpioEvent(*unpkd)

    def make_can_event(msg_data):
        fmt = CoreDevice.CanEventFormat.format(dlc=len(msg_data)-(8+3))
        unpkd = struct.unpack(fmt, msg_data)
        return CoreDevice.CanEvent(*unpkd)

    def send_message(self, aMessage):
        if self.serial_port is None:
            return False
        # assume that message is well-formatted according to our protocol
        # otherwise, add a "validateMessage" function
        self.serial_port.write(aMessage)
        return True

    def read_all_messages(self):
        receive_buffer = bytearray(2048)        # its size should be aligned with core seding buffer
        read_bytes = self.serial_port.readinto(receive_buffer)

        start_positions = []
        i = 0
        while (i < read_bytes):
            start_positions.append(i)
            i += receive_buffer[i]

        all_messages = []
        for pos in start_positions:

            msg_len = receive_buffer[pos]
            msg_type_intf = receive_buffer[pos+1]
            msg_data = receive_buffer[pos:pos+msg_len]

            if msg_type_intf == 0x03:         # gpio event
                all_messages.append( CoreDevice.make_gpio_event(msg_data) )
            elif msg_type_intf == 0x23:       # can event
                all_messages.append( CoreDevice.make_can_event(msg_data) )
            else:
                print('debug: {} from bytes: {}'.format(msg_type_intf, msg_data))
                raise ValueError

        return all_messages

    def expect_gpio_event(self, waitFor, canIdMask):
        # this implementation bloks for that period, no matter how soon that event arrived
        sleep(waitFor)

        gpio_events = [ev for ev in self.read_all_messages() if ev.typeIntf == 0x03]
        selected_events = [ev for ev in gpio_events if ev.port & portMask]
        return selected_events

    def expect_can_event(self, waitFor, portMask):
        # this implementation bloks for that period, no matter how soon that event arrived
        sleep(waitFor)

        gpio_events = [ev for ev in self.read_all_messages() if ev.typeIntf == 0x23]
        selected_events = [ev for ev in gpio_events if ev.can_id & canIdMask]
        return selected_events


def main():

    serial_devices = list(list_ports.grep('0403:6001'))     # search a box core device
    port = Serial(serial_devices[0].device, baudrate=115200, timeout=0.2) # always pick first device
    box = CoreDevice(serialPort=port)
    box.open_connection()

    while True:
        messages = box.read_all_messages()
        print( messages )
        sleep( 0.5 )

if __name__ == '__main__':
    main()