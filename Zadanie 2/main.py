########################################
# 2.10
line = '''
Lorem ipsum dolor sit amet
consectetur
adipiscing  elit
'''
word_count = len(line.split())
print(word_count)

########################################
#2.11
word = "Lorem"
word = "_".join(word)
print(word)

########################################
#2.12
line = '''
Lorem ipsum dolor sit amet
consectetur
adipiscing  elit
'''
words = line.split()
first_letters = ''.join([word[0] for word in words])
last_letters = ''.join([word[-1] for word in words])
print(first_letters)
print(last_letters)

########################################
#2.13
line = '''
Lorem ipsum dolor sit amet
consectetur
adipiscing  elit
'''
length = sum(len(word) for word in line.split())
print(length)

########################################
#2.14
line = '''
Lorem ipsum dolor sit amet
consectetur
adipiscing  elit
'''
word = max(line.split(), key=len)
length = len(word)
print(word)
print(length)

########################################
#2.15
L = [10, 300, 17, 90, 1, 2, 3, 4]
result = ''.join(map(str, L))
print(result)

########################################
#2.16
line = '''
Lorem ipsum dolor sit amet
consectetur GvR
adipiscing  elit
'''
line_replaced = line.replace("GvR", "Guido van Rossum")
print(line_replaced)

########################################
#2.17
line = '''
Lorem ipsum dolor sit amet
consectetur GvR
adipiscing  elit
'''
words = line.split()
sorted_alpha = sorted(words, key=lambda s: s.lower())
sorted_len = sorted(words, key=len)
print(sorted_alpha)
print(sorted_len)

########################################
#2.18
large_number = 100230040500
zero_count = str(large_number).count('0')
print(zero_count)

########################################
#2.19
L = [1, 23, 456]
result = ''.join(str(num).zfill(3) for num in L)
print(result)
