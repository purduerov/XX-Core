from socketIO_client import SocketIO, LoggingNamespace

class ROVControl(object):
	def __init__(self,IP = 'localhost',port = 5000):
		self.socket = SocketIO(IP, port, LoggingNamespace)
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
		self.socket.on("dearclient",self.dearclient)

	def dearclient(self,*args):
		self.dataup = args[0]

	def comm(self):
		self.socket.emit('dearflask',self.datadown)
		self.socket.emit('dearclient')
		self.socket.wait(seconds=1)


if __name__ == "__main__":
	con = ROVControl()
	i = 0
	print(con.datadown.keys())
	while True:
		con.comm()
		print(con.dataup)
		con.datadown = i
		i+=1
