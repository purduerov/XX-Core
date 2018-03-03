import copy
import os
import traceback
import datetime

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

from sensors import Pressure, IMU

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

    def update(self):
        with self._data_lock:
            self.dearflask = self._data['dearflask']

        # if time() - self._last_packet > 0.5:
            # # print 'Data connection lost'
            # self.motor_control.kill()
            # self.thruster_control.stop()

        try:
            df = self.dearflask
            print df, self.dearclient


            """ Disabled until hardware is done and sw is tested
            self.pressure.update()
            self.IMU.update()
            """
        except Exception as e:
            print "Failed updating things"
            print "Exception: %s" % e
            print traceback.format_exc()


        # retrieve all sensor data
        # self.dearclient['sensor'] = sensorThings

        self.last_update = time()

        now = datetime.datetime.now()
        self.dearclient['last_update'] = "{day}_{hour}_{minu}_{sec}_{usec}".format(day=now.day,
                                                                            hour=now.hour,
                                                                            minu=now.minute,
                                                                            sec=now.second,
                                                                            usec=now.microsecond)

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
