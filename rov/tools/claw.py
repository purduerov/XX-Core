class Claw(object):
    def __init__(self, motor_control, pin):
        self.pin = pin
        self.motor_control = motor_control

    def update(self, power):
        self.motor_control.set(self.pin, power)
