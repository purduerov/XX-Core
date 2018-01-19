from socketIO_client import SocketIO, BaseNamespace, LoggingNamespace
from time import sleep
from json import dumps
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
	def __init__(self,IP = '127.0.0.1',port = 5001):
		self.datadown = {}
		self.dataup = {}
		self.socket = SocketIO(IP, port, NameSpace)

	def dearclient(self,*args):
		self.dataup = args
		print("GOT DEARCLIENT",self.dataup)

	def getClient(self):
		self.socket.emit('dearclient')
		self.socket.wait(seconds=1)

		return self.dataup

	def getFlask(self,data):
		self.socket.emit('dearflask',dumps(data))#,con.dataup,onresp)

if __name__ == "__main__":
	con = ROVControl()
	i = 0
	while True:
		con.getClient()
		if i % 5 == 4:
			con.getFlask(con.datadown)
		i+=1
