

class ESC(object):

    def __init__(self):
        self.currents = []
        self.temperatures = []

    def update(self):
        pass

    @property
    def data(self):
        return {
            'currents': self.currents,
            'temperatures': self.temperatures
        }