from smbus import SMBus
import time

class Rov(object):

    def _intialize(rov):
        rov.bus = SMBus(1)

        rov._data = {
        # default pressure and temperature
            "pressure": 0,
            "temperature": 0,
        }


    @property
    def data(rov):
        return rov._data


    def update(rov):
        # address of the arduino
        address = 0x76
        # to tell the arduino the request number
        request = 0xAA
        offset=0

        rov.bus.read_i2c_block_data(address,offset,2)

        #read the block of data containing pressure and temperature information
        data = rov.bus.read_i2c_block_data(address,offset,12)
        Value0 = data[0]
        Value1 = data[1]
        Value2 = data[2]
        Value3 = data[3]
        Value4 = data[4]
        Value5 = data[5]
        Value6 = data[6]
        Value7 = data[7]
        Value8 = data[8]
        Value9 = data[9]
        Value10 =data[10]
        Value11 = data[11]
        print data



        time.sleep(.5)


