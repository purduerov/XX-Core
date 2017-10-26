from abc import ABCMeta, abstractmethod


class BaseThrusters(object):
    """ Abstract Base Class for hardware thrusters. It should implement a set
    and immediate stop method.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def set(self, values):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def stop(self):
        pass
