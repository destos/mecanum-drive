from .servos import ContinuousServo


class Wheels(object):
    """wheel position starts at the top left and goes clockwise around the vehicle ending at the bottom left"""
    pos = [0,0,0,0]
    
    def set(self, i, point):
        self.pos[i] = point


class ServoWheels(Wheels):
    def __init__(self, pwm):
        super(ServoWheels, self).__init__()
        self.pwm = pwm
        # TODO, accept channel asignments
        for i in range(4):
            print "setting up wheel: %s" % i
            self.pos[i] = ContinuousServo(self.pwm, i)

    def set(self, i, point):
        self.pos[i].set(point)
