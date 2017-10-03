import copy
import os
import traceback

from threading import Lock
from time import time, sleep


from sensors import Pressure, IMU

from hardware.motor_control import MotorControl



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
        #self.cameras = Cameras(
        #    resolution='640x480',
        #    framerate=30,
        #    port_start=8080,
        #    brightness=16,
        #    contrast=32
        #)

        self.motor_control = MotorControl(
            zero_power=305,
            neg_max_power=222,
            pos_max_power=388,
            frequency=47
        )

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
            print df


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
