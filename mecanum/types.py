__version__ = '0.0.1'

from servo import ContinuousConst

class Joystick(object):
    pos = [0,0,0,0]
    @property
    def x1(self):
        return float(self.pos[0])
    @property
    def x2(self):
        return float(self.pos[1])

    @property
    def y1(self):
        return float(self.pos[2])
    @property
    def y2(self):
        return float(self.pos[3])


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
            self.pos[i] = ContinuousConst(self.pwm, i)

    def set(self, i, point):
        self.pos[i].set(point)


class Base(object):
    def __init__(self, *args, **kwargs):
        self.wheels = kwargs.pop('wheels', Wheels())
        self.js = kwargs.pop('joystick', Joystick())

    def calc_speeds(self):
        raise NotImplemented


# http://www.chiefdelphi.com/forums/showthread.php?t=84446
class TankDrive(Base):
    
    # average both x axis?
    def calc_speeds(self):
        # Y axis average
        Yf = (self.js.y1 + self.js.y2)/2
        # Y axis diff average
        Yt = (self.js.y1 - self.js.y2)/2
        
        # X axis slide average
        Xs = (self.js.x1 + self.js.x2)/2
        Xt = (self.js.x1 - self.js.x2)/2
        
        
        W1 = Yf + Yt + Xs + Xt #front left
        W2 = Yf - Yt - Xs - Xt #front right
        W3 = Yf + Yt - Xs + Xt #back left 
        W4 = Yf - Yt + Xs - Xt #back right
        
        # print "%s %s - %s %s" % (W1, W2, W3, W4)
        
        self.wheels.set(0, W1)
        self.wheels.set(1, W2)
        self.wheels.set(2, W4)
        self.wheels.set(3, W3)


class Drive(Base):
    def calc_speeds(self):
        W1 = self.js.y1 + self.js.x1 + self.js.x2 #front left
        W2 = self.js.y1 - self.js.x1 - self.js.x2 #front right
        W3 = self.js.y1 + self.js.x1 - self.js.x2 #back left 
        W4 = self.js.y1 - self.js.x1 + self.js.x2 #back right
        
        # print "%s %s - %s %s" % (W1, W2, W3, W4)
        
        # evenly lower trust along wheels to compensate for directional thrust
        # high = max([abs(w) for w in [W1,W2,W3,W4]])
        # print high
        # if high > 1:
            # high = high 
            # print 'high'
            # print [W1,W2,W3,W4]
            # [W1,W2,W3,W4] = [ (w/2) for w in [W1,W2,W3,W4]]
        
        self.wheels.set(0, W1)
        self.wheels.set(1, W2)
        self.wheels.set(2, W3)
        self.wheels.set(3, W4)
        