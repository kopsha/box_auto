import struct
import binascii
from collections import namedtuple

class CoreDevice(object):
    """BoxIO CoreDevice interface"""
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
        MessageHeader = namedtuple('MessageHeader', ['length', 'typeIntf', 'payload'])
        firmware_rq = MessageHeader( 3, 0x62, 0x04 )
        rq_data = struct.pack('>BBB', *firmware_rq)
        self.serial_port.write( rq_data )
        self.serial_port.flush()

        receive_buffer = bytearray(64)
        size = self.serial_port.readinto(receive_buffer)
        response_data = receive_buffer[:receive_buffer[0]]
        ResponseHeader = namedtuple('ResponseHeader', ['length', 'typeIntf', 'response_id', 'payload'])

        response_fmt = 'BBB{}s'.format(response_data[0]-3)
        response = ResponseHeader( *struct.unpack(response_fmt, response_data) )

        return response

    def get_hardware_version(self):
        MessageHeader = namedtuple('MessageHeader', ['length', 'typeIntf', 'payload'])
        hardware_rq = MessageHeader( 3, 0x62, 0x05 )
        rq_data = struct.pack('>BBB', *hardware_rq)
        self.serial_port.write( rq_data )
        self.serial_port.flush()

        receive_buffer = bytearray(64)
        size = self.serial_port.readinto(receive_buffer)
        response_data = receive_buffer[:receive_buffer[0]]
        ResponseHeader = namedtuple('ResponseHeader', ['length', 'typeIntf', 'response_id', 'payload'])

        response_fmt = 'BBB{}s'.format(response_data[0]-3)
        response = ResponseHeader( *struct.unpack(response_fmt, response_data) )

        return response

    def make_can_message(self, can_id, can_data):
        mTypeIntf = (0x0 << 4) | 0x2
        mLen = 2 + 4 + len(can_data)
        box_can_format = '>BBLB{}s'.format(len(can_data))
        data = struct.pack(box_can_format, mLen, mTypeIntf, can_id, len(can_data), can_data)
        return data

    def send_message(self, aMessage):
        if self.serial_port is None:
            return False
        # assume that message is well-formatted according to our protocol
        # otherwise, add a "validateMessage" function
        self.serial_port.write(aMessage)
        return True

    def read_all_messages(self):
        print('CoreDevice.read_messages, should return []')
        return []
