from math import floor
import operator

class ForceLimiter(object):

    # TODO: convertToPowerUnit()

    def __init__(self):
        self.force_direction = [0 for _ in range(6)]
        self.thruster_powers = [0 for _ in range(8)]
        self.prev_thruster_powers = [0 for _ in range(8)]

        self.mapper = Mapper()

    """
    Order of Limiting Functions
    1. acceptable_total_power
    2. acceptable_individual_total
    3. acceptable_total_change
    4. acceptable_individual_change
    """

    def convertToPowerUnit(self, thruster_powers):
        # equation: PWM vs Power = y = 0.00114535x^2-3.4372x+2579.273
        #for x in thruster_powers:
            #do something

        return 1


    # TODO: edit powerThresh constant, import thruster_power function function, edit else return value
    def acceptable_total_power(self):
        # tests the total power consumed

        POWER_THRESH = 1000

        totalPower = sum(convertToPowerUnit(self.thruster_powers))

        if totalPower < POWER_THRESH:
            return 1
        else:
            # TODO: JASON: Need function to calculate direction scalar from power scalar.
            return floor(POWER_THRESH/totalPower * 10) / 10

    # TODO: edit ind_thresh
    def acceptable_individual_total(self):
        # tests whether each individual thruster is exceeding the maximum
        # "Limiting"
        # should return 1 if everything is acceptable, otherwise a value in (0,1) which will be multiplied to force_direction

        IND_THRESH = 300

        maxComp = max(self.thruster_powers)

        if maxComp < IND_THRESH:
            return 1
        else:
            # TODO: JASON: Need function to calculate direction scalar from power scalar.
            return floor(IND_THRESH / maxComp * 10) / 10

    # TODO: edit total_change_thresh
    def acceptable_total_change(self, diff_thruster_powers):
        # tests whether the total "instantaneous" change in power consumed summed among all thrusters is within a threshold
        # should return 1 if everything is acceptable, otherwise a value in (0,1) which will be multiplied to force_direction

        TOTAL_CHANGE_THRESH = 1000

        sumChange = sum(diff_thruster_powers)

        if sumChange < TOTAL_CHANGE_THRESH:
            return 1
        else:
            # TODO: JASON: Need function to calculate direction scalar from power scalar.
            return floor(TOTAL_CHANGE_THRESH / sumChange * 10) / 10

    # TODO: edit ind_change_thresh
    def acceptable_individual_change(self, diff_thruster_powers):
        # tests whether the "instantaneous" change in the thruster value is acceptable for each individual thruster
        # "Ramping"
        # should return 1 if everything is acceptable, otherwise a value in (0,1) which will be multiplied to force_direction

        IND_CHANGE_THRESH = 1000

        # get the greatest absolute value
        max_change = abs(max(min(diff_thruster_powers), max(diff_thruster_powers), key=abs))

        if max_change < IND_CHANGE_THRESH:
            return 1
        else:
            # TODO: JASON: Need function to calculate direction scalar from power scalar.
            return floor(IND_CHANGE_THRESH / max_change * 10) / 10

    def enforce(self, force_direction, prev_thruster_powers, disabledT):

        self.force_direction = force_direction
        self.thruster_powers = mapper.calculate(force_direction, disabledT)
        self.prev_thruster_powers = prev_thruster_powers

        diff_thruster_powers = map(operator.sub, self.thruster_powers, self.prev_thruster_powers)

        total_power = self.acceptable_total_power()
        if total_power != 1:
            self.force_direction = total_power * self.force_direction

        ind_total_scale = self.acceptable_individual_total()
        if ind_total_scale != 1:
            self.force_direction = ind_total_scale * self.force_direction

        total_change = self.acceptable_total_change(diff_thruster_powers)
        if total_change != 1:
            self.force_direction = total_change * self.force_direction

        ind_change_scale = self.acceptable_individual_change(diff_thruster_powers)
        if ind_change_scale != 1:
            self.force_direction = ind_change_scale * self.force_direction

        return self.force_direction

