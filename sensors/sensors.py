from imu.BNO055 import IMU
from pressure.BlueRobotics_Bar30 import Pressure


class Sensor(object):

    def __init__(self):
        self.imu = IMU()
        self.imu.update()
        self.pressure = Pressure()
        self.pressure.update()
        self._data = {'imu': self.imu.data,
                      'pressure': self.pressure.data}

    @property
    def data(self):
        return self._data

    def update(self):
        self.imu.update()
        self.pressure.update()
        self._data['imu'] = self.imu.data
        self._data['pressure'] = self.pressure.data
