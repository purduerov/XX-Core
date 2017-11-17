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
        self.reset()

    def deactivate(self):
        self._activated = False
        self._dof = [0,0,0,0,0,0]

    @property
    def desired_position(self):
        return self._desired_position

    @desired_position.setter
    def desired_position(self, value):
        self._desired_position = value

    #todo: make for one degree of freedom
    def calculate(self):
        if self._activated:
            delta_time = time.time() - self._previous_time
            self._previous_time = time.time()
            error = self._desired_position - self.get_current_position()
            #resets integral term if there is no error
            #if error == 0:
            #    self._pid.reset(0)
            output = self._pid.calculate(error, delta_time)

            if output > 1:
                output = 1
            elif output < -1:
                output = -1

            self._dof[self._parameter] = output
        return self._dof

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
        self._pid.reset(self._desired_position - self.get_current_position())
        self._previous_time = time.time()