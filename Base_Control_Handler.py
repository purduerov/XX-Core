from abc import ABCMeta, abstractmethod

class BaseControlHandler(object):
    """ Abstract Base Class for the controlHandler."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def calculate(self, time_interval, user_input):
        pass

    @abstractmethod
    def activate_algorithm(self, algorithm):
        pass

    @abstractmethod
    def deactivate_algorithm(self, algorithm):
        pass

    @abstractmethod
    def prioritizeAlgorithm(self, algorithm):
        pass
