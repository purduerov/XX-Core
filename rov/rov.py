import copy
import os
import traceback

from threading import Lock
from time import time, sleep


from sensors import Pressure, IMU
from camera import Cameras

from hardware.motor_control import MotorControl

from thrusters.Control import ThrusterControl
from thrusters.hardware.PWM_Control import Thrusters
from thrusters.mapper.Simple import Mapper

from tools import Claw, ValveTurner, FountainTool


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

        self.thrusters = Thrusters(
            self.motor_control,
            [7, 4, 6, 5, 10, 0, 11, 1]
        )

        self.thrust_mapper = Mapper()

        self.thruster_control = ThrusterControl(
            self.thrusters,
            self.thrust_mapper,
            num_thrusters=8,
            ramp=True,
            max_ramp=0.03
        )

        self.valve_turner = ValveTurner(
            self.motor_control,
            pin=8
        )

        self.claw_status = False
        self.claw = Claw(
            self.motor_control,
            pin=3
        )

        self.fountain_tool = FountainTool(
            self.motor_control,
            pin=2
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

            self.thruster_control.update(**df['thrusters'])

            self.valve_turner.update(df['valve_turner']['power'])
            self.fountain_tool.update(df['fountain_tool']['power'])

            # if 'claw' is powered, turn off, else if last status was off but current status is on then let it be on (turn ramping off).
            # This assumes an on period per button press of about 10ms.
            if self.claw_status == True and df['claw']['power'] != 0:
                claw_power = (df['claw']['power'])
            else:
                claw_power = 0.0

            self.claw.update(claw_power)
            if df['claw']['power'] != 0:
                self.claw_status = True
            else:
                self.claw_status = False

            #cam = df['cameras']
            #for cam in df['cameras']:
            #    if (cam['status'] == 0):
            #        self.cameras.kill(cam['port'])
            #    if (cam['status'] == 1):
            #        self.cameras.start(cam['port'])

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
        self.dearclient['thrusters'] = self.thruster_control.data
        #self.dearclient['cameras'] = self.cameras.status()

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
