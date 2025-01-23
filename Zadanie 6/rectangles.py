from points import *

class Rectangle:
    def __init__(self, x1, y1, x2, y2):
        self.pt1 = Point(x1, y1)
        self.pt2 = Point(x2, y2)

    def __str__(self):
        return f"[{self.pt1}, {self.pt2}]"

    def __repr__(self):
        return f"Rectangle({self.pt1.x}, {self.pt1.y}, {self.pt2.x}, {self.pt2.y})"

    def __eq__(self, other):
        return self.pt1 == other.pt1 and self.pt2 == other.pt2

    def __ne__(self, other):
        return not self == other

    def center(self):
        s = (self.pt1 + self.pt2)
        return  Point(s.x / 2, s.y / 2)

    def area(self):
        return abs(self.pt2.x - self.pt1.x) * abs(self.pt2.y - self.pt1.y)

    def move(self, x, y):
        p = Point(x, y)
        new_pt1 = self.pt1 + p
        new_pt2 = self.pt2 + p
        return Rectangle(new_pt1.x, new_pt1.y, new_pt2.x, new_pt2.y)

