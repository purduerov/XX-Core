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

# Meanings of frozen_in input
# 0 - no control
# 1 - position
# 2 - speed
# 3 - height

class Master_Algorithm_Handler():
    # COMPARE THE ACTIVATION LOGIC
    def __init__(self, activate, sensors): # refer to the XX-Core/frontend/src/packets.js
        self._dof_control = [0,0,0,0,0,0] # HOLDS THE OUTPUT FOR MOVEMENT
        self._dof_names = ['x', 'y', 'z', 'roll', 'pitch', 'yaw']
        self._freeze = [] # CONTAINS THE POSITION STABILIZERS
        self._movement = [] # CONTAINS THE MOVEMENT STABILIZERS
        self._freeze_height = HeightStabilizer(sensors)
        self._prev_activate = activate # USED TO SEE IF FREEZE IS TOGGLED

        for i in range(6):
            # ACTIVATES IF IT SHOULD BE USED
            self._freeze.append(PositionStabilizer(i, sensors))
            self._movement.append(SpeedStabilizer(i, sensors))
            # ACTIVATES IT IF IT SHOULD BE USED
            if activate[i]:
                if i == 2 and activate[i] == 3:
                    self._freeze_height.activate()
                elif activate[i] == 1:
                    self._freeze[i].activate()
                elif activate[i] == 2:
                    self._movement[i].activate()

    def set_max_speed(value):
        for alg in self._movement:
            alg.set_max_speed(value)

    def master(self, desired_thrust_in, activate): # "MAIN" CONTROL HANDLER
        for i in range(6):
            # CHECK IF FROZEN WAS TOGGLED TO TOGGLE CONTROLS
            if ((activate[i] == 2) != (self._prev_activate[i] == 2)):
                self._movement[i].toggle()
            if ((activate[i] == 1) != (self._prev_activate[i] == 1)):
                self._freeze[i].toggle()
            if i == 2 and ((activate[i] == 3) != (self._prev_activate[i] == 3)):
                self._freeze_height.toggle()

        # ONLY CALCULATES ROLL, PITCH AND YAW
        for i in range(6):
            if activate[i] == 1:
                self._dof_control[i] = self._freeze[i].calculate()[i]
            elif activate[i] == 2:
                self._dof_control[i] = self._movement[i].calculate(desired_thrust_in[i])[i]
            elif activate[i] == 1:
                self._dof_control[i] = self._freeze[i].calculate()[i]
            elif activate[i] == 3 and i == 2:
                output = self._freeze_height.calculate()
                for j in range(3):
                    self._dof_control[j] += output[j]
            else:
                # SETS TO USER INPUT VALUE IF NOT FROZEN
                self._dof_control[i] = desired_thrust_in[i]

        for i in range(6):
            if self._dof_control[i] > 1:
                self._dof_control[i] = 1
            elif self._dof_control[i] < -1:
                self._dof_control[i] = -1

        self._prev_activate = activate
        return self._dof_control # RETURNS THE UPDATED VALUES

# -----------------------------------------------------
#                   GRAPHS DATA
# -----------------------------------------------------

    # USES MATPLOTLIB TO GRAPH ALGORITHM DATA
    def plot_data(self):
        count = 1
        for alg in self._freeze:
            if alg.has_data():
                plt.subplot(4, 4, count)
                plt.title('Freeze: ' + self._dof_names[alg._dof])
                plt.plot(alg.get_data()[0], alg.get_data()[1], 'r', alg.get_data()[0], alg.get_data()[2], 'b')
                count += 1

        for alg in self._movement:
            if alg.has_data():
                plt.subplot(4, 4, count)
                plt.title('Movement: ' + self._dof_names[alg._dof])
                plt.plot(alg.get_data()[0], alg.get_data()[1], 'r', alg.get_data()[0], alg.get_data()[2], 'b')
                count += 1

        if self._freeze_height.has_data():
            plt.subplot(4, 4, count)
            plt.title('Height Control')
            plt.plot(self._freeze_height.get_data()[0], self._freeze_height.get_data()[1], 'r', self._freeze_height.get_data()[0], self._freeze_height.get_data()[2], 'b')

        plt.show()
        plt.close()

    # ALLOWS TUNING OF THE PID VALUES WHEN TESTING
    # WILL PROBABLY NEED TO BE ABLE TO CHANGE EACH INDIVIDUAL DOF
    # BUT THIS WILL DO FOR NOW AND WILL BE QUICK TO CHANGE
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
                    'linear_acceleration' :
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
    master.master([1,0,0,0,0,0], [0,0,0,0,0,0])
    print(data)
