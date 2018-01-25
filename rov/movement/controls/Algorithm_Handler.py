from Control_Algorithm import ControlAlgorithm

# Algorithm_Handler
# README:
#   This control handler takes in the users input and frozen dof's the create a new output for the thrusters
#   This is initialized with which variables should be frozen
#   This is updated with the desired thrust with 6 degrees and which variables should be frozen
#   This returns the new desired thrust for the thrust mapper and ramper
#   This is to allows the ROV to lock a certain position in the water if needed
# How to use:
#   1. handler = Master_Algorithm_Handler([0,0,1,0,0,0], sensors)
#   2. handler.master()
#   -   This function returns the new thruster input ex: [0,1,0.4,-0.3,0]
#   -   Use handler.tune(3,2,1) to change the pid values

class Master_Algorithm_Handler():
    # figure out the activation logic
    # compare the activation logic
    def __init__(self, frozen_in, sensors): #refer to the XX-Core/frontend/src/packets.js
        #dont think this is needed because it directly go inst o the control algorithms
        #self.sensors = sensors
        self.dof_control = [0,0,0,0,0,0]
        # not sure where this is used or if needed
        # self.dimension_lock = [False, False, False, False, False, False]
        self.dof_names = ['x', 'y', 'z', 'roll', 'pitch', 'yaw']
        self.freeze = [ControlAlgorithm('x', sensors), ControlAlgorithm('y', sensors), ControlAlgorithm('z', sensors), ControlAlgorithm('roll', sensors), ControlAlgorithm('pitch', sensors), ControlAlgorithm('yaw', sensors)]
        self.prev_activate = [0, 0, 0, 0, 0, 0]
        for i in range(6):
            if frozen_in[i]:
                freeze[i].activate()

    def master(self, desired_thrust_in, frozen_in): # "main" control handler

        # axis freeze activation:
        for i in range(6):
            # check if frozen control was toggled
            if self.prev_activate[i] != frozen_in[i]:
                self.freeze[i].toggle()

        # Run the currently activated frozen axes
        for i in range(6):
            # if the dof is frozen - calculate the adjustment
            if frozen_in[i] == True:
                self.dof_control[i] = self.freeze[i].calculate()[i]
            else:
                # sets to user input value if not frozen
                self.dof_control[i] = desired_thrust_in[i]

        self.prev_activate = frozen_in
        return self.dof_control #returns the updated values

    # allows tuning of the pid values when testing
    # will probably need to be able to change each individual dof
    # but this will do for now and will be quick to change
    def tune(self, p, i, d):
        for i in range(6):
            self.freeze[i].p = p
            self.freeze[i].i = i
            self.freeze[i].d = d

if __name__ == "__main__":
    data = {'sensors':
            {
                'imu' :
                {
                    'linear-acceleration' :
                    {
                        'x' : 1,
                        'y' : 1
                    },
                    'euler' :
                    {
                        'roll': 1,
                        'pitch': 1,
                        'yaw': 1
                    }
                },
                'pressure' :
                {
                    'pressure': 1
                }
            }
        }

    master = Master_Algorithm_Handler([0,0,0,0,0,0], data['sensors'])
    master.master([0,0,0,0,0,0], [True,True,True,True,True,True])
    print(data)

