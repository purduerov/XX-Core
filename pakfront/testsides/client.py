from socketIO_client import SocketIO, BaseNamespace, LoggingNamespace
from time import sleep
import logging

logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()

class NameSpace(BaseNamespace):
	def dearclient_resp(self, *args):
	    print("Response", args)

class ROVControl(object):
	def __init__(self,IP = '127.0.0.1',port = 5001):
		self.datadown = {"ugh":"why"
		}
		self.dataup = {}
		self.socket = SocketIO(IP, port, NameSpace)

	def dearclient(self,*args):
		self.dataup = args
		print("GOT DEARCLIENT",self.dataup)



if __name__ == "__main__":
	con = ROVControl()
	i = 0
	while True:
		con.socket.emit('dearclient')
		con.socket.wait(seconds=1)
		if i % 5 == 4:
			con.socket.emit('dearflask',"Blerg")#con.datadown)#,con.dataup,onresp)
		i+=1
