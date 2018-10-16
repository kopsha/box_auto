import unittest
import sys

from struct import pack
from struct import unpack

from time import sleep

from serial import Serial
from serial.tools import list_ports

from box_auto import CoreDevice

class AccelerationFixture(unittest.TestCase):
    """Acceleration from 0 to 25 kmh test suite"""

    def setUp(self):
        self.assertTrue('box_auto' in sys.modules)

        serial_devices = list(list_ports.grep('0403:6001'))
        self.assertTrue(serial_devices)
        port = Serial(serial_devices[0].device, baudrate=115200, timeout=0.2) # always pick first device
        self.box = CoreDevice(serialPort=port)

        self.assertTrue( self.box.open_connection() )

    def tearDown(self):
        self.assertTrue( self.box.close_connection() )

    def test_steady_acceleration(self):
        top_speed = 25
        for sim_speed in range(top_speed):
            can_id = 0x403          # assumption this is the speed can id
            can_data = pack('B', sim_speed)
            msg_data = self.box.make_can_message(can_id, can_data)
            was_ok = self.box.send_message(msg_data)
            self.assertTrue(was_ok)

            sleep(0.04)      # 40ms

            # self.assertEqual( can_id, msg.get('can_id') )
            # actual_speed = unpack('B', msg.get('can_data', 0xff))[0]
            # self.assertEqual( sim_speed, actual_speed )

    def test_steady_breaking(self):
        top_speed = 25
        for sim_speed in reversed(range(top_speed)):
            can_id = 0x403          # assumption this is the speed can id
            can_data = pack('B', sim_speed)
            msg_data = self.box.make_can_message(can_id, can_data)
            was_ok = self.box.send_message(msg_data)
            self.assertTrue(was_ok)

            sleep(0.04)      # 40ms

def main():
    # start the bloody tests
    unittest.main(verbosity=2, buffer=True)

if __name__ == '__main__':
    main()
