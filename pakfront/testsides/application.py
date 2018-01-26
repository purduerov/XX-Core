import multiprocessing
import os
from json import dumps, loads

from flask import Flask
from flask_socketio import SocketIO

import rov as rov

import eventlet
eventlet.sleep()
eventlet.monkey_patch(socket=False, thread=False)

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

last_rov = None

manager = multiprocessing.Manager()
lock = manager.Lock()
data = manager.dict()

data["dearclient"] = {}

data["dearflask"] = {
    "thrusters": {
        "desired_thrust": [0, 0, 0, 0, 0, 0],
        "disabled_thrusters": [],
        "thruster_scales": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    },
    "valve_turner": {
        "power": 0.0
    },
    "claw": {
        "power": 0.0
    },
    "fountain_tool": {
        "power": 0.0
    },
    "cameras": [
        { "port": 8080, "status": 1 },
        { "port": 8081, "status": 0 },
        { "port": 8082, "status": 1 },
        { "port": 8083, "status": 0 },
        { "port": 8084, "status": 1 },
        { "port": 8085, "status": 1 },
    ]
}
"""
try:
    os.system("../runCams.sh > ../mjpeg_noise.txt")
except Exception:
    print "Run mjpeg streamer on your own please"
"""

@socketio.on('connect')
def on_connect():
    print "Client connected"

@socketio.on('disconnect')
def on_disconnect():
    print "Client disconnected"

@socketio.on('dearflask')
def dearflask(indata):
    print "dearflask", indata
    with lock:
        data['dearflask'] = loads(indata)

@socketio.on('dearclient')
def dearclient(*args):
    print "dearclient"
    with lock:
        socketio.emit("dearclient", dumps(data['dearclient']))



if __name__ == 'application':
    rov_proc = multiprocessing.Process(target=rov.run, args=(lock, data))
    rov_proc.start()
