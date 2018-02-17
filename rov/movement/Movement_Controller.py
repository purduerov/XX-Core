from controller_constants import *
from hardware.Thrusters_PWM_Control import Thrusters
from mapper.Simple import Mapper
#from controls.Force_Limiter import ForceLimiter
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

        #self.limiter = ForceLimiter()

        self.algorithm_handler = Master_Algorithm_Handler(self.df['thrusters']['frozen'], self.dc['sensors'])
        self.algorithm_handler.tune(PID_P, PID_I, PID_D)

    def update(self):

        # TODO: Add Fail Safe to prevent thrusters from locking at power when data stream is stopped (check for time since last packet update)

        # TODO: Add thrust limiter when complete
        # 1. thrust limiter:
        #self.limiter.enforce(self.df['thrusters']['desired_thrust'], self.thrusters.get(), self.df['thrusters']['disabled_thrusters'])

        # 2. Master Algorithm Handler
        self.algorithm_handler.master(self.df['thrusters']['desired_thrust'], self.df['thrusters']['frozen'])

        # 3. Thrust Mapper
        thruster_values = self.thrust_mapper.calculate(self.df['thrusters']['desired_thrust'], self.df['thrusters']['disabled_thrusters'])

        # 4. Push to Thrusters
        self.thrusters.set(thruster_values)

        # 5. Update dearclient reported thruster values:
        self.dc["thrusters"] = self.get_thruster_values()

    def stop_thrusters(self):
        self.thrusters.stop()

    def get_thruster_values(self):
        """The value of each thruster returned as a list"""
        return self.thrusters.get()

    def set_thruster_values(self, values):
        """A decorated function for setting the thruster values"""
        self.thrusters.set(values)



if __name__ == "__main__":

    from rov.hardware.motor_control import MotorControl
    from rov.init_hw_constants import *

    dearflask = {
            "thrusters": {
                "desired_thrust": [1, 0, 0, 0, 0, 0],
                "disabled_thrusters": [0,0,0,0,0,0,0,0],
                "frozen" : [0,0,0,0,0,0],
                "thruster_scales": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
            },
            "valve_turner": {
                "power": 0.0
            },
            "claw": {
                "power": 0.0
            },
            "fountain_tool": {
                "power": 0.0
            },
            "cameras": [
                { "port": 8080, "status": 1 },
                { "port": 8081, "status": 0 },
                { "port": 8082, "status": 1 },
                { "port": 8083, "status": 0 },
                { "port": 8084, "status": 1 },
                { "port": 8085, "status": 1 },
            ]
        }

    dearclient = {
            "sensors" : {
                'imu' : {
                    'linear-acceleration' :
                    {
                        'x' : 1,
                        'y' : 1
                    },
                    'euler' :
                    {
                        'roll': 1,
                        'pitch': 1,
                        'yaw': 1
                    }
                },
                'pressure' : {
                    'pressure': 1
                }
            }
        }

    motors = MotorControl(ZERO_POWER, NEG_MAX_POWER, POS_MAX_POWER, FREQUENCY)

    controller = Movement_Controller(dearflask, dearclient, motors)

    controller.update()

    print "dearflask" + str(dearflask)
    print "dearclient" + str(dearclient)
