class Elecmagnet(object):
    def __init__(self, motor_control, pin,onpower=0.1):
        self.pin = pin
        self.motor_control = motor_control
        self.power = onpower

    def update(self, state):
        if state:
                self.motor_control.set(self.pin, self.power)
        else:
                self.motor_control.set(self.pin, 0)
