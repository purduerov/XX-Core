from __future__ import print_function
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
from hardware.servo import Servo

# Class that controls the rov movement
from movement import controller

from sensors import OBS, ESC
# from sensors import IMU # IMU is broken
from sensors import Pressure

from camera import Cameras

from tools import Manipulator, OBS_Tool, Elecmagnet, Transmitter

# THIS IS NEW and everyone's going to need to download psutil to work the rov file
import psutil

def memory_usage_psutil():
    # return the memory usage in percentage like top
    process = psutil.Process(os.getpid())
    return process.memory_percent()

class ROV(object):

    def __init__(self, lock, data):
        self._data_lock = lock

        self._data = data
        self.dearflask = self._data['dearflask']
        self.dearclient = self._data['dearclient']

        self.last_update = time()

        self._running = True

        #with open("rov/packets.json","r") as fh:
        #    temp = load(fh)
        #    self.dearclient = temp['dearclient']
        #    self.dearflask = temp['dearflask']

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
        self.maincam_servo = Servo()

        # Thrusters
        self.controls = controller(self.motor_control, self._data)

        # Tools
        self.manipulator = Manipulator(self.motor_control, pin=MANIPULATOR_PIN)
        self.obs_tool = OBS_Tool(self.motor_control, pin=OBS_TOOL_PIN)
        self.elecmagnet = Elecmagnet()
        self.transmitter = Transmitter(self.motor_control, pin=TRANSMITTER_PIN)

        # Sensors
        # self.imu = IMU()
        self.pressure = Pressure()
        self.obs = OBS()
        self.esc = ESC()

    def update(self):
        # TODO: Fix data locking?

        with self._data_lock:
            df = self.dearflask = self._data['dearflask']

        #if time() - self._last_packet > 0.5:
            # print 'Data connection lost \n...Killing Thrusters'
            # self.motor_control.kill()
            # self.thruster_control.stop()

        try:
            print(self.dearclient)
            print(memory_usage_psutil())
            print('')
            self.elecmagnet.update(df['magnet'])
            # Updating Sensors
            # self.imu.update()
            self.pressure.update()
            self.obs.update()
            self.esc.update()
            # Updating hardware
            self.maincam_servo.setAngle(df['maincam_angle'])
            self.controls.update()
            self.obs_tool.update(self.dearflask['obs_tool'])
            self.manipulator.update(self.dearflask['manipulator'])
            #print df, '\n', self.dearclient, '\n\n'
            self.transmitter.update(df['transmitter'])

        except Exception as e:
            print ("Failed updating things")
            print ("Exception: %s" % e)
            print (traceback.format_exc())
        self.dearclient['sensors']['obs'] = self.obs.data
        self.dearclient['sensors']['esc'] = self.esc.data

        # self.dearclient['sensors']['imu'] = self.imu.data
        self.dearclient['sensors']['pressure'] = self.pressure.data
        self.dearclient['thrusters'] = self.controls.data
        #self.dearclient['obs_tool'] = self.obs_tool.data
        #self.dearclient['manipulator'] = self.manipulator.data
        self.last_update = time()

        now = datetime.datetime.now()
        self.dearclient['last_update'] = "{day}_{hour}_{minu}_{sec}_{usec}".format(day=str(now.day).zfill(2),
                                                                            hour=str(now.hour).zfill(2),
                                                                            minu=str(now.minute).zfill(2),
                                                                            sec=str(now.second).zfill(2),
                                                                            usec=str(now.microsecond).zfill(6))
        #print (self.dearclient['last_update'])
        #print (self.dearflask['thrusters']['desired_thrust'])
        #for i in self.dearclient['thrusters']:
        #    print ("%.3f " % i, end='')
        #print ('')

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
            print ("Exception: %s" % e)
            print (traceback.format_exc())
