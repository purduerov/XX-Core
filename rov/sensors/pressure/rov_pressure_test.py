#!/usr/bin/python
import ms5837
import time

sensor = ms5837.MS5837_30BA() # Default I2C bus is 1 (Raspberry Pi 3)

# We must initialize the sensor before reading it
if not sensor.init():
        print "Sensor could not be initialized"
        exit(1)

# We have to read values from sensor to update pressure and temperature
if not sensor.read():
    print "Sensor read failed!"
    exit(1)

#print("Pressure: %.2f mbar") % (sensor.pressure())

#print("Temperature: %.2f C") % (sensor.temperature(ms5837.UNITS_Centigrade))

#time.sleep(2)

print("Time \tPressure (mbar) \tTemperature (C)")

# Spew readings
while True:
        if sensor.read():
            print("%s \t%0.1f \t%0.2f") % (time.strftime("%H:%M:%S", time.localtime()) + '.%d' % (time.time() % 1 * 1000),
                sensor.pressure(), # Default is mbar (no arguments)
                sensor.temperature()) # Default is degrees C (no arguments) 
        else:
                print "Sensor read failed!"
                exit(1)
