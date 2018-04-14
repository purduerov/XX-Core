"""
Set of tests for checking the functionality of the controller class. These tests do...
"""

import pytest
import time
from rov.movement.controls.Algorithm_Handler import Master_Algorithm_Handler
from random import *

buffer = 0.005
# last time
lt = time.time()

data = {'sensors':
        {
            'imu' :
            {
                'linear_acceleration' :
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

def rand():
    return (random() / 5.0) + 0.9

def rand2():
    return random() * 0.001 - 0.0005

def update_data(user_input, data, lt):
    dt = time.time() - lt
    lt = time.time()
    data['sensors']['imu']['linear_acceleration']['x'] += user_input[0] * dt * rand() + rand2()
    data['sensors']['imu']['linear_acceleration']['y'] += user_input[1] * dt * rand() + rand2()
    data['sensors']['pressure']['pressure'] += user_input[2] * dt * rand() + rand2()
    data['sensors']['imu']['euler']['roll'] += user_input[3] * dt * rand() + rand2()
    data['sensors']['imu']['euler']['pitch'] += user_input[4] * dt * rand() + rand2()
    data['sensors']['imu']['euler']['yaw'] += user_input[5] * dt * rand() + rand2()
    if data['sensors']['imu']['euler']['roll'] > 360:
        data['sensors']['imu']['euler']['roll'] -= 360
    elif data['sensors']['imu']['euler']['roll'] < 0:
        data['sensors']['imu']['euler']['roll'] += 360

@pytest.fixture()
def position(data):
    position = [0,0,0,0,0,0]

    position[0] = data['sensors']['imu']['linear_acceleration']['x']
    position[1] = data['sensors']['imu']['linear_acceleration']['y']
    position[2] = data['sensors']['pressure']['pressure']
    position[3] = data['sensors']['imu']['euler']['roll']
    position[4] = data['sensors']['imu']['euler']['pitch']
    position[5] = data['sensors']['imu']['euler']['yaw']

    return position

@pytest.fixture()
def sensor_data():
    return data['sensors']

def test_returns_empty_user_input_if_deactivated():
    # initializes a control algorithm with the desired position of 4 for the z parameter
    pass


def test_activate_and_deactivate_functionality():
    # initializes a control algorithm with the desired position of 4 for the z parameter
    frozen = [1,2,1,2,1,2]
    user_input = [0,0,0,0,0,0]
    mah = Master_Algorithm_Handler(frozen, sensor_data())
    for i in range(100):
        time.sleep(buffer)
        update_data(mah.master(user_input, frozen), data, lt)
    time.sleep(buffer)

    user_input = [0.5, 0.1, 0.2, 0.3, 0.4, 0.5]
    mah = Master_Algorithm_Handler(frozen, sensor_data())
    for i in range(100):
        time.sleep(buffer)
        update_data(mah.master(user_input, frozen), data, lt)
    for i in range(6):
        time.sleep(buffer)

    frozen = [2,1,2,1,2,1]
    user_input = [0.5, 0.1, 0.2, 0.3, 0.21, 0.14]

    for i in range(100):
        time.sleep(buffer)
        update_data(mah.master(user_input, frozen), data, lt)
    for i in range(6):
        time.sleep(buffer)
        mah.master(user_input, frozen)[i]

    frozen = [1,2,1,2,1,2]
    user_input = [0.5, 0.1, 0.2, 0.3, 0.21, 0.14]

    for i in range(100):
        time.sleep(buffer)
        update_data(mah.master(user_input, frozen), data, lt)
    for i in range(6):
        time.sleep(buffer)
        mah.master(user_input, frozen)[i]

    frozen = [3,3,3,3,3,3]
    user_input = [0.5, 0.1, 0.2, 0.3, 0.21, 0.14]

    for i in range(100):
        time.sleep(buffer)
        update_data(mah.master(user_input, frozen), data, lt)
    for i in range(6):
        time.sleep(buffer)
        mah.master(user_input, frozen)[i]

    mah.plot_data()
