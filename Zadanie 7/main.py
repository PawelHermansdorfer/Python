# ZADANIE 7.1
from math import gcd

class Frac:
    def __init__(self, x=0, y=1):
        if y == 0:
            raise ValueError("y is 0")
        self.x = x
        self.y = y

    def __str__(self):
        if self.y != 1:
            return f"{self.x}/{self.y}"
        else:
            return f"{self.x}"

    def __repr__(self):
        return f"Frac({self.x}, {self.y})"

    def __eq__(self, other):
        if isinstance(other, int): other = Frac(other)
        self_gcd = gcd(self.x, self.y)
        other_gcd = gcd(other.x, other.y)
        normal_check = (self.x // self_gcd == other.x // other_gcd
                    and self.y // self_gcd == other.y // other_gcd)
        neg_check =    (self.x // self_gcd == -other.x // other_gcd
                    and self.y // self_gcd == -other.y // other_gcd)
        return normal_check or neg_check

    def __ne__(self, other):
        if isinstance(other, int): other = Frac(other)
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, int): other = Frac(other)
        return self.x * other.y < other.x * self.y

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        if isinstance(other, int): other = Frac(other)
        return self.x * other.y > other.x * self.y

    def __ge__(self, other):
        return self > other or self == other

    def __add__(self, other):
        if isinstance(other, int): other = Frac(other)
        x = self.x * other.y + other.x * self.y
        y = self.y * other.y
        return Frac(x, y)

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, int): other = Frac(other)
        x = self.x * other.y - other.x * self.y
        y = self.y * other.y
        return Frac(x, y)

    def __rsub__(self, other):
        if isinstance(other, int): other = Frac(other)
        return other - self

    def __mul__(self, other):
        if isinstance(other, int): other = Frac(other)
        x = self.x * other.x
        y = self.y * other.y
        return Frac(x, y)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, int): other = Frac(other)
        if other == 0:
            raise ZeroDivisionError("division by 0")
        x = self.x * other.y
        y = self.y * other.x
        return Frac(x, y)

    def __rtruediv__(self, other):
        if isinstance(other, int): other = Frac(other)
        return other / self

    def __pos__(self):
        return self

    def __neg__(self):
        return Frac(-self.x, self.y)

    def __invert__(self):
        if self == 0:
            return Frac(0)
        return Frac(self.y, self.x)

    def __float__(self):
        return self.x / self.y

    def __hash__(self):
        return hash((self.x, self.y))


import unittest

