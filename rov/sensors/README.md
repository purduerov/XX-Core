# Sensor Libraries
Contains the libraries for sensors used on the ROV
- BlueRobotics Bar30 Pressure and Temp Sensor
- Adafruit BNO055 IMU

## How to write sensor libraries
Most sensors will at minimum require an update method and a way to get data.
The proposed way of handling this is with the update method and a data property
like so:
```python
class Sensor(object):
    def __init__(self):
        # init sensor
        self._data = {
            # predefined null data goes here
            pressure: 0,
            # etc
        }

    @property
    def data(self):
        return self._data

    def update(self):
        # update all data
        self._data['pressure'] += 5
```

The advantage to this is that all sensors can be updated quickly by calling
update, and data can then be extracted separately when needed.

Additionally, for each sensor, a test script should be provided to easily
verify that it is working.

## Detecting Failed Imports and Using Mock Library
Lastly, a mock library should be made in place in case the sensor is not
working.  This lets the ROV still run while a sensor may not be connected. For
example, here is how to handle dynamically choosing the mock library for the
pressure sensor:
```python
# Attemps to initialize and read the Bar30 sensor.
# If it fails updating, then use the mock pressure library.

def Pressure():
    try:
        from BlueRobotics_Bar30 import Pressure as BlueRobotics_Bar30
        pressure = BlueRobotics_Bar30()
        # Call update so it can try writing some bytes
        # It should fail fast when not connected
        pressure.update()
        return pressure
    except Exception:
        print "Failed to Initialize BlueRobotics Bar30 Pressure Sensor"
        print "Using Mock Pressure Sensor"
        from Pressure_Mock import Pressure as Pressure_Mock
        return Pressure_Mock()
```

This lets you import the pressure sensor like normally: `from pressure import
Pressure` When you attempt to initialize the pressure sensor: `Presure()`, the
method is called that figures which one to use. First, it tries to initialize
and update the data. For the pressure sensor, updating the data will throw an
exception when it cannot write to the device. Other devices, like the IMU,
throw an error when initializing, so an update call isn't required. The idea
here is to fail fast, and once we know it fails, return the mock sensor. One
important aspect, is to also put the import statements in the try/except. This
will catch when imports are missing (since some packages would not be able to
install on a dev machine).

**So, if adding a new sensor library, please take a look at the completed ones and follow
along with the proposed standard**
