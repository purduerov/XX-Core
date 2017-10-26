class thrusters_struct():
    def __init__(self, thruster_values):
        self.horr_front_left = thruster_values[0]
        self.horr_front_right = thruster_values[1]
        self.horr_back_left = thruster_values[2]
        self.horr_back_right = thruster_values[3]
        self.vert_front_left = thruster_values[4]
        self.vert_front_right = thruster_values[5]
        self.vert_back_left = thruster_values[6]
        self.vert_back_right = thruster_values[7]

        self.__all_thrusters = thruster_values

    def __iter__(self):
        return iter(self.__all_thrusters)

    def __sub__(self, other):
        """Subtracts the right thruster from the left thruster and returns a new thruster_struct class"""
        return thrusters_struct([a - b for a, b in zip(self.__all_thrusters, other.all_thrusters)])

    def __getitem__(self, index):
        return self.__all_thrusters[index]

    def get_vert_thruster_values(self):
        return self.__all_thrusters[4:8]

    def get_horr_thruster_valeus(self):
        return self.__all_thrusters[0:4]

    def normalize(self):
        """Normalizes all thruster values so that the largest thruster value becomes 1 with
                all other thruster values scaled accordingly"""

        max_value = max(self.__all_thrusters)

        # Only normalize the thruster values if one of them is over 1.0
        if max_value > 1:
            self.__all_thrusters = [float(x) / max_value for x in self.__all_thrusters]

    def stop(self):
        """Turns all thruster values to zero"""
        self.__all_thrusters = [0 for _ in self.__all_thrusters]


if __name__ == "__main__":
    thrusters = thrusters_struct([1, 2, 3, 4, 5, 6, 7, 8])
    thrusters2 = thrusters_struct([11, 12, 13, 14, 15, 16, 17, 18])

    """for thruster in thrusters:
        print thruster

    thrusters3 = thrusters2 - thrusters

    for thruster in thrusters3:
        print thruster

    print thrusters[7]

    for thruster in thrusters.get_horr_thruster_valeus():
        print "horr: " + str(thruster)

    for thruster in thrusters.get_vert_thruster_values():
        print "vert: " + str(thruster)"""

    thrusters.normalize()
    for thruster in thrusters:
        print thruster

    thrusters.stop()

    for thruster in thrusters:
        print thruster