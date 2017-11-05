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

    input_6_dof = [0, 0, 0, 0, 0, 0]
    mapped_output = mapper.calculate(input_6_dof)

    for value in mapped_output:
        assert value == 0


def test_positive_x_input():
    """Tests that only horizontal thrusters are changed, and in the correct direction"""

    # create whichever thrust mapper we are testing
    mapper = Mapper()

    input_6_dof = [1, 0, 0, 0, 0, 0]
    mapped_output = mapper.calculate(input_6_dof)

    # test that the x direction send the rov forward
    assert (mapped_output.hor_front_left() > 0)
    assert (mapped_output.hor_front_right() > 0)
    assert (mapped_output.hor_back_left() < 0)
    assert (mapped_output.hor_back_right() < 0)

    # verify that the values have been normalized
    for value in mapped_output:
        assert (abs(value) <= 1)


def test_positive_y_input():
    """Tests that only horizontal thrusters are changed, and in the correct direction"""

    # create whichever thrust mapper we are testing
    mapper = Mapper()

    input_6_dof = [0, 1, 0, 0, 0, 0]
    mapped_output = mapper.calculate(input_6_dof)

    # test that the y direction send the rov forward
    assert (mapped_output.hor_front_left() > 0)
    assert (mapped_output.hor_front_right() < 0)
    assert (mapped_output.hor_back_left() > 0)
    assert (mapped_output.hor_back_right() < 0)

    # verify that the values have been normalized
    for value in mapped_output:
        assert (abs(value) <= 1)


def test_positive_z_input():
    """Tests that only vertical thrusters are changed, and in the correct direction"""

    # create whichever thrust mapper we are testing
    mapper = Mapper()

    input_6_dof = [0, 0, 1, 0, 0, 0]
    mapped_output = mapper.calculate(input_6_dof)

    # test that the y direction send the rov forward
    assert (mapped_output.vert_front_left() > 0)
    assert (mapped_output.vert_front_right() > 0)
    assert (mapped_output.vert_back_left() > 0)
    assert (mapped_output.vert_back_right() > 0)

    # verify that the values have been normalized
    for value in mapped_output:
        assert (abs(value) <= 1)


def test_positive_roll_input():
    """Tests that only vertical thrusters are changed, and in the correct direction"""

    # create whichever thrust mapper we are testing
    mapper = Mapper()

    input_6_dof = [0, 0, 0, 1, 0, 0]
    mapped_output = mapper.calculate(input_6_dof)

    # test that the y direction send the rov forward
    assert (mapped_output.vert_front_left() > 0)
    assert (mapped_output.vert_front_right() < 0)
    assert (mapped_output.vert_back_left() > 0)
    assert (mapped_output.vert_back_right() < 0)

    # verify that the values have been normalized
    for value in mapped_output:
        assert (abs(value) <= 1)


def test_positive_pitch_input():
    """Tests that only vertical thrusters are changed, and in the correct direction"""

    # create whichever thrust mapper we are testing
    mapper = Mapper()

    input_6_dof = [0, 0, 0, 0, 1, 0]
    mapped_output = mapper.calculate(input_6_dof)

    # test that the y direction send the rov forward
    assert (mapped_output.vert_front_left() > 0)
    assert (mapped_output.vert_front_right() > 0)
    assert (mapped_output.vert_back_left() < 0)
    assert (mapped_output.vert_back_right() < 0)

    # verify that the values have been normalized
    for value in mapped_output:
        assert (abs(value) <= 1)

def test_positive_yaw_input():
    """Tests that only horizontal thrusters are changed, and in the correct direction"""

    # create whichever thrust mapper we are testing
    mapper = Mapper()

    input_6_dof = [0, 0, 0, 0, 0, 1]
    mapped_output = mapper.calculate(input_6_dof)

    # test that the y direction send the rov forward
    assert (mapped_output.hor_front_left() < 0)
    assert (mapped_output.hor_front_right() > 0)
    assert (mapped_output.hor_back_left() > 0)
    assert (mapped_output.hor_back_right() < 0)

    # verify that the values have been normalized
    for value in mapped_output:
        assert (abs(value) <= 1)


def test_z_input_and_pitch_input():
    # create whichever thrust mapper we are testing
    mapper = Mapper()

    input_6_dof = [0, 0, 1, 0, 1, 0]
    mapped_output = mapper.calculate(input_6_dof)

    # test that the y direction send the rov forward
    assert (mapped_output.vert_front_left() > 0)
    assert (mapped_output.vert_front_right() > 0)
    assert (mapped_output.vert_back_left() < mapped_output.vert_front_left())
    assert (mapped_output.vert_back_right() < mapped_output.vert_front_right())

    # verify that the values have been normalized
    for value in mapped_output:
        assert (abs(value) <= 1)