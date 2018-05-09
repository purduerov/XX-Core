import subprocess
import requests
import re
from time import time

class Status():
    connected = "connected"
    unconnected = "unconnected"
    connecting = "connecting"
    datanotthrough = "connected,nodata"
    datathrough = "connected,withdata"
    level = "connected,OBSisLevel"
    idkman = "recieveddatabutitsweirdforsomereason"

class OBS(object):

    def __init__(self):
        self.x_tilt = 1
        self.y_tilt = 2
        self.z_tilt = 0
        self.time = list(range(16))
        self.amplitude = [0 for i in range(16)]

        self.timesconnected = 0
        self.connectionstostart = 5
        self.lastconnectattempt = time()
        self.voltage = 0
        
        self.lastupdate = 0
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
                         
                print ips
    
                self.lastconnectattempt = connecttime
        if self.timesconnected > self.connectionstostart:
                try:
                        r = requests.get("http://192.168.4.1",timeout = 0.1)
                except Exception(requests.exceptions.Timeout):
                        self.status = Status.datanotthrough
                else:
                        self.status = Status.datathrough
                        rawdata = r.text
                        if "Xangle" in rawdata:
                                query = "Voltage\s+(?P<volt>-?\d+\.\d+)?.*Xangle=(?P<xangle>-?\d+\.\d+)?.*Yangle=(?P<yangle>-?\d+\.\d+)?.*Count=(?P<count>\d+)"
                                found = re.find(query,rawdata)
                                self.voltage = float(found.group("volt"))
                                self.x_tilt = float(found.group("xangle"))
                                self.y_tilt = float(found.group("yangle"))

                                self.lastupdate = time()

                        elif "DATA" in rawdata: 
                                query = "DATA:(?P<points>.*)"
                                found = re.find(query,rawdata)
                                cleanedfound = found.group("points").strip("\n").replace(" ","").split(",")
                                self.amplitude = [int(c) for c in cleanedfound]

                                self.lastupdate = time()
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
    obs = OBS()
    while True:
            obs.update()
