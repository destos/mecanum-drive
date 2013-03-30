# if __name__ == "__main__":
    
from adafruit import PWM
from servo import Continuous, Servo, Futaba3003, ContinuousConst
from time import sleep
import random

from math import sin, pi

pwm = PWM(address=0x40, debug=False)
pwm.setPWMFreq(50)

wheel = ContinuousConst(pwm, 0)
wheel2 = ContinuousConst(pwm, 1)

wheel.set(0)
# wheel2.set(0)

dur = 900
freq = 30
factor = 2 * pi * freq/8000

# while (True):
for seg in range(10 * dur):
    # sine wave calculations
    sin_seg = sin(seg * factor)
    # sin_seq 
    deg = int((sin_seg))
    wheel.set(deg)
    print "%s" % deg
    sleep(0.05)

pwm.reset()