from .util import getinput
from itertools import islice

s = getinput(23)


class Node:
    def __init__(self, v):
        self.v = v
        self.next = None
        self.prev = None


class Ring:
    def __init__(self, a):
        prev = None
        first = None
        self.nodes = {}
        self.n = len(a)
        for x in a:
            n = Node(x)
            self.nodes[x] = n
            if first is None:
                first = prev
            if prev is not None:
                prev.next = n
                n.prev = prev
            prev = n
        prev.next = first
        first.prev = prev
        self.current = first

    def get(self, n):
        return self.nodes[n]

    def step(self):
        x = self.current.v
        p1, p2, p3 = (
            self.current.next.v,
            self.current.next.next.v,
            self.current.next.next.next.v,
        )

        dest = x
        while dest in (x, p1, p2, p3):
            dest = (dest + self.n - 2) % self.n + 1

        dest_node = self.get(dest)

        n1 = self.current
        n2 = self.current.next.next.next.next

        n1.next.prev = dest_node
        n2.prev.next = dest_node.next
        dest_node.next.prev = n2.prev
        dest_node.next = n1.next
        n1.next = n2
        n2.prev = n1
        self.current = n2

    def iterfrom(self, i):
        n = self.get(i)
        while n.next.v != i:
            n = n.next
            yield n.v


c = [int(x) for x in s.strip()]

r = Ring(c)
for i in range(100):
    r.step()
print("".join(str(x) for x in r.iterfrom(1)))

r = Ring(c + list(range(len(c) + 1, 1000000 + 1)))
for i in range(10000000):
    r.step()

a, b = islice(r.iterfrom(1), 2)
print(a * b)