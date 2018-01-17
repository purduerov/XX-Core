from rov.movement.controls.Control_Algorithm.py import ControlAlgorithm

class Master_Control_Handler():
    #figure out the activation logic
    #compare the activation logic

    #TODO: add sensor as input to the contorl algorithms
    def __init__(self, desired_thrust_in, frozen_in): #refer to the XX-Core/frontend/src/packets.js
        self.dof_control = desired_thrust_in
        self.dimension_lock = [False, False, False, False, False, False]
        self.dof_names = ['x', 'y', 'z', 'roll', 'pitch', 'yaw']
        self.freeze = [ControlAlgorithm('x'), ControlAlgorithm('y'), ControlAlgorithm('z'), ControlAlgorithm('roll'), ControlAlgorithm('pitch'), ControlAlgorithm('yaw')]
        self.prev_activate = [0, 0, 0, 0, 0, 0]

    def master(self, desired_thrust_in, frozen_in): # "main" control handler
        # axis freeze activation:
        for i in range(6):
            # check if frozen control was toggled
            if self.prev_activate[i] != frozen_in[i]:
                self.freeze[i].toggle() 

        # Run the currently activated frozen axes:
        for i in range(6):
            # if the dof is frozen - calculate the adjustment
            if frozen_in[i] == True:
                self.dof_control[i] = self.freeze[i].calculate()[i]

        self.prev_activate = frozen_in
        return self.dof_control #returns the updated values
