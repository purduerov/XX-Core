import pytest
import time
from rov.sensors.pressure.ms5837 import MS5837

buffer = 0.005

def test_pressure_values():
    print("Time \tPressure (mbar) \tTemperature (C)\n")
    for i in range(10):
        time.sleep(buffer)
        print(MS5837.getData)
        print("\n")
    text = raw_input("Is data correct (y/n)\n")
    assert text == "y"
    
