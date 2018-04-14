

class ESC(object):

    def __init__(self):
        self.currents = [0.5, 0.3]
        self.temperatures = [25, 20]

    def update(self):
        pass

    @property
    def data(self):
        return {
            'currents': self.currents,
            'temperatures': self.temperatures
        }
