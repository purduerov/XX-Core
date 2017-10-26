"""
Tests the thrust mapper to verify that the thrust mapper
outputs thruster values that appear to be reasonable.
This class assumes that the ROV has 4 horizontal thrusters and 4
vertical thrusters. If this changes, some of the test cases might not
be applicable.
"""

import pytest
from rov.movement.mapper.Simple import Mapper

def test_zero_input_expect_zero_output():
    """Tests that the thrust mapper outputs all zeros when inputted with all zeros"""
    mapper = Mapper()

    input6Dof = [0, 0, 0, 0, 0, 0]
    mapped_output = mapper.calculate(input6Dof)

    for value in mapped_output:
        assert value == 0


def test_positive_x_input():
    """Tests that only horizontal thrusters are changed, and in the correct direction"""
    pass


def test_positive_y_input():
    """Tests that only horizontal thrusters are changed, and in the correct direction"""
    pass


def test_positive_z_input():
    """Tests that only vertical thrusters are changed, and in the correct direction"""
    pass


def test_positive_pitch_input():
    """Tests that only vertical thrusters are changed, and in the correct direction"""
    pass


def test_positive_roll_input():
    """Tests that only vertical thrusters are changed, and in the correct direction"""
    pass


def test_positive_yaw_input():
    """Tests that only horizontal thrusters are changed, and in the correct direction"""
    pass


def test_max_z_input_produces_max_vertical_thrusters():
    pass


def test_z_input_and_pitch_input():
    pass

