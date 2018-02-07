from Position_Stabilizer import PositionStabilizer
from Speed_Stabilizer import SpeedStabilizer
from Height_Stabilizer import HeightStabilizer
import matplotlib.pyplot as plt

# Algorithm_Handler
# -----------
#   README:
# -----------
#   This control handler takes in the users input and frozen dof's the create a new output for the thrusters
#   This is initialized with which variables should be frozen
#   This is updated with the desired thrust with 6 degrees and which variables should be frozen
#   This returns the new desired thrust for the thrust mapper and ramper
#   This is to allows the ROV to lock a certain position in the water if needed
# How to use:
#   1. handler = Master_Algorithm_Handler([0,0,1,0,0,0], sensors)
#   2. handler.master([0,0,0,0,0,0], [0,0,0,0,0,0])
#   -   This function returns the new thruster input ex: [0,1,0.4,-0.3,0]
#   -   Use handler.tune(3,2,1) to change the pid values

class Master_Algorithm_Handler():
    # compare the activation logic
    def __init__(self, frozen_in, sensors): #refer to the XX-Core/frontend/src/packets.js
        self._dof_control = [0,0,0,0,0,0] # holds the output for movement
        self._dof_names = ['x', 'y', 'z', 'roll', 'pitch', 'yaw'] 
        self._freeze = [] # contains the position stabilizers
        self._prev_activate = [0, 0, 0, 0, 0, 0] # used to see if freeze is toggled
        for i in range(6):
            self._freeze.append(PositionStabilizer(i, sensors)) 
            # activates if it should be used
            if frozen_in[i]:
                self._freeze[i].activate()
        # option to not used movement controls 
        self._movement_control = True
        self._movement = [] # contains the movement stabilizers 
        
        for i in range(6):
            self._movement.append(SpeedStabilizer(i, sensors))
            # activates it if it should be used
            if frozen_in[i] == False:
                self._movement[i].activate()

        self._freeze_height = HeightStabilizer(sensors)
    def set_max_speed(value):
        for alg in self._movement:
            alg.set_max_speed(value)

    def master(self, desired_thrust_in, frozen_in): # "main" control handler
        for i in range(6):
            # check if frozen was toggled to toggle algorithms
            if self._prev_activate[i] != frozen_in[i]:
                self._freeze[i].toggle()
                if i > 2:
                    self._movement[i].toggle()

        # only caluclates roll, pitch and yaw
        for i in range(6):
            if frozen_in[i] == True and i > 2:
                self._dof_control[i] = self._freeze[i].calculate()[i]
            elif frozen_in[i] == True and i == 2:
                output = self._freeze_height.calculate()
                for j in range(3):
                    self._dof_control[j] += output[j]
            else:
                if self._movement_control and i > 2:
                    self._dof_control[i] = self._movement[i].calculate(desired_thrust_in[i])[i]
                else:
                    # sets to user input value if not frozen
                    self._dof_control[i] = desired_thrust_in[i]

        for i in range(6):
            if self._dof_control[i] > 1:
                self._dof_control[i] = 1
            elif self._dof_control[i] < -1:
                self._dof_control[i] = -1

        self._prev_activate = frozen_in
        return self._dof_control # returns the updated values

# -----------------------------------------------------
#                   Graphs Data
# -----------------------------------------------------
   
    # uses matplotlib to graph algorithm data
    def plot_data(self):
        count = 1
        for alg in self._freeze:
            if alg.has_data():
                plt.subplot(4, 3, count)
                plt.title('Freeze: ' + self._dof_names[alg._dof])
                plt.plot(alg.get_graph_data()[0], alg.get_graph_data()[1], 'r', alg.get_graph_data()[0], alg.get_graph_data()[2], 'b')
                count += 1

        for alg in self._movement:
            if alg.has_data():
                plt.subplot(4, 3, count)
                plt.title('Movement: ' + self._dof_names[alg._dof])
                plt.plot(alg.get_graph_data()[0], alg.get_graph_data()[1], 'r', alg.get_graph_data()[0], alg.get_graph_data()[2], 'b')
                count += 1

        plt.show()
        plt.close()

    # allows tuning of the pid values when testing
    # will probably need to be able to change each individual dof
    # but this will do for now and will be quick to change
    def tune(self, p, i, d):
        for i in range(6):
            self._freeze[i].p = p
            self._freeze[i].i = i
            self._freeze[i].d = d

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
