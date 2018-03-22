import copy
import os
import traceback
import datetime
from json import loads, load

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

        with open("rov/packets.json","r") as fh:
            self.dearclient = load(fh)['dearclient']


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

        self.imu = IMU()
        self.pressure = Pressure()
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
            self.imu.update()
            self.pressure.update()
            self.obs.update()
            self.esc.update()
            df = self.dearflask
            #print df, '\n', self.dearclient, '\n\n'

        except Exception as e:
            print "Failed updating things"
            print "Exception: %s" % e
            print traceback.format_exc()
        self.dearclient['obs'] = self.obs.data
        self.dearclient['esc'] = self.esc.data

        self.dearclient['imu'] = self.imu.data
        self.dearclient['pressure'] = self.pressure.data
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
