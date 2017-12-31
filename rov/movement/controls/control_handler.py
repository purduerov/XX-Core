from rov.movement.controls.Control_Algorithm.py import ControlAlgorithm

class Master_Control_Handler():
    #global variables
    prev_activate = [0, 0, 0, 0, 0, 0]

    def __init__(self, desired_thrust_in, frozen_in): #refer to the XX-Core/frontend/src/packets.js
        self.desired_thrust_in = desired_thrust_in
        self.frozen_in = frozen_in
        self.dof_control = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.dimension_lock = [False, False, False, False, False, False]
        self.dof_names = ['x', 'y', 'z', 'roll', 'pitch', 'yaw']
        self.xfreeze = ControlAlgorithm('x')



    def master(self): # sort of "main" function
        i = 0
        while (i < 6):
            if (self.frozen_in[i] == True):
                if (i==0):
                    


            i++