class TestFrac(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Frac(1, 2)), "1/2")
        self.assertEqual(str(Frac(3, 1)), "3")
        self.assertEqual(str(Frac(3, 3)), "3/3")
        self.assertRaises(ValueError, Frac, 1, 0)

    def test_repr(self):
        self.assertEqual(repr(Frac(1, 2)), "Frac(1, 2)")
        self.assertEqual(repr(Frac(0, 2)), "Frac(0, 2)")

    def test_eq(self):
        self.assertTrue(Frac(1, 2) == Frac(1, 2))
        self.assertTrue(Frac(2, 4) == Frac(1, 2))
        self.assertTrue(Frac(0, 2) == Frac(0))
        self.assertTrue(Frac(-1, -2) == Frac(1, 2))

    def test_ne(self):
        self.assertTrue(Frac(1, 2) != Frac(1, 3))
        self.assertTrue(Frac(-1, 2) != Frac(1, 2))
        self.assertTrue(Frac(-1, -2) != Frac(-1, 2))

    def test_lt(self):
        self.assertTrue(Frac(1, 3) < Frac(1, 2))
        self.assertTrue(Frac(2, 5) < Frac(3, 5))

    def test_le(self):
        self.assertTrue(Frac(1, 3) <= Frac(1, 2))
        self.assertTrue(Frac(2, 5) <= Frac(3, 5))
        self.assertTrue(Frac(3, 5) <= Frac(3, 5))
        self.assertTrue(Frac(10, 5) <= Frac(2, 1))


    def test_gt(self):
        self.assertTrue(Frac(1, 2) > Frac(1, 3))
        self.assertTrue(Frac(3, 5) > Frac(2, 5))

    def test_ge(self):
        self.assertTrue(Frac(1, 2) >= Frac(1, 3))
        self.assertTrue(Frac(3, 5) >= Frac(2, 5))
        self.assertTrue(Frac(3, 5) >= Frac(3, 5))
        self.assertTrue(Frac(10, 5) >= Frac(2, 1))

    def test_add(self):
        self.assertEqual(Frac(1, 3) + Frac(1, 2), Frac(5, 6))
        self.assertEqual(Frac(0, 3) + Frac(1, 2), Frac(1, 2))
        self.assertEqual(Frac(-1, 3) + Frac(1, 3), Frac(0))
        self.assertEqual(Frac(-1, 3) + 1, Frac(2, 3))
        self.assertEqual(Frac(0) + 1, Frac(1))
        self.assertEqual(Frac(2, 5) + 1, Frac(7, 5))
        self.assertEqual(1 + Frac(2, 5), Frac(7, 5))

    def test_sub(self):
        self.assertEqual(Frac(1, 3) - Frac(1, 3), Frac(0))
        self.assertEqual(Frac(0, 3) - Frac(1, 2), Frac(-1, 2))
        self.assertEqual(Frac(1, 3) - Frac(1, 3), Frac(0))
        self.assertEqual(Frac(1, 3) - 1, Frac(-2, 3))
        self.assertEqual(Frac(0) - 1, Frac(-1))
        self.assertEqual(1 - Frac(2), Frac(-1))
        self.assertEqual(0 - Frac(1, 2), Frac(-1, 2))

    def test_mul(self):
        self.assertEqual(Frac(1, 2) * Frac(1), Frac(1, 2))
        self.assertEqual(Frac(1, 2) * Frac(0), Frac(0))
        self.assertEqual(Frac(1, 2) * Frac(2), Frac(1))
        self.assertEqual(Frac(1, 2) * Frac(1, 2), Frac(1, 4))
        self.assertEqual(Frac(1, 2) * Frac(2, 1), Frac(1))
        self.assertEqual(1 * Frac(2, 1), Frac(2))
        self.assertEqual(2 * Frac(2, 1), Frac(4))

    def test_div(self):
        self.assertEqual(Frac(1, 2) / Frac(1), Frac(1, 2))
        self.assertRaises(ZeroDivisionError,  Frac.__truediv__, Frac(1, 2), Frac(0))
        self.assertEqual(Frac(1, 2) / Frac(2), Frac(1, 4))
        self.assertEqual(Frac(1, 2) / 2, Frac(1, 4))
        self.assertEqual(2 / Frac(1, 2), Frac(4))
        self.assertEqual(0 / Frac(1, 2), Frac(0))

    def test_pos(self):
        self.assertEqual(+Frac(1, 2), Frac(1, 2))

    def test_neq(self):
        self.assertEqual(-Frac(1, 2), Frac(-1, 2))
        self.assertEqual(-Frac(1, 2), Frac(1, -2))
        self.assertEqual(-Frac(0), Frac(0))

    def test_invert(self):
        self.assertEqual(~Frac(1, 2), Frac(2, 1))
        self.assertEqual(~Frac(0), 0)
        self.assertEqual(~Frac(2), Frac(1, 2))

    def test_assertEqual(self):
        self.assertEqual(float(Frac(1, 2)), 0.5)
        self.assertEqual(float(Frac(3, 4)), 0.75)
        self.assertEqual(float(Frac(0)), 0.0)
        self.assertEqual(float(Frac(2, 1)), 2.0)


# ZADANIE 7.6
import random
import itertools

def iterator_a():
    return itertools.cycle([0, 1])

def iterator_b():
    directions = ["N", "E", "S", "W"]
    while True:
        yield random.choice(directions)

def iterator_c():
    current = 0
    while True:
        yield current
        current = (current + 1) % 7

if __name__ == '__main__':
    print("a:")
    a = iterator_a()
    i = 0
    for x in a:
        print(x)
        if i == 5: break
        i += 1

    print("\nb:")
    b = iterator_b()
    i = 0
    for x in b:
        print(x)
        if i == 5: break
        i += 1

    print("\nc:")
    c = iterator_c()
    i = 0
    for x in c:
        print(x)
        if i == 10: break
        i += 1


    unittest.main()
