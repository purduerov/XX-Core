class Leveler(object):
    def __init__(self, motor_control, pin, power = 0.1):
        self.pin = pin
        self.motor_control = motor_control
        self.power = power

    def update(self, direction):
        if direction > 0:
                self.motor_control.set(self.pin, self.power)
        elif direction < 0:
                self.motor_control.set(self.pin, -self.power)
        else:
                self.motor_control.set(self.pin, 0)
