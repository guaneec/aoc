from .util import getinput
from heapq import *


s = getinput(15)

g = [[int(c) for c in l] for l in s.splitlines()]

def expand(g):
    gg = []
    for l in g:
        ll = l.copy()
        for i in range(4):
            ll += [(x + i) % 9 + 1 for x in l]
        gg.append(ll)
    ggg = gg.copy()
    for i in range(4):
        for l in gg:
            ggg.append([(x + i) % 9 + 1 for x in l])
    return ggg


def solve(g):
    m = len(g)
    n = len(g[0])
    q = [(0, (0, 0))]
    visited = {(0, 0)}
    while True:
        c, (x, y) = heappop(q)
        if (x, y) == (m - 1, n - 1):
            return c
        for xx, yy in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            if 0 <= xx < m and 0 <= yy < n and (xx, yy) not in visited:
                visited.add((xx, yy))
                heappush(q, (c + g[xx][yy], (xx, yy)))

print(solve(g))
g = expand(g)
print(solve(g))