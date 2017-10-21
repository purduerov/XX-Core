

class ControlAlgorithm():

    activated = False

    def __init__(self):
        pass

    def calculate(self,x,y,z,roll,pitch,yaw,lock_x,lock_y,lock_z):
        if not self.activated:
            return x
        else:
            if lock_x:


    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activate = False