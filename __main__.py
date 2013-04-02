from adafruit import PWM
from mecanum.types import TankDrive, ServoWheels, Drive

from time import sleep
from math import sin, pi

def main():
    pwm = PWM(address=0x40, debug=False)
    pwm.setPWMFreq(50)

    # drive = TankDrive(wheels=ServoWheels(pwm))
    
    drive = Drive(wheels=ServoWheels(pwm))

    dur = 100
    freq = 30
    factor = 2 * pi * freq/8000

    # while (True):
    for seg in range(8 * dur):
        # sine wave calculations
        sin_seg = sin(seg * factor)
        #tank
        # drive.js.pos=[1,-1,sin_seg,-sin_seg]
        drive.js.pos=[sin_seg,0,1,0]
        drive.calc_speeds()
        # print "sin_seq: %s" % sin_seg
        # print drive.wheels.pos
        sleep(0.05)
    
    # reset joystick and re-calculate wheel speeds, should stop servos
    # drive.js.pos=[0,0,0,0]
    # drive.calc_speeds()
    
    # pwm.reset()

def zero():
    pwm = PWM(address=0x40, debug=False)
    pwm.setPWMFreq(50)
    drive = Drive(wheels=ServoWheels(pwm))
    # joystick at zero so we should have zeroed out drive commands
    drive.calc_speeds()
    
if __name__ == "__main__":
    zero()