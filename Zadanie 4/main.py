# ZADANIE 4.2
def make_ruler(n):
    ruler = ''
    numbers = ''
    result = ''
    if n <= 0:
        raise ValueError('N <= 0')

    for _ in range(n):
        ruler += '|....'
    ruler += '|'

    for i in range(n + 1):
        numbers += str(i)
        if i != n:
            for i in range(5-len(str(i + 1))):
                numbers += ' '

    result += ruler + '\n' + numbers
    return result 

def make_grid(rows, cols):
    if rows <= 0 or cols <= 0:
        raise ValueError('rows or cols <= 0')
    row = ('+' + '---') * cols + '+\n' + ('|' + '   ') * cols + '|\n'
    grid = row * rows + ('+' + '---') * cols + '+'
    return grid


print(make_ruler(12))
print(make_grid(2,4))


# ZADANIE 4.3
def factorial(n):
    if n < 0:
        raise ValueError("n < 0")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print(factorial(0))
print(factorial(1))
print(factorial(3))
print(factorial(5))

# ZADANIE 4.4
def fibonacci(n):
    if n < 0:
        raise ValueError("n < 0")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(fibonacci(0))
print(fibonacci(1))
print(fibonacci(2))
print(fibonacci(3))
print(fibonacci(4))

# ZADANIE 4.5
def reverse_iterative(L, left, right):
    if not (0 <= left <= right < len(L)):
        raise ValueError("0 <= left <= right < len(L) failed")
    while left < right:
        L[left], L[right] = L[right], L[left]
        left += 1
        right -= 1


def reverse_recursive(L, left, right):
    if not (0 <= left <= right < len(L)):
        raise ValueError("0 <= left <= right < len(L) failed")
    if left >= right:
        return
    L[left], L[right] = L[right], L[left]
    reverse_recursive(L, left + 1, right - 1)

list_a = [1,2,3,4,5,6,7,8,9]
reverse_iterative(list_a, 1, 7)
print(list_a)

list_b = [1,2,3,4,5,6,7,8,9]
reverse_recursive(list_b, 1, 7)
print(list_b)

# ZADANIE 4.6
def sum_seq(sequence):
    total = 0
    for item in sequence:
        if isinstance(item, (list, tuple)):
            total += sum_seq(item)
        elif isinstance(item, (int, float)):
            total += item
        else:
            raise ValueError("invalid type of element: ", item)
    return total

seq = [
        1, 2, 3,
        (4, 5),
        6,
        [(7, 8, 9), (10, 11, 12), (13, 14, 15)]
]
print(sum_seq(seq))

# ZADANIE 4.7
def flatten(sequence):
    result = []
    for item in sequence:
        if isinstance(item, (list, tuple)):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result
print(flatten(seq))
