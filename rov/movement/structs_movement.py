class thrusters_struct():
    def __init__(self, thruster_values):
        """Takes in an array of thruster values and returns a class that wraps all of the values in easy to read
                mnemonics and provides some very useful helper classes"""
        self.__all_thrusters = thruster_values


    def hor_front_left(self):
        return self.__all_thrusters[0]

    def hor_front_right(self):
        return self.__all_thrusters[1]

    def hor_back_left(self):
        return self.__all_thrusters[2]

    def hor_back_right(self):
        return self.__all_thrusters[3]

    def vert_front_left(self):
        return self.__all_thrusters[4]

    def vert_front_right(self):
        return self.__all_thrusters[5]

    def vert_back_left(self):
        return self.__all_thrusters[6]

    def vert_back_right(self):
        return self.__all_thrusters[7]

    def __iter__(self):
        """Allows for iterations over all of the thrusters"""
        return iter(self.__all_thrusters)

    def __sub__(self, other):
        """Subtracts the right thruster from the left thruster and returns a new thruster_struct class"""
        return thrusters_struct([a - b for a, b in zip(self.__all_thrusters, other.all_thrusters)])

    def __getitem__(self, index):
        """Allows array like lookups of the class so previous code will still work. Basically, you can
                still treat this class as a list and the code will still work"""
        return self.__all_thrusters[index]

    def get_vert_thruster_values(self):
        """Returns all of the vertical thrusters"""
        return self.__all_thrusters[4:8]

    def get_horr_thruster_valeus(self):
        """Returns all of the horizontal thrusters"""
        return self.__all_thrusters[0:4]

    def normalize(self):
        """Normalizes all thruster values so that the largest thruster value becomes 1 with
                all other thruster values scaled accordingly"""

        max_value = max([abs(x) for x in self.__all_thrusters])

        # Only normalize the thruster values if one of them is over 1.0
        if max_value > 1:
            self.__all_thrusters = [float(x) / max_value for x in self.__all_thrusters]

    def stop(self):
        """Turns all thruster values to zero"""
        self.__all_thrusters = [0 for _ in self.__all_thrusters]


if __name__ == "__main__":

    a = [1, 2, 3, 4, 5, 6, 7, 8]
    thrusters = thrusters_struct(a)
    thrusters2 = thrusters_struct([11, 12, 13, 14, 15, 16, 17, 18])

    print thrusters[0]
    a[0] = 9
    print thrusters[0]
    a = [8, 7, 6, 5, 4, ]



    """for thruster in thrusters:
        print thruster

    thrusters3 = thrusters2 - thrusters

    for thruster in thrusters3:
        print thruster

    print thrusters[7]

    for thruster in thrusters.get_horr_thruster_valeus():
        print "horr: " + str(thruster)

    for thruster in thrusters.get_vert_thruster_values():
        print "vert: " + str(thruster)

    thrusters.normalize()
    for thruster in thrusters:
        print thruster

    thrusters.stop()

    for thruster in thrusters:
        print thruster

    #thrusters4 = thrusters_struct([-2, -1, -0.5, 0, 0.5, 1, 0.5, 0])

    #thrusters4.normalize()

    #for thruster in thrusters4:
    #    print thruster"""