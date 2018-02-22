from PID_Controller import PID
from Base_Algorithm import Algorithm
import time
import math

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

#   NOTE: This will modify X, Y, and Z force so no Speed Stabilizers can be activated on X and Y when this is activated

class HeightStabilizer(Algorithm):

    def __init__(self, sensor_data):
        Algorithm.__init__(self, 2, sensor_data)
        self._desired_position = 0

    # calculates error for pid
    def _error(self):
        error = self._desired_position - self._current_position(self._dof)
        return error

    # calculates output for thrust mapper and graphs data
    def calculate(self):
        if self._activated:
            delta_time = time.time() - self._previous_time
            self._previous_time = time.time()
            value = self._pid.calculate(self._error(), delta_time)

            # caps max output value
            if value > 1:
                value = 1
                self._pid.reset_esum()
            elif value < -1:
                value = -1
                self._pid.reset_esum()

            # stores the sin(theta) output for these angles
            pitch = math.sin(self._current_position(4) * math.pi / 180)
            roll = math.sin(self._current_position(3) * math.pi / 180)

            # Calculates each component needed for upward motion
            x = -1 * pitch * value
            y = roll * value
            c = 1 - math.pow(roll, 2) - math.pow(pitch, 2)
            if c < 0:
                c = 0

            z = math.sqrt(c) * value

            # Places these values in the output vector
            self._output[0] = x
            self._output[1] = y
            self._output[2] = z

            # adds data to the graph
            if self._count == 0:
                self._graph_data[0].append(0)
                self._has_data = True
            else:
                self._graph_data[0].append(self._graph_data[0][self._count - 1] + delta_time)
            self._graph_data[1].append(self._current_position(self._dof))
            self._graph_data[2].append(self._desired_position)

            self._count += 1

        else:
            self._reset()
        return self._output

    # resets time and position values
    def _reset(self):
        self._pid.reset(0)
        self._desired_position = self._current_position(self._dof)
        self._previous_time = time.time()
        self._output = [0, 0, 0, 0, 0, 0]
