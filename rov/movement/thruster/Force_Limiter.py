from math import floor
import operator

class ForceLimiter(object):

    # TODO: convertToPowerUnit()

    def __init__(self):
        self.a6vector = [0 for _ in range(6)]
        self.an8vector = [0 for _ in range(8)]
        self.last8vector = [0 for _ in range(8)]

        self.mapper = Mapper()

    """
    1. acceptable_total_power
    2. acceptable_individual_total
    3. acceptable_total_change
    4. acceptable_individual_change
    """

    def convertToPowerUnit(self, an8vector):
        # equation: PWM vs Power = y = 0.00114535x^2-3.4372x+2579.273
        #for x in an8vector:
            #do something

        return 1


    # TODO: edit powerThresh constant, import thruster_power function function, edit else return value
    def acceptable_total_power(self):
        # tests the total power consumed

        POWER_THRESH = 1000

        totalPower = sum(convertToPowerUnit(self.an8vector))

        if totalPower < POWER_THRESH:
            return 1
        else:
            # TODO: JASON: Need function to calculate direction scalar from power scalar.
            return floor(POWER_THRESH/totalPower * 10) / 10

    # TODO: edit ind_thresh
    def acceptable_individual_total(self):
        # tests whether each individual thruster is exceeding the maximum
        # "Limiting"
        # should return 1 if everything is acceptable, otherwise a value \in (0,1) which will be multiplied to the 6vector

        IND_THRESH = 300

        maxComp = max(self.an8vector)

        if maxComp < IND_THRESH:
            return 1
        else:
            # TODO: JASON: Need function to calculate direction scalar from power scalar.
            return floor(IND_THRESH / maxComp * 10) / 10

    # TODO: edit total_change_thresh
    def acceptable_total_change(self, difference8):
        # tests whether the total "instantaneous" change in power consumed summed among all thrusters is within a threshold
        # should return 1 if everything is acceptable, otherwise a value \in (0,1) which will be multiplied to the 6vector

        TOTAL_CHANGE_THRESH = 1000

        sumChange = sum(difference8)

        if sumChange < TOTAL_CHANGE_THRESH:
            return 1
        else:
            # TODO: JASON: Need function to calculate direction scalar from power scalar.
            return floor(TOTAL_CHANGE_THRESH / sumChange * 10) / 10

    # TODO: edit ind_change_thresh
    def acceptable_individual_change(self, difference8):
        # tests whether the "instantaneous" change in the thruster value is acceptable for each individual thruster
        # "Ramping"
        # should return 1 if everything is acceptable, otherwise a value \in (0,1) which will be multiplied to the 6vector

        IND_CHANGE_THRESH = 1000

        # get greatest absolute value
        max_change = abs(max(min(difference8), max(difference8), key=abs))

        if max_change < IND_CHANGE_THRESH:
            return 1
        else:
            # TODO: JASON: Need function to calculate direction scalar from power scalar.
            return floor(IND_CHANGE_THRESH / max_change * 10) / 10

    def enforce(self, a6vector, last8vector, disabledT):

        self.a6vector = a6vector
        self.an8vector = mapper.calculate(a6vector, disabledT)
        self.last8vector = last8vector

        difference8 = map(operator.sub, self.an8vector, self.last8vector)

        total_power = self.acceptable_total_power()
        if total_power != 1:
            self.a6vector = total_power * self.a6vector

        ind_total_scale = self.acceptable_individual_total()
        if ind_total_scale != 1:
            self.a6vector = ind_total_scale * self.a6vector

        total_change = self.acceptable_total_change(difference8)
        if total_change != 1:
            self.a6vector = total_change * self.a6vector

        ind_change_scale = self.acceptable_individual_change(difference8)
        if ind_change_scale != 1:
            self.a6vector = ind_change_scale * self.a6vector

        return self.a6vector

