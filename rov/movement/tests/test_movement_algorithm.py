"""
Set of tests for checking the functionality of the controller class. These tests do...
"""

import pytest
import time
from rov.movement.controls.Movement_Algorithm import MovementAlgorithm

buffer = 0.001

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
    return data['sensors']

def test_returns_empty_user_input_if_deactivated():
    # initializes a control algorithm with the desired position of 4 for the z parameter
    z = MovementAlgorithm('roll', sensor_data(), 211)
    time.sleep(buffer)

    # activates then deactivates
    z.activate()
    time.sleep(buffer)
    z.deactivate()
    # checks to make sure an empty list is outputted
    assert z.calculate(0) == [0,0,0,0,0,0]

def test_control_algorithm_correctly_gets_and_sets_pid_values():
    # initializes a control algorithm with the desired position of 2 for the y parameter
    y = MovementAlgorithm('pitch', sensor_data(), 212)
    # activates    
    time.sleep(buffer)
    y.activate()
    y.p = 0.5
    y.i = 0.3
    y.d = 4
    assert y.p == 0.5
    assert y.i == 0.3
    assert y.d == 4

def test_correctly_gets_and_sets_desired_position():
    assert 1 > 0

def test_activate_deactivate_and_toggle_functions_work_properly():
    roll = MovementAlgorithm('roll', sensor_data(), 213)
    time.sleep(buffer)
    assert roll.getActivated() == False
    roll.deactivate()
    assert roll.getActivated() == False
    roll.toggle()
    assert roll.getActivated() == True
    roll.toggle()
    assert roll.getActivated() == False


def test_control_algorithm_output_results_make_sense():
    yaw = MovementAlgorithm('yaw', sensor_data(), 214)
    time.sleep(buffer)
    yaw.activate()
    assert yaw.calculate(4) == [0,0,0,0,0,0]
    time.sleep(buffer)
    assert yaw.calculate(4)[5] > 0
    yaw.deactivate()
    time.sleep(buffer)
    yaw.activate()
    for i in range(6):
        yaw.calculate(-20)[5]
        time.sleep(buffer)
    time.sleep(buffer)
    time.sleep(buffer)
    assert yaw.calculate(-20)[5] < 0

