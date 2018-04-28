# Motor Controller class initialization constants
ZERO_POWER = 305  # Value to set thrusters to 0 power
NEG_MAX_POWER = 222  # Value to set thrusters to max negative power
POS_MAX_POWER = 388  # Value to set thrusters to max positive power
FREQUENCY = 47  # Frequency at which the i2c to pwm will be updated
POWER_THRESH = 120 # Power threshold for each individual thruster in Watts


#-----------------------#
#       PID Values      #
#-----------------------#

# Position Algorithms
POSITION_PID_X = 1,0,0
POSITION_PID_Y = 1,0,0
POSITION_PID_Z = 1,0,0
POSITION_PID_ROLL = 1,0,0
POSITION_PID_PITCH = 1,0,0
POSITION_PID_YAW = 1,0,0

# Speed Algorithms
SPEED_PID_X = 1,0,0
SPEED_PID_Y = 1,0,0
SPEED_PID_Z = 1,0,0
SPEED_PID_ROLL = 1,0,0
SPEED_PID_PITCH = 1,0,0
SPEED_PID_YAW = 1,0,0

# Height Algorithm
HEIGHT_PID = 1,0,0
