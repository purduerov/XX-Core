from smbus import SMBus
import time

class Rov(object):

    def _intialize(rov):
        rov.bus = SMBus(1)

        rov._data = {
        # default pressure and temperature

            "pressure": 0,
            "temperature": 0,
        }


    @property
    def data(rov):
        return rov._data


    def update(rov):
        # address of the arduino
        address = 0x76
        # to tell the arduino the request number
        request = 0xAA

        rov.bus.write_byte(address, request)
        time.sleep(.5)


