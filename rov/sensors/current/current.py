from smbus import SMBus
import time


class Current(object):

    def __init__(self):
        self.bus = SMBus(1)

        self._data = {
            #float
            "thruster1": 0,
            "thruster2": 0,
            "thruster3": 0,
            "thruster4": 0,
            "thruster5": 0,
            "thruster6": 0,
            "thruster7": 0,
            "thruster8": 0,
            "claw": 0,
            "obs": 0,
            "electromagnet": 0,
            "transmitter": 0,
        }

    @property
    def data(self):
        return self._data

    def update(self):
        self.bus.write_byte(0x43, 0x78)
        #time.sleep(.5)
        # Read 32 bytes of data
        data = self.bus.read_i2c_block_data(0x43, 0, 32)
        
        # Set thruster 1
        self._data['thruster1'] = data[0] * 256 + data[1]
        # Set thruster 2
        self._data['thruster2'] = data[2] * 256 + data[3]
        # Set thruster 3
        self._data['thruster3'] = data[4] * 256 + data[5]
        # Set thruster 4
        self._data['thruster4'] = data[6] * 256 + data[7]
        # Set thruster 5
        self._data['thruster5'] = data[8] * 256 + data[9]
        # Set thruster 6
        self._data['thruster6'] = data[10] * 256 + data[11]
        # Set thruster 7
        self._data['thruster7'] = data[12] * 256 + data[13]
        # Set thruster 8
        self._data['thruster8'] = data[14] * 256 + data[15]
        # Set claw
        self._data['claw'] = data[16] * 256 + data[17]
        # Set obs
        self._data['obs'] = data[18] * 256 + data[19]
        # Set electromagnet
        self._data['electromagnet'] = data[20] * 256 + data[21]
        # Set transmitter
        self._data['transmitter'] = data[22] * 256 + data[23]

