import smbus
import time
bus = smbus.SMBus(1)
address = 0x2b
while True:
    data =[]
    for i in range(16):
        data.append(bus.read_byte(address))
    print data
    time.sleep(1)

