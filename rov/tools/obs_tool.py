
# NOTE: OBS TOOL ROTATES CLOCKWISE WITH POSITIVE POWER
#       Rotates quickly, increment slowly on order of 2% 


class OBS_Tool(object):
    def __init__(self, motor_control, pin):
        self.pin = pin
        self.motor_control = motor_control
        self._data = { 'power': 0.0 }

    def update(self, data):
        self._data = data
        self.motor_control.set(self.pin, self._data["power"])

    @property
    def data(self):
        return self._data


if __name__ == "__main__":
    from rov.hardware.motor_control import MotorControl
    from rov import init_hw_constants
    import sys

    motor_control = MotorControl()

    obs_tool = OBS_Tool(motor_control, init_hw_constants.OBS_TOOL_PIN)

    packet = { "power": 0.0 }

    obs_tool.update(packet)

    ch = sys.stdin.read(1)
    while (ch != '0'):
        packet = obs_tool.data
        if ch == '=':
            packet["power"] += 0.01
            obs_tool.update(packet)
        if ch == '-':
            packet["power"] -= 0.01
            obs_tool.update(packet)

        print (obs_tool.data)

        ch = sys.stdin.read(1)

    obs_tool.update({ "power": 0.0 })
