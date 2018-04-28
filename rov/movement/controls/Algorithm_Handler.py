from Position_Stabilizer import PositionStabilizer
from Speed_Stabilizer import SpeedStabilizer
from Height_Stabilizer import HeightStabilizer
from Visualization import Visualization
import matplotlib.pyplot as plt
import threading
import matplotlib.animation as animation
import time
from random import *

# from Tkinter import ttk

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
    def __init__(self, activate, sensors, launch_visual = True): # refer to the XX-Core/frontend/src/packets.js
        self._launch_visual = launch_visual
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

        if self._launch_visual:
            #self.launch()
            #thread.start_new_thread( self.launch, () )
            t = threading.Thread(target=self.launch)
            t.start()

    def update():
        self.app.update()

    def launch(self):
        self.app = Visualization(self)
        self.app.title("PID Visualization")
        ani = animation.FuncAnimation(self.app.f, self.app.animate, interval=500)

        #ani = animation.FuncAnimation(self.app.f, self.app.animate, interval=1000)
        self.app.mainloop()

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
    def get_data(self, alg_type, index):
        if alg_type == 1:
            alg = self._freeze[index]
        elif alg_type == 2:
            alg = self._movement[index]
        elif alg_type == 3:
            alg = self._freeze_height

        data = alg.get_data()
        return data

    def clear_data(self, alg):
        x = ( alg / 6 ) + 1
        y = alg - (6 * x) + 6

        if x == 1:
            self._freeze[y].clear_data()

        if x == 2:
            self._movement[y].clear_data()

        if x == 3:
            self._freeze_height.clear_data()

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
    def tune(self, alg, pid, value):
        x = ( alg / 6 ) + 1
        y = alg - (6 * x) + 6

        if x == 1:
            if pid == 0:
                self._freeze[y].set_p(value)
            if pid == 1:
                self._freeze[y].set_i(value)
            if pid == 2:
                self._freeze[y].set_d(value)

        if x == 2:
            if pid == 0:
                self._movement[y].set_p(value)
            if pid == 1:
                self._movement[y].set_i(value)
            if pid == 2:
                self._movement[y].set_d(value)

        if x == 3:
            if pid == 0:
                self._freeze_height.set_p(value)
            if pid == 1:
                self._freeze_height.set_i(value)
            if pid == 2:
                self._freeze_height.set_d(value)

    def get_pid(self, alg, pid):
        x = ( alg / 6 ) + 1
        y = alg - (6 * x) + 6

        if x == 1:
            if pid == 0:
                return self._freeze[y].get_p()
            if pid == 1:
                return self._freeze[y].get_i()
            if pid == 2:
                return self._freeze[y].get_d()

        if x == 2:
            if pid == 0:
                return self._movement[y].get_p()
            if pid == 1:
                return self._movement[y].get_i()
            if pid == 2:
                return self._movement[y].get_d()

        if x == 3:
            if pid == 0:
                return self._freeze_height.get_p()
            if pid == 1:
                return self._freeze_height.get_i()
            if pid == 2:
                return self._freeze_height.get_d()


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

    lt = time.time()

    def rand():
        return 1#(random() / 5.0) + 0.9

    def rand2():
        return random() * 0.001# - 0.0005

    def update_data(user_input, data, lt):
        dt = time.time() - lt
        lt = time.time()
        data['sensors']['imu']['linear-acceleration']['x'] += user_input[0] * dt * rand() + rand2() * dt
        data['sensors']['imu']['linear-acceleration']['y'] += user_input[1] * dt * rand() + rand2() * dt

        data['sensors']['pressure']['pressure'] += user_input[2] * dt * rand() + rand2() * dt

        data['sensors']['imu']['euler']['roll'] += user_input[3] * dt * rand() + rand2() * dt

        data['sensors']['imu']['euler']['pitch'] += user_input[4] * dt * rand() + rand2() * dt

        data['sensors']['imu']['euler']['yaw'] += user_input[5] * dt * rand() + rand2() * dt

        if data['sensors']['imu']['euler']['roll'] > 360:
            data['sensors']['imu']['euler']['roll'] -= 360
        elif data['sensors']['imu']['euler']['roll'] < 0:
            data['sensors']['imu']['euler']['roll'] += 360


    master = Master_Algorithm_Handler([0,0,0,0,0,0], data['sensors'])
    user_input = [0,0,0,0,0,0]
    frozen = [1,1,1,2,2,2]
    print(data)
    while True:
        update_data(master.master(user_input, frozen), data, lt)
        time.sleep(0.02)
