import wiringpi
import time

class Servo(object):
    """ Look here for more of how this works:
        https://learn.adafruit.com/adafruits-raspberry-pi-lesson-8-using-a-servo-motor/software """
    def __init__(self, pin=12):
        self.pin = pin

        # sets up wiring pi gpio
        wiringpi.wiringPiSetupGpio()

        # set the pin to pwm output
        wiringpi.pinMode(self.pin, wiringpi.GPIO.PWM_OUTPUT)

        # set pwm mode to ms that duty cycle is on
        wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

        # PWM Frequency in Hz = 19,200,000 Hz / pwmClock / pwmRange
        # Solve for 50 Hz

        # PWM clock speed
        wiringpi.pwmSetClock(192)

        # PWM range
        wiringpi.pwmSetRange(2000)
        self.setAngle(0)

    def setAngle(self, rawangle):
        # map [-90, 90] to [50, 249]
        # mapping values are 0.5ms (50) to 2.5ms (250)
        # don't go all the way to 250, because the servo vibrates because it's just too far
        if rawangle > 90:
                angle = 90
        elif rawangle < -90:
                angle = -90
        else:
                angle = rawangle
        pulse = self.range_map(rawangle, -90, 90, 50, 240)

        wiringpi.pwmWrite(self.pin, pulse)
        time.sleep(0.01)
        wiringpi.pwmWrite(self.pin, 0)

    def range_map(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return int(round(rightMin + (valueScaled * rightSpan)))
if __name__ == "__main__":
    s = Servo()
    while True:
        s.setAngle(-40)
