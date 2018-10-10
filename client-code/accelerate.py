import unittest
import sys
from time import sleep

import box_auto

class AccelerationFixture(unittest.TestCase):
    """Acceleration from 0 to 25 kmh test suite"""

    def setUp(self):
        self.assertTrue('box_auto' in sys.modules)
        #To add here:
        # * connect to box-core device
        # * setup baud-rate to device

    def tearDown(self):
        #print('tearDown')
        pass

    def test_steady_acceleration(self):
        top_speed = 25
        for sim_speed in range(top_speed):
            can_frame = {
                'speed' : sim_speed
            }
            # box_auto.send_can_frame(frame=can_frame)
            sleep(0.04)      # 40ms
            actual_speed = can_frame.get('speed') # instead of box_auto.get_frame().get('speed')
            self.assertEqual( sim_speed, actual_speed )

    def test_steady_breaking(self):
        top_speed = 25
        for sim_speed in reversed(range(top_speed)):
            can_frame = {
                'speed' : sim_speed
            }
            # box_auto.send_can_frame(frame=can_frame)
            sleep(0.04)      # 40ms
            actual_speed = can_frame.get('speed') # instead of box_auto.get_frame().get('speed')
            self.assertEqual( sim_speed, actual_speed )


def main():
    # start the bloody tests
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()
