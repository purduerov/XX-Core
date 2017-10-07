from controller_constants import *
from hardware.PWM_Control import Thrusters
from mapper.Simple import Mapper

class controller(object):
    def __init__(self, motor_control):

        self.motor_control = motor_control

        self.thrusters = Thrusters(
            self.motor_control,
            LIST_OF_THRUSTER
        )

        self.thrust_mapper = Mapper()

    def update(self, user_input):
        pass