from rov.movement.controls.Control_Algorithm.py import ControlAlgorithm

class Master_Control_Handler():
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
        self.prev_activate = [0, 0, 0, 0, 0, 0]




    def master(self, desired_thrust_in, frozen_in): # "main" control handler

        # axis freeze activation:
        # TODO: Tobi: simplify code to check prev_activate != frozen_in, then 'toggle' activation.
        # TODO: change to a for-loop!
        i = 0
        while(i < 6):
            if(self.prev_activate[i] == False and frozen_in[i] == True): #check if it was previously frozen and currently not
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
            else if (self.prev_activate[i] == True and frozen_in[i] == False): #check if it was previously not frozen and currently is
                if (i==0):
                    self.xfreeze.deactivate()
                if (i==1):
                    self.yfreeze.deactivate()
                if (i==2):
                    self.zfreeze.deactivate()
                if (i==3):
                    self.rollfreeze.deactivate()
                if (i==4):
                    self.pitchfreeze.deactivate()
                if (i==5):
                    self.yawfreeze.deactivate()
            i+=1

        # Run the currently activated frozen axes:
        # TODO: Tobi, change to a for loop..
        i = 0
        while (i < 6):
            if (frozen_in[i] == True): #if the dof is frozen - calculate the adjustment
                if (i==0):
                    self.dof_control[0] = self.xfreeze.calculate(self.dof_names[i])[i]
                if (i==1):
                    self.dof_control[1] = self.yfreeze.calculate(self.dof_names[i])[i]
                if (i==2):
                    self.dof_control[2] = self.zfreeze.calculate(self.dof_names[i])[i]
                if (i==3):
                    self.dof_control[3] = self.rollfreeze.calculate(self.dof_names[i])[i]
                if (i==4):
                    self.dof_control[4] = self.pitchfreeze.calculate(self.dof_names[i])[i]
                if (i==5):
                    self.dof_control[5] = self.yawfreeze.calculate(self.dof_names[i])[i]
            i += 1


        self.prev_activate = frozen_in
        return self.dof_control #returns the updated values
