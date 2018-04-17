class OBS_Tool(object):
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

    obs_tool = OBS_Tool(motor_control, init_hw_constants.OBS_TOOL_PIN)

    obs_tool.update(0.0)

    ch = sys.stdin.read(1)
    while (ch != '0'):
        if ch == '+':
            obs_tool.update(obs_tool.data + .1)
        if ch == '-':
            obs_tool.update(obs_tool.data - .1)

        print (obs_tool.data)

        ch = sys.stdin.read(1)

    obs_tool.update(0.0)
