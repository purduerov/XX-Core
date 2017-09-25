import numpy


class PID(object):
    """A generic PID loop controller which can be inherited and used in other control algorithms"""

    def __init__(self):
        """Return a instance of a un tuned PID controller"""
        self._p = 1
        self._i = 0
        self._d = 0

        self._desired_pos = 0

    def calculate(self, time_intervale):
        """Calculates the output of the PID controller"""
        pass

    @property
    def desired_pos(self):
        return self._desired_pos

    @desired_pos.setter
    def desired_pos(self, value):
        self._desired_pos = value

    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, value):
        self._p = value

    @property
    def i(self):
        return self._i

    @i.setter
    def i(self, value):
        self._i = value

    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, value):
        self._d = value
