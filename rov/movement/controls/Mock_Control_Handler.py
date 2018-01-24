from BaseControlHandler import BaseControlHandler

import numpy

class ControlHandler(BaseControlHandler):

    def __init__(self,  algorithms_used, sensors):
        self.sensors = sensors
        self.algorithms = algorithms_used

    def calculate(self, time_interval, user_input):
        pass

    def activate_algorithm(self, algorithm):
        pass

    def deactivate_algorithm(self, algorithm):
        pass

    def prioritizeAlgorithm(self, algorithm):
        pass