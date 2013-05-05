class Wheels(object):
    """wheel position starts at the top left and goes clockwise around the vehicle ending at the bottom left"""
    pos = [0,0,0,0]
    
    def set(self, i, point):
        self.pos[i] = point


class ServoWheels(Wheels):
    def __init__(self, pwm):
        super(ServoWheels, self).__init__()
        self.pwm = pwm
        # TODO, accept channel asignments?
        from adafruit.servos import ContinuousServo
        for i in range(4):
            print "setting up wheel: %s" % i
            flipped = False
            # flip right side
            if i in [1,3]:
                flipped = True
            self.pos[i] = ContinuousServo(self.pwm, i, flipped=flipped)

    def set(self, i, point):
        self.pos[i].set(point)

    def get_positions(self):
        return [self.pos[i].power for i in range(4)]
