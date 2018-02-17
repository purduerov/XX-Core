from smbus import SMBus
import ms5837
import time

class Pressure(object):

    def __init__(self):
        self.bus = SMBus(1)

        self._data = {
            "pressure": 0,
            "temperature": 0,
        }

    @property
    def data(self):
        return self._data

    def update(self):
        # pressure in mBars
        pressure = sensor.pressure()
        self._data['pressure'] = pressure

        # Temp in celsius
        temperature = sensor.temperature()
        self._data['temperature'] = temperature
if __name__ == "__main__": 
				p = Pressure()
				print "hello"

