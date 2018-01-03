from math import floor
import operator

class ForceLimiter(object):

    def __init__(self):
        self.a6vector = [0 for _ in range(6)]
        self.an8vector = [0 for _ in range(8)]
        self.last8vector = [0 for _ in range(8)]

    """
    1. acceptable_total_power
    2. acceptable_individual_total
    3. acceptable_total_change
    4. acceptable_individual_change
    """

    # TODO: an8vector hardcoded to 0 for now
    def calc8vector(self):
        # calculates and saves values for an8vector
        self.an8vector = [0 for _ in range(8)]

    # TODO: edit powerThresh constant, import thruster_power function function, edit else return value
    def acceptable_total_power(self):
        # tests the total power consumed

        power_thresh = 1000

        totalPower = sum(thruster_power(self.an8vector))

        if totalPower < power_thresh:
            return 1
        else:
            return 0.5

    # TODO: edit ind_thresh
    def acceptable_individual_total(self):
        # tests whether each individual thruster is exceeding the maximum
        # "Limiting"
        # should return 1 if everything is acceptable, otherwise a value \in (0,1) which will be multiplied to the 6vector

        ind_thresh = 300

        maxComp = max(self.an8vector)

        if maxComp < ind_thresh:
            return 1
        else:
            return floor(ind_thresh / maxComp * 10) / 10

    # TODO: edit total_change_thresh
    def acceptable_total_change(self, change):
        # tests whether the total "instantaneous" change in power consumed summed among all thrusters is within a threshold
        # should return 1 if everything is acceptable, otherwise a value \in (0,1) which will be multiplied to the 6vector

        total_change_thresh = 1000

        sumChange = sum(change)

        if sumChange < total_change_thresh:
            return 1
        else:
            return floor(total_change_thresh / sumChange * 10) / 10

    # TODO: edit ind_change_thresh
    def acceptable_individual_change(self, change):
        # tests whether the "instantaneous" change in the thruster value is acceptable for each individual thruster
        # "Ramping"
        # should return 1 if everything is acceptable, otherwise a value \in (0,1) which will be multiplied to the 6vector

        ind_change_thresh = 1000

        # get greatest absolute value
        max_change = abs(max(min(change), max(change), key=abs))

        if max_change < ind_change_thresh:
            return 1
        else:
            return floor(ind_change_thresh / max_change * 10) / 10

    def enforce(self):
        self.calc8vector()
        # last8vector = old8vector
        # change = an8vector - last8vector
        change = map(operator.sub, self.an8vector, self.last8vector)

        ind_total_scale = self.acceptable_individual_total()
        if ind_total_scale != 1:
            self.a6vector = ind_total_scale * self.a6vector

        ind_change_scale = self.acceptable_individual_change(change)
        if ind_change_scale != 1:
            self.a6vector = ind_change_scale * self.a6vector

        total_change = self.acceptable_total_change(change)
        if total_change != 1:
            self.a6vector = total_change * self.a6vector

        total_power = self.acceptable_total_power()
        if total_power != 1:
            self.a6vector = total_power * self.a6vector

        # update last8vector and an8vector
        self.last8vector = self.an8vector
        self.calc8vector()

        return self.a6vector

    # TODO: import runThrusters method
    def power(self):
        self.a6vector = self.enforce()

        runThrusters(self.an8vector)