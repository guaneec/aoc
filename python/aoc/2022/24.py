from .util import getinput
from ..aoc import astar, bfs
s = getinput(24)
m = len(s.splitlines())
n = len(s.splitlines()[0])
i0, i1 = 0, m-1
lefts, rights, downs, ups = [], [], [], []
for i, l in enumerate(s.splitlines()):
    for j, c in enumerate(l):
        if c == '.':
            if i == i0:
                j0 = j
            if i == i1:
                j1 = j
        if c == '>': rights.append((i, j))
        if c == '<': lefts.append((i, j))
        if c == 'v': downs.append((i, j))
        if c == '^': ups.append((i, j))
z0 = (i0, j0)
z1 = (i1, j1)
cache = [set([*lefts, *rights, *downs, *ups])]
def f(t):
    global lefts, rights, downs, ups
    if t < len(cache):
        return cache[t]
    assert t == len(cache)
    ups = [(1+(ii-1+m-2-1)%(m-2), jj) for ii, jj in ups ]
    downs = [(1+(ii-1+m-2+1)%(m-2), jj) for ii, jj in downs ]
    lefts = [(ii, 1+(jj-1+n-2-1)%(n-2)) for ii, jj in lefts ]
    rights = [(ii, 1+(jj-1+n-2+1)%(n-2)) for ii, jj in rights ]
    cache.append(set([*lefts, *rights, *downs, *ups]))
    return cache[-1]

def nb(zt):
    z, t = zt
    i, j = z
    assert t < 2000
    yield from [(((ii, jj), t+1)) for ii, jj in (
        (i, j), (i+1,j), (i-1, j), (i, j+1), (i, j-1)
    ) if (ii, jj ) in (z0, z1) or (0 < ii < m-1 and 0 < jj < n-1 and (ii, jj ) not in f(t+1))]

for d, nn in bfs([(z0, 0)], nb):
    if nn[0] == z1:
        print(d)
        break

def nb(zt):
    z, t, cps = zt
    i, j = z
    assert t < 2000
    yield from [(((ii, jj), t+1, cps + (z == (z1, z0)[cps % 2]))) for ii, jj in (
        (i, j), (i+1,j), (i-1, j), (i, j+1), (i, j-1)
    ) if (ii, jj ) in (z0, z1) or (0 < ii < m-1 and 0 < jj < n-1 and (ii, jj ) not in f(t+1))]

for d, nn in bfs([(z0, 0, 0)], nb):
    if nn[-1] == 2 and nn[0] == z1:
        print(d)
        break