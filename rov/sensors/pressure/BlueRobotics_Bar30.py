from smbus import SMBus
import ms5837
import time
class Pressure(object):
    
    def __init__(self):
        self.bus = SMBus(1)
        self.sensor = ms5837.MS5837_30BA()
        if not self.sensor.init():
            print "Sensor not initialized"
            exit(1)

        if not self.sensor.read():
            print "Sensor read failed"
            exit(1)

        self._data = {
            "pressure": 0,
            "temperature": 0
        }

    @property
    def data(self):
        return self._data

    def update(self):
        # pressure in mBars
        pressure = self.sensor.pressure()
        self._data['pressure'] = pressure

        # Temp in celsius
        temperature = self.sensor.temperature()
        self._data['temperature'] = temperature
if __name__ == "__main__": 
				p = Pressure()
                                print "pressure:"
                                p.update()
                                print p._data['pressure']
                                print "temperature:"
                                print p._data['temperature']

