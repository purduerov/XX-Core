def Servo(*args, **kwargs):
    try:
        from Servo import Servo as Servo
        return Servo(*args, **kwargs)
    except Exception as e:
        print "Failed to Initialize Servo"
        print "Error: %s" % e.message
        print "Using Mock Servo"
        from Servo_Mock import Servo as Servo_Mock
        return Servo_Mock()
