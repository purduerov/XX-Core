:rom rov.movement.controls.Control_Algorithm.py import ControlAlgorithm

class Master_Control_Handler():
    #figure out the activation logic
    #compare the activation logic

    def __init__(self, desired_thrust_in, frozen_in): #refer to the XX-Core/frontend/src/packets.js
        self.dof_control = desired_thrust_in
        self.dimension_lock = [False, False, False, False, False, False]
        self.dof_names = ['x', 'y', 'z', 'roll', 'pitch', 'yaw']
        self.freeze = [ControlAlgorithm('x'), ControlAlgorithm('y'), ControlAlgorithm('z'), ControlAlgorithm('roll'), ControlAlgorithm('pitch'), ControlAlgorithm('yaw')]
        self.prev_activate = [0, 0, 0, 0, 0, 0]


    def master(self, desired_thrust_in, frozen_in): # "main" control handler

        # axis freeze activation:
        # TODO: Tobi: simplify code to check prev_activate != frozen_in, then 'toggle' activation.

        for i in range(6):
            if(self.prev_activate[i] == False and frozen_in[i] == True): # check if it was previously frozen adn currently not
                self.freeze[i].activate(desired_thrust_in[i])
            else if (self.prev_activate[i] == True and frozen_in[i] == False): # check if it was previously not frozen and currently is
                self.freeze[i].deactivate()

        # Run the currently activated frozen axes:

        for i in range(6):
            if (frozen_in[i] == True): #if the dof is frozen - calculate the adjustment
                self.dof_control[i] = self.freeze[i].calculate(self.dof_names[i])[i]

        self.prev_activate = frozen_in
        return self.dof_control #returns the updated values
