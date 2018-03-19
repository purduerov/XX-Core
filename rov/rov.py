import copy
import os
import traceback

# this folder no longer exists 
# nor were the files being used
# from controls import *	#Tested


from threading import Lock
from time import time, sleep

# Import constants to initiate the hardware
from init_hw_constants import *

# Class that communicates to the i2c to pwm chip that controls the brushless motors
from hardware.motor_control import MotorControl

# Class that controls the rov movement
from movement import controller

from sensors import Pressure, IMU, OBS, ESC

from camera import Cameras


class ROV(object):

    def __init__(self, lock, data):
        self._data_lock = lock

        self._data = data
        self._new_data = False
        self._last_packet = time() - 1

        self.last_update = time()

        self._running = True

        self.dearclient = {}
        self.dearflask = {}

        self.debug = (os.environ.get("ROV_DEBUG") == "1")

        self.init_hw()

    def init_hw(self):
        self.cameras = Cameras(
            resolution='640x480',
            framerate=30,
            port=8080,
            brightness=16,
            contrast=32
        ).start()

        self.motor_control = MotorControl(
            zero_power=ZERO_POWER,
            neg_max_power=NEG_MAX_POWER,
            pos_max_power=POS_MAX_POWER,
            frequency=FREQUENCY
        )

        self.controls = controller(self.motor_control)

        #""" Disabled until hardware is done and sw is tested
        # self.IMU = IMU()
        # self.pressure = Pressure()
        #"""
        self.obs = OBS()
        self.esc = ESC()

    def update(self):
        with self._data_lock:
            self.dearflask = self._data['dearflask']

        # if time() - self._last_packet > 0.5:
            # # print 'Data connection lost'
            # self.motor_control.kill()
            # self.thruster_control.stop()

        try:
            self.obs.update()
            self.esc.update()
            df = self.dearflask
            #print df

            # Calculate the new thurster values, set the thrusters to that value, and
            # then record that value in dearclient
            thruster_output = self.controls.update(self.dearflask["thrusters"])
            self.dearclient["thrusters"] = thruster_output

            """ Disabled until hardware is done and sw is tested
            self.pressure.update()
            self.IMU.update()
            """
        except Exception as e:
            print "Failed updating things"
            print "Exception: %s" % e
            print traceback.format_exc()
        self.dearclient['obs'] = self.obs.data
        self.dearclient['esc'] = self.esc.data

        # retrieve all sensor data
        # self.dearclient['sensor'] = sensorThings

        self.last_update = time()

        self.dearclient['last_update'] = self.last_update

        with self._data_lock:
            self._data['dearclient'] = self.dearclient


def run(lock, data):
    rov = ROV(lock, data)
    while True:
        while time() - rov.last_update < 0.01:
            sleep(0.005)

        try:
            rov.update()
        except Exception as e:
            print "Exception: %s" % e
            print traceback.format_exc()

"""This main loop will only run if ./scotty run --rov is called.
    This main loop will be used to run the ROV without having to
    run the flask server."""
if __name__ == "__main__":
    # imports that are needed for testing but not anywhere else
    import json
    from pprint import pprint
    from copy import deepcopy
    import multiprocessing

    # constants to pass as input for future improvement
    inputFileName = 'rov/json_test_files/testOutput.json'
    outputFileName = 'rov/json_test_files/json_output.json'

    # open the file that is going to be read
    with open(inputFileName, 'r') as input_file:
        test_data = json.load(input_file)

    # create a multithread manager for the rov class
    # only needed in the testing case to make the class run.
    manager = multiprocessing.Manager()
    lock = manager.Lock()
    data = manager.dict()

    # create the rov class
    test_rov = ROV(lock, data)

    # a list which will store all of the outputed dearclients
    all_dearclients = []

    # loop over all of the json files, run update, and then store the dearclient output
    for curr_data in test_data:
        data['dearflask'] = curr_data
        test_rov.update()
        all_dearclients.append(deepcopy(data['dearclient']))

    # write the contents of dear client out to a file
    with open(outputFileName, 'w') as outFile:
        outFile.write(json.dumps(all_dearclients, indent=3, sort_keys=True))