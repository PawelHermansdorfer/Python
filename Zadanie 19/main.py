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

########################################
# 19.6
def dynamic_p(i, j):
    dp = [[0] * (j + 1) for _ in range(i + 1)]

    for x in range(i + 1):
        for y in range(j + 1):
            if x == 0 and y == 0:
                dp[x][y] = 0.5
            elif x > 0 and y == 0:
                dp[x][y] = 0.0
            elif x == 0 and y > 0:
                dp[x][y] = 1.0
            else:
                dp[x][y] = 0.5 * (dp[x - 1][y] + dp[x][y - 1])

    return dp[i][j]

def recursive_p(i, j):
    if i == 0 and j == 0:
        return 0.5
    elif i > 0 and j == 0:
        return 0.0
    elif i == 0 and j > 0:
        return 1.0
    else:
        return 0.5 * (recursive_p(i - 1, j) + recursive_p(i, j - 1))


i, j = 0, 0
print(f"dynamiczne P({i}, {j}) = {dynamic_p(i, j)}")
print(f"Rekurencja P({i}, {j}) = {recursive_p(i, j)}")

i, j = 10, 0
print(f"dynamiczne P({i}, {j}) = {dynamic_p(i, j)}")
print(f"Rekurencja P({i}, {j}) = {recursive_p(i, j)}")

i, j = 0, 10
print(f"dynamiczne P({i}, {j}) = {dynamic_p(i, j)}")
print(f"Rekurencja P({i}, {j}) = {recursive_p(i, j)}")

i, j = 10, 10
print(f"dynamiczne P({i}, {j}) = {dynamic_p(i, j)}")
print(f"Rekurencja P({i}, {j}) = {recursive_p(i, j)}")
