# Attemps to initialize the SparkFun IMU.
# If it fails on init, then use the mock IMU


def IMU():
    try:
        from BNO055 import BNO055
        return BNO055()
    except Exception as e:
        print "Failed to Initialize Sparkfun IMU"
        print "Error: %s" % e.message
        print "Using Mock IMU"
        from IMU_Mock import IMU as IMU_Mock
        return IMU_Mock()
