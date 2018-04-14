import pytest
import time
from rov.sensors.pressure import ms5837

buffer = 0.005

def test_pressure_values():
    print("Time \tPressure (mbar) \tTemperature (C)\n")
    for i in range(10):
        time.sleep(buffer)
        print(MS5837.getData)
        print("\n")
    text = input("Is data correct (y/n)")
    assert text == "y"
    
