class ThrustLimiter(object):

    def __init__(self):
        self.speed = [0 for _ in range(6)]

    def ramp(self, curr_thrust_values, desired_thrust_values, power_cap):

        sum_difference = 0

        # for loop-- input difference between desired and curr thrust values
        for i in range(6):
            self.speed[i] = abs(desired_thrust_values[i] - curr_thrust_values[i])
            sum_difference += self.speed[i]

        # if the power required exceeds available power
        if sum_difference > power_cap:

            # scale the values by certain percentage so it's under the power cap
            power_scale = power_cap / sum_difference

            for i in range(6):
                self.speed[i] = self.speed[i] * power_scale

        # return the new speed by reference
        return self.speed