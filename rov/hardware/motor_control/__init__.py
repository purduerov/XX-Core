def MotorControl(*args, **kwargs):
    try:
        from MotorControl import MotorControl as MotorControl
        return MotorControl(*args, **kwargs)
    except Exception as e:
        print "Failed to Initialize Hardware Motor Control (I2C PWM Device)"
        print "Error: %s" % e.message
        print "Using Mock Motor Control"
        from MotorControl_Mock import MotorControl as MotorControl_Mock
        return MotorControl_Mock()
