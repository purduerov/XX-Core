# Attemps to initialize the SparkFun IMU.
# If it fails on init, then use the mock IMU


def IMU():
    try:
        from Adafruit_BNO055 import IMU as Adafruit_BNO055
        return Adafruit_BNO055()
    except Exception as e:
        print "Failed to Initialize Sparkfun IMU"
        print "Error: %s" % e.message
        print "Using Mock IMU"
        from IMU_Mock import IMU as IMU_Mock
        return IMU_Mock()
