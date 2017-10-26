from BaseThrusters import BaseThrusters


class Thrusters(BaseThrusters):

    def __init__(self, motor_control, pin_layout):
        self.motor_control = motor_control
        self.pin_layout = pin_layout
        self.num_thrusters = len(pin_layout)

        self.__thruster_values = []

    def get(self):
        """Returns the values of each thruster as a list [first half horizontal, second half vertical]"""
        return self.__thruster_values

    def set(self, values):
        for i in range(self.num_thrusters):
            self.motor_control.set(self.pin_layout[i], values[i])

        self.__thruster_values = values

    def stop(self):
        values = [0 for _ in range(self.num_thrusters)]
        self.set(values)
