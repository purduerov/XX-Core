import subprocess
import requests
import re
from time import time

class Status():
    connected = "connected"
    unconnected = "unconnected"
    connecting = "connecting"
    connectednovoltage = "connectednovoltage"
    datanotthrough = "connected,nodata"
    datathrough = "connected,withdata"
    level = "connected,OBSisLevel"
    idkman = "recieveddatabutitsweirdforsomereason"

class OBS(object):

    def __init__(self,ip = "192.168.42.1",connstart=5):
        self.ip = ip
        self.x_tilt = 1
        self.y_tilt = 2
        self.z_tilt = 0
        self.time = list(range(16))
        self.amplitude = [0 for i in range(16)]

        self.timesconnected = 0 # How many times we have successfully connected
        self.connectionstostart = connstart # How many successful connection checks in order to begin requesting
        self.lastconnectattempt = time() # the last time we attempted a connection
        
        self.lastupdate = 0 # Last time we recieved correct data
        self.voltage = 0 # OBS voltage
        self.status = Status.unconnected

    def update(self):
        connecttime = time()
        if connecttime - self.lastconnectattempt > 0.1:
                rawips = subprocess.check_output(["hostname","-I"]).strip('\n').split(" ")
                ips = [ip for ip in rawips if ip]
                if len(ips) > 1:
                        self.timesconnected += 1
                        self.status = Status.connecting
                else:
                        self.timesconnected = 0
                        self.status = Status.unconnected
                         
    
                self.lastconnectattempt = connecttime
        if self.timesconnected > self.connectionstostart:
                try:
                        r = requests.get("http://{}".format(self.ip),timeout = 0.1)
                except:
                        self.status = Status.datanotthrough
                else:
                        self.status = Status.datathrough
                        rawdata = r.text
                        if "DATA" in rawdata: 
                                query = "DATA:(?P<points>.*)"
                                found = re.search(query,rawdata)
                                if found != None:
                                        cleanedfound = found.group("points").strip("\n").replace(" ","").split(",")
                                        self.amplitude = [int(c) for c in cleanedfound]

                                        self.lastupdate = time()
                                else:
                                        self.status = Status.idkman
                        elif "Xangle" in rawdata:
                                query = "Voltage=(?P<volt>-?\d+\.\d+)?.*Xangle=(?P<xangle>-?\d+\.\d+)?.*Yangle=(?P<yangle>-?\d+\.\d+)?.*Count=(?P<count>\d+)"
                                found = re.search(query,rawdata)
                                if found != None:
                                        self.voltage = float(found.group("volt"))
                                        self.x_tilt = float(found.group("xangle"))
                                        self.y_tilt = float(found.group("yangle"))

                                        self.lastupdate = time()
                                else:
                                        self.status = Status.idkman
                        elif "Voltage" in rawdata:
                                self.status = Status.connectednovoltage
                                query = "Voltage=(?P<volt>-?\d+\.\d+)?.*"
                                found = re.search(query,rawdata)
                                if found != None:
                                        self.voltage = float(found.group("volt"))
                                else:
                                        self.status = Status.idkman
                        else:
                                self.status = Status.idkman
                
    @property
    def data(self):
        return {
            'tilt': {
                'x': self.x_tilt,
                'y': self.y_tilt,
                'z': self.z_tilt
            },
            'seismograph_data': {
                'time': self.time,
                'amplitude': self.amplitude
            },
            'meta': {
                'lastupdate': time() - self.lastupdate,
                'connectstat': self.status,
                'obsvoltage': self.voltage
             }
        }

if __name__ == "__main__":
    obs = OBS( ip = "192.168.43.176")
    while True:
            obs.update()
