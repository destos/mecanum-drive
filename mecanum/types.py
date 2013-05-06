__version__ = (0, 0, 2)

from hardware import Wheels
from hardware import Joystick


class Base(object):

    virtual = False

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
        W3 = Yf - Yt + Xs - Xt #back right
        W4 = Yf + Yt - Xs + Xt #back left
        
        # print "%s %s - %s %s" % (W1, W2, W3, W4)
        
        self.wheels.set(0, W1)
        self.wheels.set(1, W2)
        self.wheels.set(2, W4)
        self.wheels.set(3, W3)


class Drive(Base):
    def calc_speeds(self):
        W1 = self.js.y1 + self.js.x1 + self.js.x2 #front left
        W2 = self.js.y1 - self.js.x1 - self.js.x2 #front right
        W3 = self.js.y1 + self.js.x1 - self.js.x2 #back right
        W4 = self.js.y1 - self.js.x1 + self.js.x2 #back left

        # evenly lower thrust along wheels to compensate for inputs higher than 1 and lower than -1
        high = max([abs(w) for w in [W1,W2,W3,W4]])
        for i, wheel in enumerate([W1,W2,W3,W4]):
            # from ipdb import set_trace; set_trace()
            if high > 1:
                wheel = wheel/high
            self.wheels.set(i, wheel)
