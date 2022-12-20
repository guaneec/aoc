from .util import getinput

s = getinput(20)
a = list(map(int, s.splitlines()))
n = len(a)

class Node:
    def __init__(self,v: int) -> None:
        self.next = None
        self.prev = None
        self.v = v
    
    def movefront(self, steps):
        n = self.nextn(steps)
        if n is self:
            return
        nn = n.next
        self.prev.next = self.next
        self.next.prev = self.prev
        n.next = self
        self.prev = n
        nn.prev = self
        self.next = nn

    def nextn(self, steps):
        it = self
        for _ in range(steps):
            it = it.next
        return it
    
for mult, rounds in [(1, 1), (811589153, 10)]:
    nodes = []
    for i, x in enumerate(a):
        nodes.append(Node(x*mult))
        if x == 0:
            n0 = nodes[-1]
    for i in range(n):
        nodes[i].next = nodes[(i+1)%n]
        nodes[i].prev = nodes[(n+i-1)%n]
    for _ in range(rounds):
        for x in nodes:
            x.movefront(x.v % (n-1))
    print(sum(n0.nextn(x).v for x in (1000, 2000, 3000)))
