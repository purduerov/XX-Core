# Motor Controller class initialization constants
ZERO_POWER = 305  # Value to set thrusters to 0 power
NEG_MAX_POWER = 222  # Value to set thrusters to max negative power
POS_MAX_POWER = 388  # Value to set thrusters to max positive power
FREQUENCY = 47  # Frequency at which the i2c to pwm will be updated
POWER_THRESH = 1000 # arbitrary power threshold value
IND_THRESH = 300 # arbitrary individual thruster threshold value
TOTAL_CHANGE_THRESH = 1000 # arbitrary total change in thrusters threshold value
IND_CHANGE_THRESH = 1000 # arbitrary individual change in a thruster threshold value