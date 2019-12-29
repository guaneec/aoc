from .util import getinput
import re
from itertools import chain, groupby

s = getinput(20)

bl = [list(map(int, re.findall(r'\d+', l))) for l in s.strip().splitlines()]
eps = sorted(chain(
    ((x[0], 1) for x in bl),
    ((x[1]+1, -1) for x in bl),
    [(0, -1), (4294967296, 1)]
))

def p1(eps):
    lvl = 1
    for g in groupby(eps, lambda x: x[0]):
        lvl += sum(x[1] for x in g[1])
        if lvl == 0:
            return g[0]

def p2(eps):
    lvl = 1
    prev = None
    o = 0
    for g in groupby(eps, lambda x: x[0]):
        tmp = lvl
        lvl += sum(x[1] for x in g[1])
        if lvl > 0 and tmp == 0:
            o += g[0] - prev
        if lvl == 0:
            prev = g[0]
    return o

print(p1(eps))
print(p2(eps))
