import multiprocessing
import os
from json import load, loads, dumps
from pprint import pprint as pp

from flask import Flask
from flask_socketio import SocketIO

import rov.rov as rov

import eventlet
eventlet.sleep()
eventlet.monkey_patch(socket=False, thread=False)

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

last_rov = None

manager = multiprocessing.Manager()
lock = manager.Lock()
data = manager.dict()

with open("rov/packets.json","r") as fh:
    l = load(fh)
    data["dearflask"] = l["dearflask"]
    data["dearclient"] = l["dearclient"]


@socketio.on('connect')
def on_connect():
    print "Client connected"

@socketio.on('disconnect')
def on_disconnect():
    print "Client disconnected"

@socketio.on('dearflask')
def dearflask(indata):
    with lock:
        data['dearflask'] = indata
    print data['dearflask']['thrusters']['desired_thrust']

@socketio.on('dearclient')
def dearclient(*args):
    with lock:
        socketio.emit("dearclient", data['dearclient'], json=True)


if __name__ == 'application':
    rov_proc = multiprocessing.Process(target=rov.run, args=(lock, data))
    rov_proc.start()
