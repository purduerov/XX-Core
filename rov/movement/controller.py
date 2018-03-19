from controller_constants import *
from hardware.Thrusters_PWM_Control import Thrusters
from mapper.Simple import Mapper

class controller(object):
    def __init__(self, motor_control):

        self.motor_control = motor_control

        self.thrusters = Thrusters(
            self.motor_control,
            LIST_OF_THRUSTER
        )

        self.thrust_mapper = Mapper()

        self.__thruster_values = {}

    def update(self, user_thruster_input):

        # TODO: Add master Control Handler

        # TODO: Add thrust limiter

        # Thrust Mapper
        thruster_values = self.thrust_mapper.calculate(user_thruster_input["desired_thrust"])

        self.thrusters.set(thruster_values)

        return self.thrusters.get()

    def stop_thrusters(self):
        self.thrusters.stop()

    def get_thruster_values(self):
        """The value of each thruster returned as a list"""
        return self.thrusters.get()

    def set_thruster_values(self, values):
        """A decorated function for setting the thruster values"""
        self.thrusters.set(values)


