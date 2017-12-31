from rov.movement.controls.Control_Algorithm.py import ControlAlgorithm

class Master_Control_Handler():
    #global variables
    prev_activate = [0, 0, 0, 0, 0, 0]
    
    #figure out the activation logic
    #compare the activation logic

    def __init__(self, desired_thrust_in, frozen_in): #refer to the XX-Core/frontend/src/packets.js
        self.dof_control = desired_thrust_in
        self.dimension_lock = [False, False, False, False, False, False]
        self.dof_names = ['x', 'y', 'z', 'roll', 'pitch', 'yaw']
        self.xfreeze = ControlAlgorithm('x')
        self.yfreeze = ControlAlgorithm('y')
        self.zfreeze = ControlAlgorithm('z')
        self.rollfreeze = ControlAlgorithm('roll')
        self.pitchfreeze = ControlAlgorithm('pitch')
        self.yawfreeze = ControlAlgorithm('yaw')



    def master(self, desired_thrust_in, frozen_in): # "main" control handler
        
        #TODO: the activation
        #if prev_activate[i] = 1 and current is 0 then we gotta deactivate it
        i = 0
        while(i < 6):
            if(prev_activate[i] == False and frozen_in[i] == True):
                if (i==0):
                    self.xfreeze.activate(desired_thrust_in[i])
                if (i==1):
                    self.yfreeze.activate(desired_thrust_in[i])
                if (i==2):
                    self.zfreeze.activate(desired_thrust_in[i])
                if (i==3):
                    self.rollfreeze.activate(desired_thrust_in[i])
                if (i==4):
                    self.pitchfreeze.activate(desired_thrust_in[i])
                if (i==5):
                    self.yawfreeze.activate(desired_thrust_in[i])
            else if (prev_activate[i] == True and frozen_in[i] == False):
                if (i==0):
                    self.xfreeze.deactivate
                if (i==1):
                    self.yfreeze.deactivate
                if (i==2):
                    self.zfreeze.deactivate
                if (i==3):
                    self.rollfreeze.deactivate
                if (i==4):
                    self.pitchfreeze.deactivate
                if (i==5):
                    self.yawfreeze.deactivate
            i+=1
 
        i = 0
        while (i < 6):
            if (frozen_in[i] == True):
                if (i==0):
                    self.dof_control[0] = self.xfreeze.calculate
                if (i==1):
                    self.dof_control[1] = self.yfreeze.calculate
                if (i==2):
                    self.dof_control[2] = self.zfreeze.calculate
                if (i==3):
                    self.dof_control[3] = self.rollfreeze.calculate
                if (i==4):
                    self.dof_control[4] = self.pitchfreeze.calculate
                if (i==5):
                    self.dof_control[5] = self.yawfreeze.calculate
            i += 1
            
            
        prev_activate = frozen_in
