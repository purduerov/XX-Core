from rov.controls.PID_Controller import PID
import time
from rov.sensors.imu.IMU_Mock import IMU
from rov.sensors.pressure.Pressure_Mock import Pressure


class ControlAlgorithm():

    def __init__(self, parameter):
        self._activated = False
        self._parameter = parameter
        self._desired_position = 0
        self._pid = PID(0)
        self._previous_time = time.time()
        self._dof = 0
        if parameter == 'x':
            self._dof = 0
        elif parameter == 'y':
            self._dof = 1
        elif parameter == 'z':
            self._dof = 2
        elif parameter == 'roll':
            self._dof = 3
        elif parameter == 'pitch':
            self._dof = 4
        elif parameter == 'yaw':
            self._dof = 5
        self._output = [0,0,0,0,0,0]
        self._pressure = Pressure()
        self._imu = IMU()
        #possibly implement imu and pressure sensor

    def current_position(self):
        try:
            if self._dof > 2:
                return self._imu.data['euler'][self._parameter]
        except:
            print("ERROR: IMU SENSOR DATA")
            return self._desired_position

        try:
            if self._dof == 1:
                return self._pressure.data['pressure']
        except:
            print("ERROR: PRESSURE SENSOR DATA")
            return self.desired_position


    def calculate_error(self, current_position):
        error = self._desired_position - current_position
        if self._parameter > 2:
            if error > 180:
                error -= 360
            elif error < -180:
                error += 360
        return error

    def activate(self, desired_position):
        self._activated = True
        self._desired_position = desired_position
        self.reset(self.current_position())

    def deactivate(self):
        self._activated = False
        self._output = [0,0,0,0,0,0]

    def lock_position(self):
        self.activate(self.current_position())

    @property
    def desired_position(self):
        return self._desired_position

    @desired_position.setter
    def desired_position(self, value):
        self._desired_position = value

    def calculate(self, current_position):
        if self._activated:
            delta_time = time.time() - self._previous_time
            self._previous_time = time.time()
            error = self.calculate(current_position)
            #resets integral term if there is no error
            #if error == 0:
            #    self._pid.reset(0)
            output = self._pid.calculate(error, delta_time)

            if output > 1:
                output = 1
            elif output < -1:
                output = -1

            self._output[self._parameter] = output
        return self._output

    #tuner
    @property
    def p(self):
        return self._pid.p

    @p.setter
    def p(self, value):
        self._pid.p = value

    @property
    def i(self):
        return self._pid.i

    @i.setter
    def i(self, value):
        self._pid.i = value

    @property
    def d(self):
        return self._pid.d

    @d.setter
    def d(self, value):
        self._pid.d = value

    def reset(self):
        self._pid.reset(self._desired_position - self.current_position())
        self._previous_time = time.time()