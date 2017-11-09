from abc import ABCMeta, abstractmethod


class BaseMapper(object):
    """ Abstract Base Class for a thrust mapper. It should implement one method,
    calculate that takes in a desired thrust and a list of disabled thrusters.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def calculate(self, desired_thrust, disabled_thrusters=[]):
        pass
