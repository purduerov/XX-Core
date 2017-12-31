class Master_Control_Handler():
    #global variables
    prev_activate = [0, 0, 0, 0, 0, 0]

    def __init__(self, thrusters, sensor_ref):
        self.dof_control = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.dimension_lock = [False, False, False, False, False, False]
