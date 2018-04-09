from controller_constants import *
from hardware.Thrusters_PWM_Control import Thrusters
from mapper.Complex_1 import Complex
# from mapper.Simple import Mapper

class controller(object):
    def __init__(self, motor_control, dearflask, dearclient):

        self.motor_control = motor_control
        self.df = dearflask
        self.dc = dearclient

        self.thrusters = Thrusters(
            self.motor_control,
            LIST_OF_THRUSTER
        )

        self.thrust_mapper = Complex()

        self.algorithm_handler = Master_Algorithm_Handler(self.df["thrusters"]["frozen"], self.dc["sensors"])

        self.__thruster_values = {}

    def update(self, user_input):

        self.algorithm_handler.master(self.df["thrusters"]["desired_thrust"], self.df["thrusters"]["disabled_thrusters"])

        thruster_values = self.thrust_mapper.calculate(self.df["thrusters"]["desired_thrust"], self.df["thrusters"]["disableD_thrusters"])

        self.thrusters.set(thruster_values)

    def stop_thrusters(self):
        self.thrusters.stop()

    def get_thruster_values(self):
        """The value of each thruster returned as a list"""
        return self.thrusters.get()

    def set_thruster_values(self, values):
        """A decorated function for setting the thruster values"""
        self.thrusters.set(values)


