#todo: learn to use PID Controller
from rov.controls.PID_Controller import PID

class ControlAlgorithm():


    def __init__(self):
        self.activated = True
        self.controls = ['x','y','z','roll','pitch','yaw']

    #Allows option to activate
    def activate(self):
        self.activated = True

    #Allows option to deactivate
    def deactivate(self):
        self.activated = False

    def calculate(self, user_input, dimension_locks, activated_controls, sensor_values):
        if self.activated:

            #iterates through the same algorithm for each degree of freedom
            for dof in self.controls:

                #checks if allowed to alter dof value input otherwise skips
                if activated_controls[dof]:

                    #checks if user wants to lock position
                    if dimension_locks[dof]:
                        #todo: implement position locking algorithm
                        #todo: should set new value for user_input[dof]
                        #todo: implement PID controller
                        pass

                    #allows rov to travel smoothly
                    else:
                        #todo: make rov movement better
                        #todo: should set new value for user_input[dof]
                        #todo: implement PID controller
                        pass

        return user_input



