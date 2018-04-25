import smbus
import time
import sys
bus = smbus.SMBus(1)

class Elecmagnet(object):
    def __init__(self, address = 0x2b):
        self.address = address
        self.electrostate = bus.read_byte(self.address)
        if self.electrostate:
                self.electrostate = bus.read_byte(self.address)

    def update(self, state):
        if state:
                if not self.electrostate:
                        self.electrostate = bus.read_byte(self.address)
        else:
                if electrostate:
                        bus.read_byte(self.address)
                        self.electrostate = bus.read_byte(self.address)
if __name__ == "__main__":
        state = false
        elec = Elecmagnet()
        while True:
                if state:
                        print "turning on"
                else:
                        print "turning off"
                elec.update(state)
                state = ~state
                time.sleep(1) 
                
        
