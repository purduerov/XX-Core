# Attemps to initialize and read the Bar30 sensor.
# If it fails updating, then use the mock pressure library.


def Pressure():
    try:
        import ms5837
        pressure = ms5837.MS5837()
        # Call update so it can try writing some bytes
        # It should fail fast when not connected
        pressure.update()
        return pressure
    except Exception as e:
        print "Failed to Initialize BlueRobotics Bar30 Pressure Sensor"
        print "Error: %s" % e.message
        print "Using Mock Pressure Sensor"
        from Pressure_Mock import Pressure as Pressure_Mock
        return Pressure_Mock()
