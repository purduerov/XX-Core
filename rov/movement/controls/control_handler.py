from Control_Algorithm import ControlAlgorithm

class Master_Control_Handler():
    #figure out the activation logic
    #compare the activation logic

    # TODO: What is the point of requiring frozen_in if you don't ever set it to anything here?
    # TODO: If you dont' think frozen_in is required, is desired_thrust_in? Or does it have to be set when object is created?
    def __init__(self, desired_thrust_in, frozen_in, sensors): #refer to the XX-Core/frontend/src/packets.js
        self.sensors = sensors
        self.dof_control = desired_thrust_in
        self.dimension_lock = [False, False, False, False, False, False]
        self.dof_names = ['x', 'y', 'z', 'roll', 'pitch', 'yaw']
        self.freeze = [ControlAlgorithm('x', sensors['imu']), ControlAlgorithm('y', sensors['imu']), ControlAlgorithm('z', sensors['pressure']), ControlAlgorithm('roll', sensors['imu']), ControlAlgorithm('pitch', sensors['imu']), ControlAlgorithm('yaw', sensors['imu'])]
        self.prev_activate = [0, 0, 0, 0, 0, 0]


    def master(self, desired_thrust_in, frozen_in): # "main" control handler

        # axis freeze activation:

        for i in range(6):
	    # check if it was previously frozen and currently not
            if(self.prev_activate[i] == False and frozen_in[i] == True):
                self.freeze[i].activate()
	    # check if it was previously not frozen and currently is
            elif (self.prev_activate[i] == True and frozen_in[i] == False):
                self.freeze[i].deactivate()

        # Run the currently activated frozen axes:

        for i in range(6):
            if (frozen_in[i] == True): #if the dof is frozen - calculate the adjustment
                self.dof_control[i] = self.freeze[i].calculate()[i]

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

    master = Master_Control_Handler([0,0,0,0,0,0], [0,0,0,0,0,0], data['sensors'])
    master.master([0,0,0,0,0,0], [True,True,True,True,True,True])
    print(data)

