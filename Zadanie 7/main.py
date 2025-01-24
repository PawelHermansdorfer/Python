# ZADANIE 7.1






# ZADANIE 7.6
import itertools
import random


def iterator_a():
    i = 0
    while True:
        yield i % 2
        i += 1

def iterator_b():
    directions = ["N", "E", "S", "W"]
    while True:
        yield random.choice(directions)

def iterator_c():
    current = 0
    while True:
        yield current
        current = (current + 1) % 7

# Testowanie iteratorów
print("a:")
a = iterator_a()
i = 0
for x in a:
    print(x)
    if i == 5: break
    i += 1

# Test iteratora (b)
print("\nb:")
b = iterator_b()
i = 0
for x in b:
    print(x)
    if i == 5: break
    i += 1

# Test iteratora (c)
print("\nc:")
c = iterator_c()
i = 0
for x in c:
    print(x)
    if i == 10: break
    i += 1
