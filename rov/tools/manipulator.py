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
