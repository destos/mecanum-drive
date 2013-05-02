# TODO: maybe use http://www.html5rocks.com/en/tutorials/doodles/gamepad/ as well

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


class JoystickTwoSticks(object):
    pos = [[0,0],[0,0]]
    @property
    def x1(self):
        return float(self.pos[0][0])
    @property
    def x2(self):
        return float(self.pos[1][0])

    @property
    def y1(self):
        return float(self.pos[0][1])
    @property
    def y2(self):
        return float(self.pos[1][1])