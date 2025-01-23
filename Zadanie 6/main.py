from points import *
from rectangles import *

import unittest

class TestPoint(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Point(10, 10)), "(10, 10)")

    def test_repr(self):
        self.assertEqual(repr(Point(10, 10)), "Point(10, 10)")

    def test_eq(self):
        self.assertTrue(Point(10, 10) == Point(10, 10))

    def test_ne(self):
        self.assertTrue(Point(10, 10) != Point(11, 11))
        self.assertTrue(Point(10, 10) != Point(10, 11))
        self.assertTrue(Point(10, 10) != Point(11, 10))

    def test_add(self):
        self.assertEqual(Point(10, 10) + Point(10, 10), Point(20, 20))
        self.assertEqual(Point(10, 10) + Point(10, 0), Point(20, 10))
        self.assertEqual(Point(10, 10) + Point(0, 10), Point(10, 20))

    def test_sub(self):
        self.assertEqual(Point(10, 10) - Point(10, 10), Point(0, 0))
        self.assertEqual(Point(10, 10) - Point(10, 0), Point(0, 10))
        self.assertEqual(Point(10, 10) - Point(0, 10), Point(10, 0))

    def test_mul(self):
        self.assertEqual(Point(1, 2) * Point(3, 4), 11)

    def test_cross(self):
        self.assertEqual(Point(1, 2).cross(Point(3, 4)), -2)

    def test_length(self):
        self.assertEqual(Point(3, 4).length(), 5.0)


class TestRectangle(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Rectangle(10, 10, 20, 20)), "[(10, 10), (20, 20)]")

    def test_repr(self):
        self.assertEqual(repr(Rectangle(10, 10, 20, 20)), "Rectangle(10, 10, 20, 20)")

    def test_eq(self):
        self.assertTrue(Rectangle(10, 10, 20, 20) == Rectangle(10, 10, 20, 20))
 
    def test_ne(self):
        self.assertTrue(Rectangle(10, 10, 20, 20) != Rectangle(11, 11, 21, 21))
        self.assertTrue(Rectangle(10, 10, 20, 20) != Rectangle(10, 11, 20, 20))
        self.assertTrue(Rectangle(10, 10, 20, 20) != Rectangle(10, 11, 20, 20))
        self.assertTrue(Rectangle(10, 10, 20, 20) != Rectangle(10, 10, 21, 20))
        self.assertTrue(Rectangle(10, 10, 20, 20) != Rectangle(10, 10, 20, 21))
 
    def test_center(self):
        self.assertEqual(Rectangle(10, 10, 20, 20).center(), Point(15, 15))

    def test_area(self):
        self.assertEqual(Rectangle(10, 10, 20, 20).area(), 100)

    def test_move(self):
        self.assertEqual(Rectangle(10, 10, 20, 20).move(1, 1), Rectangle(11, 11, 21, 21))
        self.assertEqual(Rectangle(10, 10, 20, 20).move(-1, -1), Rectangle(9, 9, 19, 19))

if __name__ == "__main__":
    unittest.main()
