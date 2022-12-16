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

logs = defaultdict(int)
for d, node in dij([('AA', 1, tuple())], nbb):
    if node is None:
        print(ss*T-d)
        break
    elif node[1] <= 26:
        x, tx, op = node
        logs[op] = max(logs[op], ss*26-d-(26+1-tx)* sum(v for k, v in valves.items() if k not in op))

print(max(
    v1 + v2
    for k1, v1 in logs.items()
    for k2, v2 in logs.items()
    if v1 <= v2 and not any(i in k1 for i in k2)
))