from .util import getinput

s = getinput(20)
a = list(map(int, s.splitlines()))
n = len(a)

class Node:
    def __init__(self,v: int) -> None:
        self.next = None
        self.prev = None
        self.v = v
    
    def movefront(self):
        n = self.next
        n.next.prev = self
        self.prev.next = n
        self.next = n.next
        n.prev = self.prev
        self.prev = n
        n.next = self
    
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
            for _ in range(x.v % (n-1)):
                x.movefront()
    def disp():
        a = [0]
        it  = n0.next
        while it != n0:
            a.append(it.v)
            it = it.next
        return a
    d = disp()
    print(d[1000%n] + d[2000%n]  + d[3000%n])
