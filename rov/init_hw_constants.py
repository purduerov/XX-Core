# Motor Controller class initialization constants
ZERO_POWER = 309  # Value to set thrusters to 0 power
NEG_MAX_POWER = 226  # Value to set thrusters to max negative power
POS_MAX_POWER = 391  # Value to set thrusters to max positive power
FREQUENCY = 49.5  # Frequency at which the i2c to pwm will be updated
POWER_THRESH = 120 # Power threshold for each individual thruster in Watts

# Tool Pin Placements
CLAW_PIN = 15
OBS_PIN = 14
TRANSMITTER_PIN = 10
