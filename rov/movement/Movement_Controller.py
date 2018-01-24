from controller_constants import *
from hardware.Thrusters_PWM_Control import Thrusters
from mapper.Simple import Mapper
from controls.Force_Limiter import ForceLimiter
from controls.Algorithm_Handler import Master_Algorithm_Handler

class Movement_Controller(object):
    def __init__(self, dearflask, dearclient, motor_control):

        self.motor_control = motor_control
        self.df = dearflask
        self.dc = dearclient

        self.thrusters = Thrusters(
            self.motor_control,
            LIST_OF_THRUSTER
        )

        self.thrust_mapper = Mapper()

        self.limiter = ForceLimiter()

        self.algorithm_handler = Master_Algorithm_Handler(self.df['thrusters']['frozen'], self.dc['sensors'])
        self.algorithm_handler.tune(PID_P, PID_I, PID_D)

    def update(self):

        # TODO: Add Fail Safe to prevent thrusters from locking at power when data stream is stopped (check for time since last packet update)

        # 1. thrust limiter:
        self.limiter.enforce(self.df['thrusters']['desired_thrust'], self.thrusters.get(), self.df['thrusters']['disabled_thrusters'])

        # 2. Master Algorithm Handler
        self.algorithm_handler.master(self.df['thrusters']['desired_thrust'], self.df['thrusters']['frozen'])

        # 3. Thrust Mapper
        thruster_values = self.thrust_mapper.calculate(self.df['thrusters']['desired_thrust'], self.df['thrusters']['disabled_thrusters'])

        # 4. Push to Thrusters
        self.thrusters.set(thruster_values)

    def stop_thrusters(self):
        self.thrusters.stop()

    def get_thruster_values(self):
        """The value of each thruster returned as a list"""
        return self.thrusters.get()

    def set_thruster_values(self, values):
        """A decorated function for setting the thruster values"""
        self.thrusters.set(values)


