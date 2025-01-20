########################################
# 19.1
def solve1(a, b, c):
    """Rozwiązywanie równania liniowego a x + b y + c = 0."""
    if a == 0 and b == 0:
        if c == 0:
            print("Rownanie jest tozsamosciowe.")
        else:
            print("Rownanie jest sprzeczne.")
    elif a == 0:
        print("Rownanie ma nieskończenie wiele rozwiazan: (x, -(c/b)).")
    elif b == 0:
        print("Rownanie ma nieskonczenie wiele rozwiazan: (-(c/a), y).")
    else:
        print("Rownanie ma jedno rozwiazanie:")
        print(f"x = -({b}*y+{c})/{a}")
        print(f"y = -({a}*x+{c})/{b}")

solve1(0, 0, 0)
solve1(1, 0, 0)
solve1(0, 1, 0)
solve1(0, 0, 1)
solve1(0, 1, 1)
solve1(1, 0, 1)
solve1(1, 1, 0)
solve1(1, 1, 1)


########################################
# 19.3
import random

def calc_pi(n=100):
    """Obliczanie liczby pi metodą Monte Carlo.
    n oznacza liczbę losowanych punktów."""
    inside = 0

    for _ in range(n):
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            inside += 1
    return (inside/n) * 4
print(calc_pi(100))
print(calc_pi(1_000))
print(calc_pi(10_000))
print(calc_pi(100_000))
print(calc_pi(1_000_000))


########################################
# 19.4
import math

def heron(a, b, c):
    """Obliczanie pola powierzchni trójkąta za pomocą wzoru
    Herona. Długości boków trójkąta wynoszą a, b, c."""
    if a + b <= c or a + c <= b or b + c <= a:
        raise ValueError("Wartosci nie spelniaja warunku trójkata.")

    p = (a + b + c) / 2
    area = math.sqrt(p * (p - a) * (p - b) * (p - c))
    return area

print(heron(3, 4, 5) == 6)
print(heron(7, 24, 25) == 84)
