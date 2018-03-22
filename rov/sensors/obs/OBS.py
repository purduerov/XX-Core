

class OBS(object):

    def __init__(self):
        self.x_tilt = 1
        self.y_tilt = 2
        self.z_tilt = 3
        self.time = [0, 0.5, 1, 0.5]
        self.amplitude = [1, 0.5, 0.34, 0.2, 0.6]

    def update(self):
        pass
    
    @property
    def data(self):
        return {
            'tilt': {
                'x': self.x_tilt,
                'y': self.y_tilt,
                'z': self.z_tilt
            },
            'seismograph_data': {
                'time': self.time,
                'amplitude': self.amplitude
            }
        }
