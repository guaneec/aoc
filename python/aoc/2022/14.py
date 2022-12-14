from copy import deepcopy
from .util import getinput
from collections import defaultdict

s = getinput(14)

g = defaultdict(set)
floor = 0
for l in s.splitlines():
    pa, pb = None, None
    for x in l.split(' -> '):
        a, b = map(int, x.split(','))
        if pa is not None:
            if a == pa:
                for bb in range(min(b, pb), max(b, pb)+1):
                    g[a].add(bb)
            elif b == pb:
                for aa in range(min(a, pa), max(a, pa)+1):
                    g[aa].add(b)
            else:
                assert False
            floor = max(floor, b + 2)
        pa, pb = a, b

def drop(a, b):
    while True:
        try:
            b = min(x for x in g[a] if x >= b) - 1
        except:
            return a, floor - 1
        if b+1 not in g[a-1]:
            a, b = a-1, b+1
        elif b+1 not in g[a+1]:
            a, b = a+1, b+1
        else:
            return a, b

for part1 in (True, False):
    gt = deepcopy(g)
    t = 0
    while True:
        t += 1
        a, b = drop(500, 0)
        if (b == floor - 1 if part1 else (a, b) == (500, 0)):
            break
        g[a].add(b)
    print(t - part1)
    g = gt