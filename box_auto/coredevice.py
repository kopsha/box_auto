import copy
import struct

def hello_world():
    print("hello core.")

class CoreDevice(object):
    """BoxIO CoreDevice interface"""
    def __init__(self, serialPort):
        super(CoreDevice, self).__init__()
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

    def make_can_message(self, can_id, can_data):
        msg = {
            'type': 0x00,
            'interface': 0x02,
            'length': 2 + 3 + len(can_data),
            'can_id': copy.deepcopy(can_id),
            'can_data': copy.deepcopy(can_data) 
        }

        mTypeIntf = (0x0 << 4) | 0x2
        mLen = 2 + 4 + len(can_data)
        box_can_format = '>B B L B {}s'.format(len(can_data))
        data = struct.pack( box_can_format, mLen, mTypeIntf, can_id, len(can_data), can_data )
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
