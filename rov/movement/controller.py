from __future__ import print_function
from controller_constants import *
from hardware.Thrusters_PWM_Control import Thrusters
from mapper.Complex_1 import Complex
# from mapper.Simple import Mapper
from controls.Algorithm_Handler import Master_Algorithm_Handler
import copy

class controller(object):
    def __init__(self, motor_control, data):

        self.motor_control = motor_control
        self._data = data
        self.df = data['dearflask']
        self.dc = data['dearclient']

        self.thrusters = Thrusters(
            self.motor_control,
            LIST_OF_THRUSTER
        )

        self.thrust_mapper = Complex()

        self.algorithm_handler = Master_Algorithm_Handler(self._data['dearflask']["thrusters"]["frozen"], self._data['dearclient']["sensors"])

        self._previous_desired_thrust = [0,0,0,0,0,0]

        self.__thruster_values = [0,0,0,0,0,0,0,0]

    def update(self):

        self.algorithm_handler.master(self._data['dearflask']["thrusters"]["desired_thrust"], self._data['dearflask']["thrusters"]["disabled_thrusters"])

        new_desired_thrust = [0 for _ in range(len(self._data['dearflask']["thrusters"]["desired_thrust"]))]

        for index, value in enumerate(self._data['dearflask']["thrusters"]["desired_thrust"]):
            new_desired_thrust[index] = self._data['dearflask']["thrusters"]["desired_thrust"][index]

            difference = value - self._previous_desired_thrust[index]
            if abs(difference) > abs(value / 2.0):
                new_desired_thrust[index] -= (difference/2.0)

        thruster_values = self.thrust_mapper.calculate(new_desired_thrust, self._data['dearflask']["thrusters"]["disabled_thrusters"])

        # Account for dynamically inverted thrusters:
        for i in range(0,8):
            thruster_values[i] *= self._data['dearflask']['thrusters']['inverted_thrusters'][i]

        self.thrusters.set(thruster_values)

        self.__thruster_values = thruster_values

        self._previous_desired_thrust = copy.deepcopy(new_desired_thrust)

        #print (self._data['dearflask']['thrusters']['desired_thrust'])
        #for i in thruster_values:
        #    print ("%.3f, " % i, end='')
        #print ('')

    @property
    def data(self):
        return self.__thruster_values

    def stop_thrusters(self):
        self.thrusters.stop()

    def get_thruster_values(self):
        """The value of each thruster returned as a list"""
        return self.thrusters.get()

    def set_thruster_values(self, values):
        """A decorated function for setting the thruster values"""
        self.thrusters.set(values)


