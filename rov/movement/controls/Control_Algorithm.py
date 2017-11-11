from rov.controls.PID_Controller import PID
import time

class ControlAlgorithm():

    def __init__(self, desired_position, parameter):
        self._activated = False
        self._parameter = parameter
        self._desired_position = desired_position
        self._pid = PID(desired_position - self.get_current_position())
        self._previous_time = time.time()
        self._dof = [0,0,0,0,0,0]

    def get_current_position(self):
        #todo: implement position finding
        return 1

    def activate(self):
        self._activated = True

    def deactivate(self):
        self._activated = False

    @property
    def activated(self):
        return self._activated

    @property
    def desired_position(self):
        return self._desired_position

    @desired_position.setter
    def desired_position(self, value):
        self._desired_position = value

    #todo: make for one degree of freedom
    def calculate(self):
        delta_time = time.time() - self._previous_time
        self._previous_time = time.time()
        error = self._desired_position - self.get_current_position()
        #resets integral term if there is no error
        if error == 0:
            self._pid.reset(0)
        output = self._pid.calculate(error, delta_time)

        if output > 1:
            output = 1
        elif output < -1:
            output = -1

        self._dof[self._parameter] = output
        if self.activated:
            return self._dof
        else:
            return [0,0,0,0,0,0]

    #tuner
    def set_p(self, value):
        self._pid.p = value

    def set_i(self, value):
        self._pid.i = value

    def set_d(self, value):
        self._pid.d = value

    def get_p(self):
        return self._pid.p

    def get_i(self):
        return self._pid.i

    def get_d(self):
        return self._pid.d