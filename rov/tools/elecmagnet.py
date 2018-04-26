import smbus
import time
import sys
bus = smbus.SMBus(1)

class Elecmagnet(object):
    def __init__(self, address = 0x2c):
        self.address = address
        self.setelectrostate(bus.read_byte(self.address))
        if self.electrostate:
                self.setelectrostate(bus.read_byte(self.address))

    def setelectrostate(self,ret):
        print ret
        if ret == 10 :
                self.electrostate = False 
        else:
                self.electrostate = True

    def update(self, state):
        if state:
            if not self.electrostate:
                self.setelectrostate(bus.read_byte(self.address))
        else:
            if self.electrostate:
                self.setelectrostate(bus.read_byte(self.address))
if __name__ == "__main__":
        mode = False
        elec = Elecmagnet()
        while True:
                if mode:
                        print "turning on"
                else:
                        print "turning off"
                elec.update(mode)
                mode = ~mode
                time.sleep(60) 
                
        
