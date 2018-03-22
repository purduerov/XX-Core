from math import sin, pi


class IMU(object):
    """Mock IMU class
    """

    def __init__(self):
        self.accel_x = 0
        self.accel_y = 0
        self.accel_z = 0
        self.pitch = 0
        self.roll = 0
        self.yaw = 0

        self._angle = 0

    def update(self):
        self._angle += 1
        self.roll = sin(self._angle * (pi)/180.0)

    @property
    def data(self):
        return  {
            'euler': {
                'yaw':   self.yaw,
                'roll':  self.roll,
                'pitch': self.pitch,
            },
            'gyro': {
                'x': 0,
                'y': 0,
                'z': 0,
            },
            'acceleration': {
                'x': self.accel_x,
                'y': self.accel_y,
                'z': self.accel_z,
            },
            'linear_acceleration': {
                'x': 0,
                'y': 0,
                'z': 0,
            },
            'temp': 0,
        }
