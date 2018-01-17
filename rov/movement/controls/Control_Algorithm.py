from rov.controls.PID_Controller import PID
import time
from rov.sensors.imu.IMU_Mock import IMU
from rov.sensors.pressure.Pressure_Mock import Pressure

# Control Algorithm
# README:
#   Initalized using one of the parameters either 'x', 'y', 'z', 'roll', 'pitch' or 'yaw' and the data from the sensors containing pressure or IMU
#   The calculate function uses change in time, current position, desired position as inputs for the PID controller.
#   This then returns a 6 degree output as the recommended user input to best achieve the desired position
#   This algorithm has the option to activate and deactivate itself with the default being deactivated
#   If deactived it always returns an empty output of the six degrees of freedom [0,0,0,0,0,0]
#   This also allows tuning of the PID values by using @property to change and refer to the PID values of the controller.
#
#   TODO: Give quick step by step of how someone should use the class externally.
#   TODO: Update function names with _ to designate private functions, helps users of the class understand what they should touch and what they shouldn't.
#   TODO: Update given new way of performing sensor data updating.
#


class ControlAlgorithm():

    def __init__(self, parameter, sensor_data):
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

        # sets sensor data and the proper function to retrieve the right data from _sensor
        self._sensor = sensor_data
        self._current_position = [self._x, self._y, self._z, self._roll, self._pitch, self._yaw][self._dof]



    def current_position(self):
	if self._dof == 0:
	    return self._x()
	elif self._dof == 1:
	    return self._y()
	elif self._dof == 2:
	    return self._z()
	elif self._dof == 3:
	    return self._roll()
	elif self._dof == 4:
	    return self._pitch()
	elif self._dof == 5:
	    return self._yaw()

    # TODO: what is current_position? vs _current_position? Use _current_position()
	# ensures quickest route to desired position
    def calculate_error(self, current_position):
        error = self._desired_position - current_position
        if self._parameter > 2:
            if error > 180:
                error -= 360
            elif error < -180:
                error += 360
        return error

    def activate(self):
        self._activated = True
        self._desired_position = self.current_position()
        self.reset()

    def deactivate(self):
        self._activated = False
        self._output = [0,0,0,0,0,0]

    # TODO: This looks like an unused or old function. Remove if so.
    def lock_position(self):
        self.activate(self.current_position())

    @property
    def desired_position(self):
        return self._desired_position

    # TODO: Does this have any practical use? When should this be called? And can it be included as a parameter to a function instead?
    @desired_position.setter
    def desired_position(self, value):
        self._desired_position = value

    # See todo above about current_position
    def calculate(self):
        if self._activated:
            delta_time = time.time() - self._previous_time
            self._previous_time = time.time()
            error = self.calculate_error(self._current_position())
            #resets integral term if there is no error
            #if error == 0:
            #    self._pid.reset(0)
            # TODO: I'm getting a divide by 0 inside this on sample data...
            output = self._pid.calculate(error, delta_time)

            if output > 1:
                output = 1
            elif output < -1:
                output = -1

            # TODO: What is the difference between _output and output????
            self._output[self._parameter] = output

        # TODO: Should this be reset to or unmodified if self._activated is not True?
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

    def _x(self):
        print('_x')
        self._sensor['linear-acceleration']['x'] = 2
        return self._sensor['linear-acceleration']['x']
    def _y(self):
        return self._sensor['linear-acceleration']['y']
    def _z(self):
        return self._sensor['pressure']
    def _roll(self):
        return self._sensor['euler']['roll']
    def _pitch(self):
        return self._sensor['euler']['pitch']
    def _yaw(self):
        return self._sensor['euler']['yaw']

