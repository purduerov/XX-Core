class ThrustLimiter(object):

    def __init__(self):
        self.speed = [0 for _ in range(8)]
        self.MAX_RAMP = 0.5
        self.DEFAULT_RAMP_VAL = 0.01

        # self.ramp_by = [0 for _ in range(8)]
        # self.desired_speed = [0 for _ in range(8)]

    # assuming 0 < inc_ramp_by <= 1
    def ramp(self, thrusters, ramp_scale):

        ramp_by = self.MAX_RAMP * ramp_scale

        # for loop-- input curr speed into self.speed

        if ramp_by == 0:
            ramp_by = self.DEFAULT_RAMP_VAL      # default ramping value

        # enumerate range and value together
        for i, value in enumerate(thrusters):

            # if the desired speed and current speed's difference is more than 0.01
            if abs(self.speed[i] - value) > ramp_by:

                # when desired speed > 0
                if self.speed[i] - value < 0:
                    self.speed[i] += ramp_by

                # when desired speed < 0
                elif self.speed[i] - value > 0:
                    self.speed[i] -= ramp_by

            # if the difference is <0.01, input the incoming speed directly to the thruster
            else:
                self.speed[i] = value

            # update the current speed
            # ThrustLimiter.speed_before[i] = ThrustLimiter.speed_updated[i]

        # return the new speed
        return self.speed       # passes by reference


        """
        percentage = 0.1    # percentage incremented by

        if thruster != self.desired_speed:
            self.desired_speed = thruster
            for i, value in enumerate(self.desired_speed):
                self.ramp_by[i] = (value - self.speed[i]) * percentage

        if self.speed != self.desired_speed:
            for i, r_by in enumerate(self.ramp_by):
                self.speed[i] = round((self.speed[i] + r_by), 2)
        """
