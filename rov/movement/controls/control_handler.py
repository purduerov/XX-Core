from Control_Algorithm import ControlAlgorithm

class Master_Control_Handler():
    # figure out the activation logic
    # compare the activation logic
    
    # TODO: create a read me explaining this and showing how to use.
    def __init__(self, frozen_in, sensors): #refer to the XX-Core/frontend/src/packets.js
        #dont think this is needed because it directly go inst o the control algorithms
        #self.sensors = sensors
        self.dof_control = [0,0,0,0,0,0]
        self.dimension_lock = [False, False, False, False, False, False]
        self.dof_names = ['x', 'y', 'z', 'roll', 'pitch', 'yaw']
        self.freeze = [ControlAlgorithm('x', sensors['imu']), ControlAlgorithm('y', sensors['imu']), ControlAlgorithm('z', sensors['pressure']), ControlAlgorithm('roll', sensors['imu']), ControlAlgorithm('pitch', sensors['imu']), ControlAlgorithm('yaw', sensors['imu'])]
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

        # Run the currently activated frozen axes:

        for i in range(6):
            # if the dof is frozen - calculate the adjustment
            if frozen_in[i] == True:
                self.dof_control[i] = self.freeze[i].calculate()[i]
            else:
                # sets to user input value if not frozen
                self.dof_control[i] = desired_thrust_in[i]

        self.prev_activate = frozen_in
        return self.dof_control #returns the updated values
    
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

    master = Master_Control_Handler([0,0,0,0,0,0], data['sensors'])
    master.master([0,0,0,0,0,0], [True,True,True,True,True,True])
    print(data)

