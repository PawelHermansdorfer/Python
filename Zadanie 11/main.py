
class Node:
    def __init__(self, value, next_node):
        self.value = value
        self.next = next_node

    def __str__(self):
        return str(self.value)

class SingleList:
    """Klasa reprezentująca całą listę jednokierunkową."""
    def __init__(self):
        self.length = 0
        self.head = None
        self.tail = None

    def empty(self):
        return self.length == 0

    def count(self):
        return self.length

    def __len__(self):
        return self.length

    def push_front(self, value):
        if self.length == 0:
            self.head = self.tail = Node(value, None)
        else:
            self.head = Node(value, self.head)
        self.length += 1

    def push_back(self, value):
        if self.head:
            self.tail.next = Node(value, None)
            self.tail = self.tail.next
        else:
            self.head = self.tail = Node(value, None)
        self.length += 1

    def pop_front(self):
        if self.length == 0:
            raise ValueError
        node = self.head
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
        self.length -= 1
        node.next = None
        return(node)

    def __str__(self):
        l = []
        node = self.head
        while node:
            l.append(node.value)
            node = node.next
        return str(l)

    def __eq__(self, other):
        result = True
        if type(other) == list:
            if len(other) == self.length:
                node = self.head
                for i in range(self.length):
                    if node.value != other[i]:
                        return False
                    node = node.next
            else:
                result = False
        return result 

    def remove_tail(self):
        if self.length == 0:
            raise ValueError
        node = self.tail
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            new_tail = self.head
            while new_tail.next != self.tail:
                new_tail = new_tail.next
            self.tail = new_tail
        self.length -= 1
        node.next = None
        return node

    def join(self, other):
        while not other.empty():
            self.push_back(other.pop_front().value)

    def clear(self):
        while not self.empty():
            self.pop_front()


l = SingleList()
assert l.empty()
assert len(l) == 0
assert l == []

for i in range(5, 0, -1):
    l.push_front(i)
assert l == [1, 2, 3, 4, 5]
assert len(l) == 5


for i in range(6, 11):
    l.push_back(i)
assert l == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
assert len(l) == 10

for i in range(5):
    assert l.pop_front().value == (1 + i)
assert l == [6, 7, 8, 9, 10]
assert len(l) == 5

for i in range(5):
    assert l.remove_tail().value == (10 - i)
assert l == []
assert len(l) == 0
assert l.empty()

l1 = SingleList()
for i in range(5, 0, -1):
    l1.push_front(i)

l2 = SingleList()
for i in range(6, 11):
    l2.push_back(i)

l1.join(l2)
assert l1 == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
assert l2 == []

l1.clear()
assert l1 == []
