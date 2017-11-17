"""
Set of tests for checking the functionality of the controller class. These tests do...
"""

import pytest
from rov.movement.controls.Control_Algorithm import *


def test_returns_empty_user_input_if_deactivated():
    # initializes a control algorithm with the desired position of 4 for the z parameter
    z = ControlAlgorithm(4,2)
    # activates then deactivates
    z.activate()
    z.deactivate()
    # checks to make sure an empty list is outputted
    assert z.calculate() == [0,0,0,0,0,0]

#todo: create test to check if pid correctly changes and gets pid values
def test_control_algorithm_correctly_gets_and_sets_pid_values():
    # initializes a control algorithm with the desired position of 2 for the y parameter
    y = ControlAlgorithm(2,1)
    # activates
    y.activate()
    y.p = 0.5
    y.i = 0.3
    y.d = 4
    assert y.p == 0.5
    assert y.i == 0.3
    assert y.d == 4

#todo: create more test cases
