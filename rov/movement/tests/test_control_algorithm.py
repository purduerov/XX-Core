"""
Set of tests for checking the functionality of the controller class. These tests do...
"""

import pytest
from rov.movement.controls.Control_Algorithm import *

@pytest.fixture()
def sensor_data():
    data = {'sensors':
            {
                'imu' :
                {
                    'linear-acceleration' :
                    {
                        'x' : 1,
                        'y' : 1
                        },
                    'euler' :
                    {
                        'roll': 1,
                        'pitch': 1,
                        'yaw': 1
                    }
                },
                'pressure' :
                {
                    'pressure': 1
                }
            }
        }
    return data

def test_returns_empty_user_input_if_deactivated():
    # initializes a control algorithm with the desired position of 4 for the z parameter
    z = ControlAlgorithm('z', sensor_data())
    # activates then deactivates
    z.activate()
    z.desired_position = 4
    z.deactivate()
    # checks to make sure an empty list is outputted
    assert z.calculate() == [0,0,0,0,0,0]

def test_control_algorithm_correctly_gets_and_sets_pid_values():
    # initializes a control algorithm with the desired position of 2 for the y parameter
    y = ControlAlgorithm('y', sensor_data())
    # activates
    y.activate()
    y.p = 0.5
    y.i = 0.3
    y.d = 4
    assert y.p == 0.5
    assert y.i == 0.3
    assert y.d == 4

def test_correctly_gets_and_sets_desired_position():
    x = ControlAlgorithm('x', sensor_data())
    x.activate()
    x.desired_position = 4
    output = x.calculate()
    assert x.desired_position == 4
    assert output[0] > 0

def test_activate_deactivate_and_toggle_functions_work_properly():
    roll = ControlAlgorithm('roll', sensor_data())
    roll.deactivate()
    assert roll.getActivated() == False
    roll.toggle()
    assert roll.getActivated() == True
    roll.toggle()
    assert roll.getActivated() == False


def test_control_algorithm_output_results_make_sense():
    
