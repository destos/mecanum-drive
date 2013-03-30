__version__ = '0.0.1'

class Joystick(object):
    pos = [0,0,0,0]
    @property
    def x1(self):
        return self.pos[0]
    @property
    def x2(self):
        return self.pos[1]

    @property
    def y1(self):
        return self.pos[2]
    @property
    def y2(self):
        return self.pos[3]


class Wheels(object):
    pos = [0,0,0,0]
    
    def set(self, pos, point):
        self.pos[pos] = point


class Base(object):
    def __init__(self, *args, **kwargs):
        self.wheels = kwargs.pop('wheels', Wheels())
        self.js = kwargs.pop('joystick', Joystick())
        
    def calc_speeds(self):
        raise NotImplemented


class TankDrive(Base):
    # tuning params
    
    Kf = 1 # forward multi
    Kt = 1 # turning multi
    Ks = 1 
    
    # average both x axis?
    def calc_speeds(self):
        # Y axis average
        Yf = (self.js.y1 + self.js.y2)/2
        # Y axis diff average
        Yt = (self.js.y1 - self.js.y2)/2
        
        W1 = self.Kf*Yf + self.Kt*Yt + self.Ks*self.js.x1
        W2 = self.Kf*Yf + self.Kt*Yt - self.Ks*self.js.x1
        W3 = self.Kf*Yf - self.Kt*Yt + self.Ks*self.js.x1
        W4 = self.Kf*Yf - self.Kt*Yt - self.Ks*self.js.x1
        
        # print "%s %s - %s %s" % (W1, W2, W3, W4)
        
        self.wheels.set(0, W1)
        self.wheels.set(1, W2)
        self.wheels.set(2, W4)
        self.wheels.set(3, W3)
