from rov.controls.PID_Controller import PID
import time

class ControlAlgorithm():

    def __init__(self, desired_position):
        self.__activated = False
        #self.__parameter = parameter
        self.__pid = PID(0)
        #self.__sensor = sensor
        self.__desired_position = desired_position
        self.__previous_time = time.time()
        #todo: make so it only handles one variable

    @property
    def activated(self):
        return self.__activated

    @activated.setter
    def activated(self, value):
        self.__activated = value

    @property
    def desired_position(self):
        return self.__desired_position

    @desired_position.setter
    def desired_position(self, value):
        self.__desired_position = value

    #todo: make for one degree of freedom
    def calculate(self, current_position):
        delta_time = time.time() - self.__previous_time
        self.__previous_time = time.time()
        error = self.__desired_position - current_position
        if error == 0:
            self.__pid.reset(0)
        output = self.__pid.calculate(error, delta_time)

        if output > 1:
            output = 1
        elif output < -1:
            output = -1

        return output
