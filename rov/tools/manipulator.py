
# NOTE: MANIPULATOR OPENS WITH POSITIVE POWER
#       10% - 15% Power to open and close


class Manipulator(object):
    def __init__(self, motor_control, pin):
        self.pin = pin
        self.motor_control = motor_control
        self._data = { "power": 0.0 }

    def update(self, data):
        self._data = data
        self.motor_control.set(self.pin, data["power"])

    @property
    def data(self):
        return self._data


if __name__ == "__main__":
    from rov.hardware.motor_control import MotorControl
    from rov import init_hw_constants
    import sys

    motor_control = MotorControl()

    manipulator = Manipulator(motor_control, init_hw_constants.MANIPULATOR_PIN)

    packet = { "power": 0.0 }

    manipulator.update(packet)

    ch = sys.stdin.read(1)
    while (ch != '0'):
        packet = manipulator.data
        if ch == '=':
            packet["power"] += 0.05
            manipulator.update(packet)
        if ch == '-':
            packet["power"] -= 0.05
            manipulator.update(packet)

        print (manipulator.data)

        ch = sys.stdin.read(1)

    packet["power"] = 0.0
    manipulator.update(packet)
