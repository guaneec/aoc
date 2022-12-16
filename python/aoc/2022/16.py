from .util import getinput
from collections import *
from itertools import combinations
import re
from functools import cache
from ..aoc import bfs

s = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''
s = getinput(16)

r = r'Valve (.+) has flow rate=(.+); tunnels? leads? to valves? (.+)'

valves = {}
paths = {}
for l in s.splitlines():
    m = re.match(r, l)
    a = m.group(1)
    x = int(m.group(2))
    b = m.group(3).split(', ')
    print(a, b, x)
    valves[a] = x
    paths[a] = b

T = 26

@cache
def f(x, t, op, s1):
    print(x, t, op, s1)
    if t == T:
        return s1
    z = []
    if x not in op and valves[x] > 0:
        z.append(f(x, t+1, tuple(sorted(op + (x,))), s1+valves[x]))
    for nb in paths[x]:
        z.append(f(nb, t+1, op, s1))
    return s1 + max(z)

N = sum(x > 0 for x in valves.values())


ss = dict()
def mycache(f):
    def g(*args):
        t = tuple(args)
        if t in ss:
            return ss[t]
        o = f(*args)
        ss[t] = o
        return o
    return g

@mycache
def f(x, e, t, op, s1):
    if t == T:
        return s1
    if len(op) == N:
        return (T - t + 1) * s1
    for tt in range(1, t):
        if (x, e, tt, op, s1) in ss:
            return 0
    
    z = []
    if x not in op and valves[x] > 0:
        for nb in paths[e]:
            z.append(f(*sorted((x, nb)), t+1, tuple(sorted(op + (x,))), s1+valves[x]))
    if e not in op and valves[e] > 0:
        for nb in paths[x]:
            z.append(f(*sorted((e, nb)), t+1, tuple(sorted(op + (e,))), s1+valves[e]))
    if e not in op and valves[e] > 0 and x not in op and valves[x] > 0 and e != x:
        z.append(f(x, e, t+1, tuple(sorted(op + (e,x))), s1+valves[x]+valves[e]))
    for nb1 in paths[x]:
        for nb2 in paths[e]:
            z.append(f(*sorted((nb1, nb2)), t+1, op, s1))
    return s1 + max(z)

dd = defaultdict(dict)
for a in valves:
    if valves[a] == 0 and a != 'AA':
        continue
    for d, n in bfs([a], lambda x: paths[x]):
        if a != n and valves[n] > 0:
            dd[a][n] = d
            if a != 'AA':
                dd[n][a] = d

print(dd)


def nb(x):
    return dd[x].items()

T = 26

# t: first minute after opening, free to move
@cache
def g(x, tx, e, te, op, s1):
    if (tx, x) > (te, e):
        return g(e, te, x, tx, op, s1)
    # print(x, tx, e, te, op, s1)
    z = [(T - te + 1) * s1]
    for n, d in nb(x):
        if n in op or tx+d+1 > T or tx + d+1 < te:
            continue
        z.append(s1 * (tx+d+1-te) + g(n, tx+d+1, e, te, tuple(sorted(op + (n,))), s1 + valves[n]))
    for n, d in nb(e):
        if n in op or te+d+1 > T:
            continue
        z.append(s1 * (d+1) + g(n, te+d+1, x, tx, tuple(sorted(op + (n,))), s1 + valves[n]))
    return max(z)



# print(f('AA', 'AA', 1, tuple(), 0))
print(g('AA', 1, 'AA', 1, tuple(), 0))