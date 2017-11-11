"""
Set of tests for checking the functionality of the controller class. These tests do...
"""

import pytest
from rov.movement.controls.Control_Algorithm import *


def test_returns_empty_user_input_if_deactivated():
    # initializes a control algorithm with the desired position of 4 for the z parameter
    x = ControlAlgorithm(4,2)
    #activates then deactivates
    x.activate()
    x.deactivate()
    # checks to make sure an empty list is outputted
    assert x.calculate() == [0,0,0,0,0,0]