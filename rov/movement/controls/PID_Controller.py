import numpy

class PID(object):
    """A generic PID loop controller which can be inherited and used in other control algorithms"""

    def __init__(self, startingError, p=1, i=0, d=0):
        """Return a instance of a un tuned PID controller"""
        self._p = p
        self._i = i
        self._d = d
        self._esum = 0              #Error sum for integral term
        self._le = startingError    #Last error value
        self._count = 0
        
    def calculate(self, error, dt):

        """Calculates the output of the PID controller"""
        self._esum += error*dt
        dError = (error - self._le)/dt
        u = self._p*error + self._i*self._esum + self._d *dError
        self._le = error
        return u


    def reset(self, startingError):
        """Resets the integral sum and the last error value"""
        self._esum = 0
        self._le = startingError

    def reset_esum(self):
        self._esum = 0

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
