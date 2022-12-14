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

def drop2(a, b):
    if b == floor or b in g[a]:
        return 0
    o = drop2(a, b+1) + drop2(a-1, b+1) + drop2(a+1, b+1)
    g[a].add(b)
    return o + 1

def drop1(a, b):
    if b == floor - 1:
        return 0, True
    if b in g[a]:
        return 0, False
    g[a].add(b)
    o = 0
    for x, leaks in (drop1(aa, b+1) for aa in (a, a-1, a+1)):
        o += x
        if leaks:
            return o, True
    return o + 1, False

gt = deepcopy(g)
print(drop1(500, 0)[0])
g = gt
print(drop2(500, 0))