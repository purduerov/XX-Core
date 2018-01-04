import Adafruit_BNO055


class IMU(object):
    def __init__(self):
        # IMU Reset Pin connected to Pin 18
        self._bno = BNO055.BNO055(rst=18)

        # Fail if it cannot be initialized
        if not self._bno.begin():
            raise RuntimeError('Failed to initialize BNO055!')

        self._data =  {
            'euler': {
                'yaw':   0,
                'roll':  0,
                'pitch': 0,
            },
            'gyro': {
                'x': 0,
                'y': 0,
                'z': 0,
            },
            'acceleration': {
                'x': 0,
                'y': 0,
                'z': 0,
            },
            'linear-acceleration': {
                'x': 0,
                'y': 0,
                'z': 0,
            },
            'temp': 0,
        }

    @property
    def data(self):
        return self._data

    def update(self):
        euler = self._bno.read_euler()
        self._data['euler']['yaw']     = euler[0]
        self._data['euler']['roll']    = euler[1]
        self._data['euler']['pitch']   = euler[2]

        gyro = self._bno.read_gyroscrope()
        self._data['gyro']['x'] = gyro[0]
        self._data['gyro']['y'] = gyro[1]
        self._data['gyro']['z'] = gyro[2]

        acceleration = self._bno.read_accelerometer()
        self._data['acceleration']['x'] = acceleration[0]
        self._data['acceleration']['y'] = acceleration[1]
        self._data['acceleration']['z'] = acceleration[2]

        linear_accel = self._bno.read_linear_acceleration()
        self._data['linear-acceleration']['x'] = linear_accel[0]
        self._data['linear-acceleration']['y'] = linear_accel[1]
        self._data['linear-acceleration']['z'] = linear_accel[2]

        temp = self._bno.read_temp()
        self._data['temp'] = temp

    def get_calibration(self):
        return self._bno.get_calibration()

    def reset_calibration(self):
        cal_array_original = self.get_calibration()
        self._bno.set_calibration(self._bno.get_calibration())
        return cal_array_original

    def set_calibration(self, data):
        self._bno.set_calibration(data)

    def sitrep (self):
        sys, gyro, accel, mag = self._bno.get_calibration_status()
        sys_stat, sys_test, sys_err = self._bno.get_system_status(True)
        good_status = [3,3,3,3,1,0x0F,0]
        test_array = [sys,gyro,accel,mag,sys_stat, sys_test, sys_err]

        for x in range(0, 4):
            if test_array[x] != 3:
                return False

        if test_array[4] == 1:
            return False

        if test_array[5] != 0x0F:
            return False

        if test_array[6] != 0:
            return False

        return True

