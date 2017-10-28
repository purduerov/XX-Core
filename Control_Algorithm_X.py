from Control_Algorithm import ControlAlgorithm

class ControlAlgorithmX(ControlAlgorithm):

    activated = False



    def __init__(self):
        super(ControlAlgorithmX, self).__init__()

    def calculate(self,x,y,z,roll,pitch,yaw,lock_x,lock_y,lock_z):
        if not self.activated:
            return x
        else:
            if lock_x:




    def activate(self):
        super(ControlAlgorithmX, self).activate()

    def deactivate(self):
        super(ControlAlgorithmX, self).deactivate()