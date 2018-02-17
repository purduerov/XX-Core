"""
Set of tests for checking the functionality of the controller class. These tests assume that there are 8 thrusters,
4 vertical and 4 horizontal.
"""

import pytest
from rov.movement.controller import *


@pytest.fixture()
def motor_controller():
    from rov.hardware.motor_control import MotorControl
    from rov.init_hw_constants import ZERO_POWER, NEG_MAX_POWER, POS_MAX_POWER, FREQUENCY

    return MotorControl(
        zero_power=ZERO_POWER,
        neg_max_power=NEG_MAX_POWER,
        pos_max_power=POS_MAX_POWER,
        frequency=FREQUENCY
    )


@pytest.fixture()
def set_z(z_value):
    return [0, 0, z_value, 0, 0, 0]


def test_expect_no_thruster_force_with_no_user_input():
    """Test that the thrusters have zero force when they are initialized"""
    controls = controller(motor_controller())

    # Simulate the user sending all zeros the controller
    all_zeros = [0 for _ in range(0, 8)]
    controls.update(all_zeros)

    # Get the thruster values that were stored in the thruster class
    thruster_values = controls.get_thruster_values()

    # Check that each value is equal to 0
    for value in thruster_values:
        assert value == 0


def test_turning_on_vertical_thrusters_to_go_up():
    """Test that the vertical thrusters all go up when given a positive z input"""
    controls = controller(motor_controller())

    # Simulate telling the rov to go up
    user_input = set_z(1)
    controls.update(user_input)

    # Get the thruster values that were stored in the thruster class
    thruster_values = controls.get_thruster_values()

    # Check that each value is equal to 0
    horizontal_thrusters = thruster_values[0:4]
    vertical_thrusters = thruster_values[4:8]

    for value in vertical_thrusters:
        assert value > 0


def test_expect_no_thruster_force_when_controller_is_stopped():
    """Test that the thruster forces are zero when the controller is given the stop command"""
    controls = controller(motor_controller())

    # Simulate the user a command that is non zero
    controls.update([1, 1, 1, 1, 1, 1, 1, 1])

    # Tell the thrusters to stop
    controls.stop_thrusters()

    # Get the thruster values that were stored in the thruster class
    thruster_values = controls.get_thruster_values()

    # Check that the thrusters have been stopped
    for value in thruster_values:
        assert value == 0
