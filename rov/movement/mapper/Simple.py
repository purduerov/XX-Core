from BaseMapper import BaseMapper


class Mapper(BaseMapper):
    def __init__(self):
        self.NUM_THRUSTERS = 8

    def normalize(self, values):
        max_val = max([abs(x) for x in values])

        if max_val > 1.0:
            values = [x / max_val for x in values]

        return values

    def calculate(self, desired_thrust, disabled_thrusters=[]):
        # Calculate Thruster Values

        velX = desired_thrust[0]
        velY = desired_thrust[1]
        velZ = desired_thrust[2]

        # rotation about X
        roll = desired_thrust[3]

        # rotation about Y
        pitch = desired_thrust[4]

        # rotation about Z
        yaw = desired_thrust[5]

        horizontalThrusters = [0, 0, 0, 0]
        verticalThrusters = [0, 0, 0, 0]

        horizontalThrusters[0] += velX
        horizontalThrusters[1] += velX
        horizontalThrusters[2] -= velX
        horizontalThrusters[3] -= velX

        horizontalThrusters[0] += velY
        horizontalThrusters[1] -= velY
        horizontalThrusters[2] += velY
        horizontalThrusters[3] -= velY

        verticalThrusters[0] += velZ
        verticalThrusters[1] += velZ
        verticalThrusters[2] += velZ
        verticalThrusters[3] += velZ

        verticalThrusters[0] += pitch
        verticalThrusters[1] += pitch
        verticalThrusters[2] -= pitch
        verticalThrusters[3] -= pitch

        horizontalThrusters[0] -= yaw
        horizontalThrusters[1] += yaw
        horizontalThrusters[2] += yaw
        horizontalThrusters[3] -= yaw

        verticalThrusters[0] += roll
        verticalThrusters[1] -= roll
        verticalThrusters[2] += roll
        verticalThrusters[3] -= roll

        horizontalThrusters = self.normalize(horizontalThrusters)
        verticalThrusters = self.normalize(verticalThrusters)

        allThrusters = horizontalThrusters + verticalThrusters

        # disable thrusters not in use
        for t in set(disabled_thrusters):
            if 1 <= t <= self.NUM_THRUSTERS:
                allThrusters[t-1] = 0.0

        return allThrusters
