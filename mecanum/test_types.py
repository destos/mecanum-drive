from unittest import TestCase

from .types import TankDrive

class TestTandDrive(TestCase):
    def setUp(self):
        self.drive = TankDrive()
    
    def test_neutral(self):
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [0,0,0,0])
        
    def test_strafe_left(self):
        """all x axis left strafes left"""
        self.drive.js.pos = [-1,-1,0,0]
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [0,0,0,0])
    
    def test_strafe_right(self):
        """all x asix right strages right"""
        self.drive.js.pos = [1,1,0,0]
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [0,0,0,0])
    
    def test_full_forward(self):
        """both y axis forward full power forward"""
        self.drive.js.pos = [0,0,1,1]
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [0,0,0,0])
    
    def test_fill_backwards(self):
        """both y axis backwards full power backwards"""
        self.drive.js.pos = [0,0,-1,-1]
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [0,0,0,0])
    
    def test_rotate_clockwise(self):
        """left x high, right x low"""
        self.drive.js.pos = [0,0,1,-1]
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [0,0,0,0])
    
    def test_rotate_anticlockwise(self):
        """left x low, right x high"""
        self.drive.js.pos = [0,0,-1,1]
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [0,0,0,0])
    
    def test_half_forward(self):
        """left x low, right x high"""
        self.drive.js.pos = [0.5,0.5,0,0]
        self.drive.calc_speeds()
        self.assertEqual(self.drive.wheels.pos, [0,0,0,0])
    

if __name__ == '__main__':
    unittest.main()