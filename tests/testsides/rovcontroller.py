from socketIO_client import SocketIO, BaseNamespace, LoggingNamespace
from json import dumps, loads
import os
import logging

logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()

class NameSpace(BaseNamespace):
    def on_connect(self):
        print("[Connected to Server]")

    def on_reconnect(self):
        print("[Reconnected to Server]")

    def on_disconnect(self):
        print("[Disconnected from Server]")

    def dearclient_resp(self, *args):
        print("Response", args)

class ROVControl(object):
    def __init__(self,IP = 'localhost',port = 5001):
        self.datadown = {"ROV":"DOO THINGS"}
        self.dataup = {}
        self.socket = SocketIO(IP, port, NameSpace)
        self.socket.on('dearclient',self.dearclient)

    def dearclient(self,*args):
        self.dataup = args

    def getClient(self):
        self.socket.emit('dearclient')
        self.socket.wait(seconds=0.01)

        return self.dataup

    def getFlask(self,data):
        self.socket.emit('dearflask',data)#,con.dataup,onresp)

def getDefaultPackets(packetpath):
    if not os.path.exists(packetpath):
        raise OSError("FILE DOES NOT EXIST")
    elif "packets.json" not in packetpath:
        raise OSError("THE PATH NEEDS TO POINT TO PACKETS.JSON")
    else:
        with open(packetpath, "r") as fh:
                    data = loads(fh.read().decode('string-escape').strip('"'))
    return data
                
