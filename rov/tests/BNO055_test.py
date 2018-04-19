import pytest
import time
from rov.sensors.imu.BNO055 import BNO055

buffer = 0.005

def test_imu_values():
	print
	for i in range(10):
		time.sleep(buffer)
		IMU.update
		print(IMU.data)	
	text = raw_input("Is this data correct (y/n)?\n")
	assert text == "y"

