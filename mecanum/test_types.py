from unittest import TestCase

from .types import TankDrive

class TestTankDrive(TestCase):
    def setUp(self):
        self.drive = TankDrive()
        # joystick values
        # self.drive.js.pos = [x1,x2,y1,y2]
    
    def test_neutral(self):
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [0,0,0,0])
        
    def test_strafe_left(self):
        """all x axis left strafes left"""
        self.drive.js.pos = [-1,-1,0,0]
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [-1,1,1,-1])
    
    def test_strafe_right(self):
        """all x asix right strafes right"""
        self.drive.js.pos = [1,1,0,0]
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [1,-1,-1,1])
    
    def test_strafe_right_one_x_axis(self):
        """docstring for test_strafe_one_x_axis"""
        self.drive.js.pos = [1,0,0,0]
        self.drive.calc_speeds()
        # should be half speed strafe
        self.assertEqual(self.drive.wheels.pos, [0.5,-0.5,-0.5,0.5])
        
    def test_full_forward(self):
        """both y axis forward full power forward"""
        self.drive.js.pos = [0,0,1,1]
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [1,1,1,1])
    
    def test_full_backwards(self):
        """both y axis backwards full power backwards"""
        self.drive.js.pos = [0,0,-1,-1]
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [-1,-1,-1,-1])
    
    def test_rotate_clockwise(self):
        """left x high, right x low"""
        self.drive.js.pos = [0,0,1,-1]
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [1,1,-1,-1])
    
    def test_rotate_anticlockwise(self):
        """left x low, right x high"""
        self.drive.js.pos = [0,0,-1,1]
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [-1,-1,1,1])
    
    def test_half_forward(self):
        """half speed forward"""
        self.drive.js.pos = [0,0,0.5,0.5]
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [0.5,0.5,0.5,0.5])
    
    def test_half_forward_one_x_axis_full(self):
        """half speed forward"""
        self.drive.js.pos = [0,0,1,0]
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [0.5,0.5,0.5,0.5])
        self.drive.js.pos = [0,0,0,1]
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [0.5,0.5,0.5,0.5])
    
    def test_diagonal(self):
        """move it crazy like"""
        self.drive.js.pos = [1,1,1,1]
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [0,0,0,0])
    

if __name__ == '__main__':
    unittest.main()