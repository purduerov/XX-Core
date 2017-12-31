from rov.movement.controls.Control_Algorithm.py import ControlAlgorithm

class Master_Control_Handler():
    #global variables
    prev_activate = [0, 0, 0, 0, 0, 0]
    
    #figure out the activation logic
    #compare the activation logic

    def __init__(self, desired_thrust_in, frozen_in): #refer to the XX-Core/frontend/src/packets.js
        self.desired_thrust_in = desired_thrust_in
        self.frozen_in = frozen_in
        self.dof_control = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.dimension_lock = [False, False, False, False, False, False]
        self.dof_names = ['x', 'y', 'z', 'roll', 'pitch', 'yaw']
        self.xfreeze = ControlAlgorithm('x')
        self.yfreeze = ControlAlgorithm('y')
        self.zfreeze = ControlAlgorithm('z')
        self.rollfreeze = ControlAlgorithm('roll')
        self.pitchfreeze = ControlAlgorithm('pitch')
        self.yawfreeze = ControlAlgorithm('yaw')



    def master(self): # sort of "main" function
        
        #TODO: the activation
        #if prev_activate[i] = 1 and current is 0 then we gotta deactivate it
        
        
        
        i = 0
        while (i < 6):
            if (self.frozen_in[i] == True):
                if (i==0):
                    self.dof_control[0] = self.xfreeze
                if (i==1):
                    self.dof_control[1] = self.yfreeze
                if (i==2):
                    self.dof_control[2] = self.zfreeze
                if (i==3):
                    self.dof_control[3] = self.rollfreeze
                if (i==4):
                    self.dof_control[4] = self.pitchfreeze
                if (i==5):
                    self.dof_control[5] = self.yawfreeze
            i++
