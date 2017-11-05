from BaseMapper import BaseMapper
from rov.movement.structs_movement import thrusters_struct

class Mapper(BaseMapper):
    def __init__(self):
        self.NUM_THRUSTERS = 8

        # create an array that contains the values of all of the thrusters and preset the
        # values to 0
        self.allThrusters = [0 for _ in range(0, 8)]
        self.return_thrusters_struct = thrusters_struct(self.allThrusters)

    def normalize(self, values):
        max_val = max([abs(x) for x in values])

        if max_val > 1.0:
            values = [x / max_val for x in values]

        return values

    def calculate(self, desired_thrust, disabled_thrusters=[]):
        # Calculate Thruster Values=

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

        # set the thruster values to the new value. Assinging by index is a copy by reference
        # which is what we want for the return_thruster_struct variable
        self.allThrusters[0:8] = horizontalThrusters + verticalThrusters

        # disable thrusters not in use
        for t in set(disabled_thrusters):
            if 1 <= t <= self.NUM_THRUSTERS:
                self.allThrusters[t-1] = 0.0

        # normalize the thruster values which are going to be returned
        self.return_thrusters_struct.normalize()

        return self.return_thrusters_struct

        pass
