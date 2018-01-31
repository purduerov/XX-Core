from PID_Controller import PID
from Base_Algorithm import Algorithm
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


class MovementAlgorithm(Algorithm):
    
    def __init__(self, parameter, sensor_data):
        Algorithm.__init__(self, parameter, sensor_data)
        self._desired_speed = 0
        self._ready = False
        self._cp = 0
        self._lp = 0
        self._value = 0
        self._last_position = [0,0,0,0,0,0]
        self._scale = 100
        self._current_time = time.time()
        self._max_speed = 360

        # sets sensor data and the proper function to retrieve the right data from _sensor
        self._sensor = sensor_data


    def _error(self, speed):
        error = self._desired_speed - speed
        return error

    def _update(self):
        self._lp = self._cp
        self._cp = self._current_position(self._dof)
        self._previous_time = self._current_time
        self._current_time = time.time()

    def set_max_speed(self, value);
        self._max_speed = value

    def calculate(self, desired_speed):
        self._desired_speed = desired_speed * self._max_speed 
        if self._activated:
            self._update()
            if self._ready:    
                delta_time = time.time() - self._previous_time
                speed = (self._cp - self._lp) / delta_time
                self._value += self._pid.calculate(self._error(speed), delta_time)/self._scale
                if self._value > 1:
                    self._value = 1
                elif self._value < -1:
                    self._value = -1
                self._output[self._dof] = self._value
        
                if self._count == 0:
                    self._graph_data[0].append(0)
                    self._has_data = True
                else:
                    self._graph_data[0].append(self._graph_data[0][self._count - 1] + delta_time)
                self._count += 1
                self._graph_data[1].append(speed)
                self._graph_data[2].append(self._desired_speed)
            else:
               self._ready = True
               self._output[self._dof] = 0.0
        
        else:
            self._reset()

        return self._output

    def _reset(self):
        self._pid.reset(0)
        self._previous_time = time.time()
        self._output = [0, 0, 0, 0, 0, 0]
        self._value = 0


