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

class Algorithm():

    def __init__(self, parameter, sensor_data):
        self._activated = False
        self._parameter = parameter
        self._sensor = sensor_data
        self._pid = PID(0)
        self._degrees = 360
        self._previous_time = time.time()
        self._dof = 0
        self._graph_data = [[], [], []]
        self._count = 0
        self._factor = [0,0,0,0,0,0]
        self._last_position = [0,0,0,0,0,0]
        self._position = [0,0,0,0,0,0]
        for dof in range(6):
            self._position[dof] = self._current_position(dof)
        self._dof = parameter
        self._output = [0,0,0,0,0,0]
        self._count = 0
        self._has_data = False
        # sets sensor data and the proper function to retrieve the right data from _sensor

    # returns position using sensor data
    def _current_position(self, dof):
        if dof == 0:
            self._last_position[dof] = self._position[dof]
            self._position[dof] = self._sensor['imu']['linear_acceleration']['x']
            return self._position[dof]

        elif dof == 1:
            self._last_position[dof] = self._position[dof]
            self._position[dof] = self._sensor['imu']['linear_acceleration']['y']
            return self._position[dof]

        elif dof == 2:
            self._last_position[dof] = self._position[dof]
            self._position[dof] = self._sensor['pressure']['pressure']
            return self._position[dof]

        elif dof == 3:
            self._last_position[dof] = self._position[dof]
            position = self._sensor['imu']['euler']['roll']
            self._jump(position, dof)
            self._position[dof] = position + self._factor[dof] * self._degrees
            return self._position[dof]

        elif dof == 4:
            self._last_position[dof] = self._position[dof]
            position = self._sensor['imu']['euler']['pitch']
            self._jump(position, dof)
            self._position[dof] = position + self._factor[dof] * 360
            return self._position[dof]

        elif dof == 5:
            self._last_position[dof] = self._position[dof]
            position = self._sensor['imu']['euler']['yaw']
            self._jump(position, dof)
            self._position[dof] = position + self._factor[dof] * 360
            return self._position[dof]

    def _position_raw(self, dof):
        position = 0

        if dof == 0:
            position = self._sensor['imu']['linear_acceleration']['x']

        elif dof == 1:
            position = self._sensor['imu']['linear_acceleration']['y']

        elif dof == 2:
            position = self._sensor['pressure']['pressure']

        elif dof == 3:
            position = self._sensor['imu']['euler']['roll']

        elif dof == 4:
            position = self._sensor['imu']['euler']['pitch']

        elif dof == 5:
            position = self._sensor['imu']['euler']['yaw']

        if dof > 2:
            if position >= 180:
                position -= 360

        return position

    def _error(self):
        pass

    # checks if algorithm is activated
    def get_activated(self):
        return self._activated

    # activated algorithm
    def activate(self):
        self._activated = True
        self._reset()

    # deactivates algorithm
    def deactivate(self):
        self._activated = False
        self._output = [0,0,0,0,0,0]

    # toggles activation state
    def toggle(self):
        if self._activated:
            self.deactivate()
        else:
            self.activate()

    # returns data of pid controllers
    def get_data(self):
        return self._graph_data

    def has_data(self):
        return self._has_data

    def calculate(self):
        pass

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

    def _reset(self):
        pass

    # scales data past 0 and 360
    def _jump(self, position, dof):
        degrees = self._degrees
        margin = 30
        if position > degrees - margin and self._last_position[dof] < margin:
            self._factor[dof] = self._factor[dof] - 1
        elif position < margin and self._last_position[dof] > degrees - margin:
            self._factor[dof] = self._factor[dof] + 1
