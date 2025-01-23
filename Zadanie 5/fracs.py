from math import gcd

def simplify(frac):
    top, bottom = frac
    c = gcd(top, bottom)
    return [top // c, bottom // c]

def add_frac(frac1, frac2):
    top = frac1[0] * frac2[1] + frac2[0] * frac1[1]
    bottom = frac1[1] * frac2[1]
    return simplify([top, bottom])

def sub_frac(frac1, frac2):
    top = frac1[0] * frac2[1] - frac2[0] * frac1[1]
    bottom = frac1[1] * frac2[1]
    return simplify([top, bottom])

def mul_frac(frac1, frac2):
    top = frac1[0] * frac2[0]
    bottom = frac1[1] * frac2[1]
    return simplify([top, bottom])

def div_frac(frac1, frac2):
    if frac2[0] == 0:
        raise ZeroDivisionError("division by zero.")
    top = frac1[0] * frac2[1]
    bottom = frac1[1] * frac2[0]
    return simplify([top, bottom])

def is_positive(frac):
    return frac[0] * frac[1] > 0

def is_zero(frac):
    return frac[0] == 0

def cmp_frac(frac1, frac2):
    diff = sub_frac(frac1, frac2)
    if diff[0] > 0:
        return 1
    elif diff[0] < 0:
        return -1
    return 0

def frac2float(frac):
    return frac[0] / frac[1]

