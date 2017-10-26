from math import sin, pi


class Pressure(object):
    """Mock Pressure Sensor class
    """

    def __init__(self):
        self.pressure = 0
        self.temperature = 0

        self._angle = 0

    def update(self):
        self._angle += 1
        self.pressure = 1000 + sin(self._angle * (pi)/180.0)

    @property
    def data(self):
        return {
            "temperature": self.temperature,
            "pressure": self.pressure
        }
