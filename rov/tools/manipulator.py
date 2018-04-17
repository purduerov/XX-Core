class Manipulator(object):
    def __init__(self, motor_control, pin):
        self.pin = pin
        self.motor_control = motor_control
        self.power = 0

    def update(self, power):
        self.motor_control.set(self.pin, power)
        self.power = power

    @property
    def data(self):
        return self.power


if __name__ == "__main__":
    from rov.hardware.motor_control import MotorControl
    from rov import init_hw_constants
    import sys

    motor_control = MotorControl()

    manipulator = Manipulator(motor_control, init_hw_constants.MANIPULATOR_PIN)

    manipulator.update(0.0)

    ch = sys.stdin.read(1)
    while (ch != '0'):
        if ch == '+':
            manipulator.update(manipulator.data + .1)
        if ch == '-':
            manipulator.update(manipulator.data - .1)

        print (manipulator.data)

        ch = sys.stdin.read(1)

    manipulator.update(0.0)
