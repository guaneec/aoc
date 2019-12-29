from .util import getinput
from ..aoc import bfs, adj4
from itertools import permutations, chain

s = getinput(24)

paths = set()
pois = {}
poisinv = {}
mp = s.strip().splitlines()
for y, l in enumerate(mp):
    for x, c in enumerate(l):
        if c != '#': paths.add((x, y))
        if c.isdigit() :
            poisinv[(x, y)] = c
            pois[c] = ((x, y))

def nb(yx):
    yield from (z for z in adj4(yx) if z in paths)

dists = {}
for p, pxy in pois.items():
    dists[p] = {}
    for d, xy in bfs([pxy], nb):
        if xy in poisinv:
            dists[p][poisinv[xy]] = d

assert(all(len(dd) == len(pois) for dd in dists.values()))

print(min( sum( dists[a][b]  for a, b in  zip(chain(['0'], p[:-1]), p) ) for p in permutations(k for k in pois if k != '0')))
print(min( sum( dists[a][b]  for a, b in  zip(chain(['0'], p), chain(p, ['0'])) ) for p in permutations(k for k in pois if k != '0')))
