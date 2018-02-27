from smbus import SMBus
import ms5837
import time
class Pressure(object):
    
    def __init__(self,PressDepthConv=0.01):
        self.bus = SMBus(1)
        self.sensor = ms5837.MS5837_30BA()
        if not self.sensor.init():
            print "Sensor not initialized"
            exit(1)

        if not self.sensor.read():
            print "Sensor read failed"
            exit(1)

        self._data = {
            "pressure": 0, # +/- 50  milibars
            "temperature": 0 # +/- 1.5 Celcius
        }
        self.initPressure = 0
        self.conv = PressDepthConv
        self.update()
        self.initPressure = self._data['pressure']

    @property
    def data(self):
        self._data['depth'] = self._data['pressure']*self.conv # Perhaps add temperature accounting
        return self._data

    def update(self):
        time.sleep(0.5)
        if self.sensor.read():
            # pressure in mBars
            pressure = self.sensor.pressure() - self.initPressure
            self._data['pressure'] = pressure

            # Temp in celsius
            temperature = self.sensor.temperature()
            self._data['temperature'] = temperature
        else:
            pass
