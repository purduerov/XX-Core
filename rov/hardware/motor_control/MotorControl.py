from Adafruit_PCA9685 import PCA9685

"""
Using PCA9685 object:
  Functions
    set all pwm power with pwm.set_all_pwm(end_low, end_high)
    set pwm power with pwm.set_pwm(pin, end_low, end_high)

  PWM Values:
    To set PWM power % (-100% to 100%) w/ end_low and end_high: know that the
    values don't matter, just the difference between them. The zero power
    setting is 1.5ms high out of a 20ms period (50 Hz). The max documented
    range for these M200 motors is 1.1ms to 1.9ms high.  The values we can use
    in this function lets us specify values between 0 and 4096, which are what
    we enter in end_low and end_high. So to get 1.5ms high in a 20ms period, we
    set end_low=0 and end_high=310, for 4096 units out of 20ms, 4096/20 = 204.8
    units/ms. If we want diff for 1.5ms, we set 204 units/ms * 1.5ms = 307
    units. This is the theoretical difference we need, however under
    experimentation using logic analyzers, to achieve real 1.5 ms the
    difference should really be 310. So to set this 0% power, we can call
    pwm.set_pwm(0, 0, 310) or pwm.set_pwm(0, 1024, 1334), there should be no
    physical difference. For best practice, we should always start at 0.
"""


class MotorControl(object):

    def __init__(self, zero_power, neg_max_power, pos_max_power, frequency=50):
        self.ZERO_POWER = zero_power
        self.NEG_MAX_POWER = neg_max_power
        self.POS_MAX_POWER = pos_max_power

        self.pwm = PCA9685()
        self.pwm.set_pwm_freq(frequency)

        # By default, set everything to off
        self.pwm.set_all_pwm(0, self.ZERO_POWER)


    # PUBLIC FUNCTION
    def set(self, pin, value):
        if pin < 0 or pin > 15:
            raise Exception("Pin %d does not exist" % pin)

        if value < -1.0 or value > 1.0:
            raise Exception("Value %f is out of range" % value)

        pwm_val = self._toPWM(value)
        self.pwm.set_pwm(pin, 0, pwm_val)


    # PUBLIC FUNCTION
    def kill(self):
        self.pwm.set_all_pwm(0, self.ZERO_POWER)

    def _toPWM(self, val):
        if val > 1.0:
            return self.POS_MAX_POWER
        elif val < -1.0:
            return self.NEG_MAX_POWER
        else:
            return self._range_map(val, -1.0, 1.0, self.NEG_MAX_POWER, self.POS_MAX_POWER)

    def _range_map(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return int(round(rightMin + (valueScaled * rightSpan)))
