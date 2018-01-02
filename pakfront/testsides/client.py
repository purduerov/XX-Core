from socketIO_client import SocketIO, BaseNamespace
from time import sleep
import logging

logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()

class Namespace(BaseNamespace):
    def on_connect(self):
        print("connected to server")

    def on_disconnect(self):
        print("disconnected from server")

class ROVControl(object):
	def __init__(self,IP = '127.0.0.1',port = 5001):
		self.datadown = {
	    "thrusters": {
	        "desired_thrust": [2, 2, 2, 2, 2, 2],
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
		self.dataup = {}
		self.socket = SocketIO(IP, port)
		self.socket.on("dearclient",self.dearclient)

	def dearclient(self,*args):
		self.dataup = args

	def comm(self):
		self.socket.emit('dearclient')
		self.socket.emit('dearflask')


if __name__ == "__main__":
	con = ROVControl()
	i = 0
	while True:
		con.socket.emit('dearclient')
		if i % 5 == 0:
			con.socket.emit('dearflask')
		i+=1
		sleep(0.01)
	print(con.dataup)
