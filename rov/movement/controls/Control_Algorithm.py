from PID_Controller import PID
import time

# Control Algorithm
# README:
#   Initalize with the parameter and sensor data
#   Parameter being either 'x', 'y', 'z', 'roll', 'pitch' or 'yaw'
#   Data from the sensors containing pressure or IMU
#   The calculate function uses change in time, current position, desired position as inputs for the PID controller.
#   This then returns a 6 degree output as the recommended user input to best achieve the desired position
#   This algorithm has the option to activate and deactivate itself with the default being deactivated
#   If deactived it always returns an empty output of the six degrees of freedom [0,0,0,0,0,0]
#   This also allows tuning of the PID values by using @property to change and refer to the PID values of the controller.
# How to used Control Algorithm class:
# 1. control = ControlAlorithm('roll')
#   -Initially deactivated
# 2. control.activate()
# 3. output = control.calculate()
# 4. output will now contain an array of the suggested output
# ex: [0, 0, 0, 0.5, 0, 0]
# - If you wish to turn off the algorithm use: control.deactivate()
# - This will cause calculate() to return an empty array: [0, 0, 0, 0, 0, 0]
# - If you wish to turn back on use: control.activate()
# - You can also use .toggle() to toggle between activated and deactivated
# - For PID tuning you can directly get and set the values using .p, .i, .d
# - ex: control.p = 5 or control.d = 2


class ControlAlgorithm():

    def __init__(self, parameter, sensor_data, tag):
        self._tag = tag
        self._activated = False
        self._parameter = parameter
        self._desired_position = 0
        self._pid = PID(0)
        self._previous_time = time.time()
        self._dof = 0
        self._xdata = []
        self._y1data = []
        self._y2data = []
        self._count = 0
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
        self._has_data = False

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

    # ensures quickest route to desired position
    def _error(self):
        error = self._desired_position - self._current_position()
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

    def getActivated(self):
        return self._activated

    def toggle(self):
        if self._activated:
            self.deactivate()
        else:
            self.activate()

    #allows potential opportunity of a velocity user input rather than thrust
    def get_desired_position(self):
        return self._desired_position
    
    def set_desired_position(self, value):
        self._desired_position = value

    def get_xdata(self):
        return self._xdata

    def get_y1data(self):
        return self._y1data

    def get_y2data(self):
        return self._y2data

    def has_data(self):
        return self._has_data
    
    def get_tag(self):
        return self._tag

    def calculate(self):         
        if self._activated:
            delta_time = time.time() - self._previous_time
            self._previous_time = time.time()
            value = self._pid.calculate(self._error(), delta_time)

            if value > 1:
                value = 1
            elif value < -1:
                value = -1

            self._output[self._dof] = value
            if self._count == 0:
                self._xdata.append(0)
                self._has_data = True
            else:
                self._xdata.append(self._xdata[self._count - 1] + delta_time)  
            self._y1data.append(self._current_position())
            self._y2data.append(self._desired_position)
            self._count += 1

        else:
            self.reset()
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
        self._desired_position = self.current_position()
        self._pid.reset(0)
        self._previous_time = time.time()
        self._output = [0, 0, 0, 0, 0, 0]

    def _x(self):
        return self._sensor['imu']['linear-acceleration']['x']
    def _y(self):
        return self._sensor['imu']['linear-acceleration']['y']
    def _z(self):
        return self._sensor['pressure']['pressure']
    def _roll(self):
        return self._sensor['imu']['euler']['roll']
    def _pitch(self):
        return self._sensor['imu']['euler']['pitch']
    def _yaw(self):
        return self._sensor['imu']['euler']['yaw']

