from BaseThrusters import BaseThrusters


class Thrusters(BaseThrusters):

    def __init__(self, motor_control, pin_layout):
        self.motor_control = motor_control
        self.pin_layout = pin_layout
        self.num_thrusters = len(pin_layout)

    def set(self, values):
        for i in range(self.num_thrusters):
            self.motor_control.set(self.pin_layout[i], values[i])

    def stop(self):
        values = [0 for _ in range(self.num_thrusters)]
        self.set(values)
