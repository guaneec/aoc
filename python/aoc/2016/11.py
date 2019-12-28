from .util import getinput
from collections import defaultdict
from functools import reduce
from ..aoc import astar, ceildiv, combrange
import re


s = '''The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.'''

s = getinput(11)

def h(n):
    e, floors = n
    fn = [len(f) for f in floors[:-1]]
    m = min(i for i, f in enumerate(floors) if f)
    s = 0
    c = 0
    for f in fn:
        f, c = c + f, c + f
        s += (2 * max(1, f-1) - 1)
    return s + abs(m - e)

def parse(s):
    o = []
    for l in s.strip().splitlines():
        f = []
        for g in re.finditer(r'(\w+)-compatible microchip', l):
            f.append((g.group(1), True))
        for g in re.finditer(r'(\w+) generator', l):
            f.append((g.group(1), False))
        o.append(frozenset(f))
    return (0, tuple(o))

def safe(floor):
    return not (any(c and (t, False) not in floor for (t, c) in floor) and any(not c for (_, c) in floor))

def nb(n):
    e, floors = n
    for ee in (ee for ee in (e+1, e-1) if ee >= 0 and ee < len(floors)):
        for comb in combrange(floors[e], 1, 3):
            ffrom = floors[e] - set(comb)
            fto = floors[ee] | set(comb)
            if safe(ffrom) and safe(fto):
                yield ee, tuple(ffrom if i == e else fto if i == ee else floors[i] for i in range(len(floors)))

def nb1(n):
    for x in nb(n):
        yield 1, x

def show(n):
    e, floors = n
    return e, [[t[:2]+'GM'[c] for (t, c) in f] for f in floors]
    
def done(n):
    e, floors = n
    return not any(floors[:-1])

n = parse(s)

for d, nn in astar([n], nb1, h):
    if done(nn):
        print(d)
        break

n2 = (n[0], tuple(n[1][i] | (set() if i != 0 else set((
        ('elerium', True), ('elerium', False), ('dilithium', True), ('dilithium', False)
    ))) for i in range(len(n[1]))) )


for d, nn in astar([n2], nb1, h):
    if done(nn):
        print(d)
        break
