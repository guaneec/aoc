from .util import getinput
from collections import *
import re
from ..aoc import bfs, dij

s = getinput(16)

r = r'Valve (.+) has flow rate=(.+); tunnels? leads? to valves? (.+)'

valves = {}
paths = {}
for l in s.splitlines():
    m = re.match(r, l)
    a = m.group(1)
    x = int(m.group(2))
    b = m.group(3).split(', ')
    valves[a] = x
    paths[a] = b

dd = defaultdict(dict)
for a in valves:
    if valves[a] == 0 and a != 'AA':
        continue
    for d, n in bfs([a], lambda x: paths[x]):
        if a != n and valves[n] > 0:
            dd[a][n] = d
            if a != 'AA':
                dd[n][a] = d
def nb(x):
    return dd[x].items()

ss = sum(valves.values())

T = 30
def nbb(node):
    x, tx, op = node
    stepped = False
    l1 = sum(v for k, v in valves.items() if k not in op)
    for n, d in nb(x):
        if n in op or tx+d+1 > T:
            continue
        stepped = True
        yield (d+1) * l1, (n, tx+d+1, tuple(sorted(op + (n,))))
    if not stepped:
        yield (T-tx+1) * l1, None

for d, node in dij([('AA', 1, tuple())], nbb):
    if node is None:
        print(ss*T-d)
        break

T = 26
def nbb(node):
    x, tx, e, te, op = node
    if (tx, x) > (te, e):
        yield from nbb((e, te, x, tx, op))
        return
    stepped = False
    l1 = sum(v for k, v in valves.items() if k not in op)
    for n, d in nb(x):
        if n in op or tx+d+1 > T or tx + d+1 < te:
            continue
        stepped = True
        yield (tx+d+1-te) * l1, (n, tx+d+1, e, te, tuple(sorted(op + (n,))))
    for n, d in nb(e):
        if n in op or te+d+1 > T:
            continue
        stepped = True
        yield (d+1) * l1, (n, te+d+1, x, tx, tuple(sorted(op + (n,))))
    if not stepped:
        yield (T-te+1) * l1, None


for d, node in dij([('AA', 1, 'AA', 1, tuple())], nbb):
    if node is None:
        print(ss*T-d)
        break
