import unittest
import sys

from struct import pack
from struct import unpack

from time import time
from time import sleep
from sched import scheduler

from serial import Serial
from serial.tools import list_ports

from box_auto import CoreDevice

class AccelerationFixture(unittest.TestCase):
    """Acceleration and breaking test suite"""

    def setUp(self):
        self.assertTrue('box_auto' in sys.modules)      # import was successful

        serial_devices = list(list_ports.grep('0403:6001'))     # search a box core device
        self.assertTrue(serial_devices)
        port = Serial(serial_devices[0].device, baudrate=115200, timeout=0.2) # always pick first device

        self.box = CoreDevice(serialPort=port)
        self.assertTrue( self.box.open_connection() )

    def tearDown(self):
        self.assertTrue( self.box.close_connection() )

    def test_firmware_version(self):
        firmware_response = self.box.get_firmware_version()
        self.assertEqual( firmware_response.typeIntf, 0x64 )
        self.assertEqual( firmware_response.response_id, 0x04 )
        self.assertTrue( firmware_response.payload )    # a.k.a. not-empty

    def test_hardware_version(self):
        hardware_response = self.box.get_hardware_version()
        self.assertEqual( hardware_response.typeIntf, 0x64 )
        self.assertEqual( hardware_response.response_id, 0x05 )
        self.assertTrue( hardware_response.payload )    # a.k.a. not-empty

    def test_steady_acceleration(self):
        top_speed = 25
        for sim_speed in range(top_speed):
            can_id = 0x403          # assumption this is the speed can id
            can_data = pack('B', sim_speed)
            msg_data = self.box.make_can_message(can_id, can_data)
            was_ok = self.box.send_message(msg_data)
            self.assertTrue(was_ok)
            sleep(0.04)      # 40ms

    def test_supportlevels_steady_breaking(self):
        top_speed = 25
        for sim_speed in reversed(range(top_speed)):
            can_id = 0x403          # assumption this is the speed can id
            can_data = pack('B', sim_speed)
            msg_data = self.box.make_can_message(can_id, can_data)
            was_ok = self.box.send_message(msg_data)
            self.assertTrue(was_ok)
            sleep(0.04)      # 40ms

    def test_expect_gpio_event(self):
        def check_event_queue(box):
            messages = self.box.read_all_messages()
            #self.assertTrue( messages )    # example code no actual testing

        boss = scheduler(time, sleep)
        howLong = 1
        boss.enter(delay=howLong, priority=3, action=check_event_queue, argument=(self.box,))
        boss.run()

def main():
    # start the bloody tests
    unittest.main(verbosity=2, buffer=True)

if __name__ == '__main__':
    main()
