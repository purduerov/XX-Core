from Adafruit_BNO055 import BNO055 as _BNO055


class BNO055(object):
    def __init__(self):
        # IMU Reset Pin connected to Pin 18
        self._bno = _BNO055.BNO055(rst=18)

        # Fail if it cannot be initialized
        if not self._bno.begin():
            raise RuntimeError('Failed to initialize BNO055!')

        self._data =  {
            'euler': {
                # Resolution found from a forumn post
                'yaw':   0,  # Rotation about z axis (vertical) +/- 0.01 degree
                'roll':  0,  # Rotation about y axix (perpindicular to the pins IMU) +/- 0.01 degree
                'pitch': 0,  # Rotation about x axis (parallel to the pins of IMU) +/- 0.01 degree

            },
            'gyro': {
                'x': 0, # 3e-2 degree/sec
                'y': 0, # 3e-2 degree/sec
                'z': 0, # 3e-2 degree/sec
            },
            'acceleration': {
                'x': 0, # +/- 5e-4 g
                'y': 0, # +/- 5e-4 g
                'z': 0, # +/- 5e-4 g
            },
            'linear_acceleration': {
                'x': 0, # +/- 0.25 m/s^2
                'y': 0, # +/- 0.25 m/s^2
                'z': 0, # +/- 0.25 m/s^2
            },
            'temp': 0, # Good enough
        }

    @property
    def data(self):
        return self._data

    def roll(self):
        return self._data['euler']['roll']

    def pitch(self):
        return self._data['euler']['pitch']

    def yaw(self):
        return self._data['euler']['yaw']

    def gyro_x(self):
        return self._data['gyro']['x']
    def gyro_y(self):
        return self._data['gyro']['y']
    def gyro_z(self):
        return self._data['gyro']['z']

    def acceleration_x(self):
        return self._data['acceleration']['x']
    def acceleration_y(self):
        return self._data['acceleration']['y']
    def acceleration_z(self):
        return self._data['acceleration']['z']

    def linear_acceleration_x(self):
        return self._data['linear_acceleration']['x']
    def linear_acceleration_y(self):
        return self._data['linear_acceleration']['y']
    def linear_acceleration_z(self):
        return self._data['linear_acceleration']['z']


    def update(self):
        euler = self._bno.read_euler()
        self._data['euler']['yaw']     = euler[0]
        self._data['euler']['roll']    = euler[1]
        self._data['euler']['pitch']   = euler[2]

	gyro = self._bno.read_gyroscope()
        self._data['gyro']['x'] = gyro[0]
        self._data['gyro']['y'] = gyro[1]
        self._data['gyro']['z'] = gyro[2]

        acceleration = self._bno.read_accelerometer()
        self._data['acceleration']['x'] = acceleration[0]
        self._data['acceleration']['y'] = acceleration[1]
        self._data['acceleration']['z'] = acceleration[2]

        linear_accel = self._bno.read_linear_acceleration()
        self._data['linear_acceleration']['x'] = linear_accel[0]
        self._data['linear_acceleration']['y'] = linear_accel[1]
        self._data['linear_acceleration']['z'] = linear_accel[2]

        temp = self._bno.read_temp()
        self._data['temp'] = temp

        return True

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

if __name__ == '__main__':
    #BNO055().main()
    import time

    def main():
        sensor = BNO055() # Default I2C bus is 1 (Raspberry Pi 3)

        # We must initialize the sensor before reading it
        if not sensor:
                print "Sensor could not be initialized"
                exit(1)

        # We have to read values from sensor to update pressure and temperature
        #if not sensor.read():
        #    print "Sensor read failed!"
        #    exit(1)

        #print("Pressure: %.2f mbar") % (sensor.pressure())

        #print("Temperature: %.2f C") % (sensor.temperature(ms5837.UNITS_Centigrade))

        #time.sleep(2)

        print("Time \tRoll \tPitch \tYaw \tGyro: \tx \ty \tz \tACC: \tx \ty \tz \tLinear: \tx \ty \tz")

        # Spew readings
        while True:
                if sensor.update():
                    print("%s \t%0.2f \t%0.2f \t%0.2f \t\t%0.2f \t%0.2f \t%0.2f \t\t%0.2f \t%0.2f \t%0.2f \t\t%0.2f \t%0.2f \t%0.2f") % (time.strftime("%H:%M:%S", time.localtime()) + '.%d' % (time.time() % 1 * 1000),
                        sensor.roll(),
                        sensor.pitch(),
                        sensor.yaw(),
                        sensor.gyro_x(),
                        sensor.gyro_y(),
                        sensor.gyro_z(),
                        sensor.acceleration_x(),
                        sensor.acceleration_y(),
                        sensor.acceleration_z(),
                        sensor.linear_acceleration_x(),
                        sensor.linear_acceleration_y(),
                        sensor.linear_acceleration_z())

                    time.sleep(0.005)
                else:
                        print "Sensor read failed!"
                        exit(1)
       
    main()

