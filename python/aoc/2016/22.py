from .util import getinput
from collections import namedtuple
import re
import numpy as np
from ..aoc import find_inc, astar
from pprint import pprint

s = getinput(22)

Node = namedtuple('Node', 'x y size used avail'.split())

nodes = []
for l in s.strip().splitlines():
    if g := re.match(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+\d+%', l):
        nodes.append(Node(*map(int, g.group(1,2,3,4,5))))

n = len(nodes)
by_avail = list(sorted(nodes, key=lambda x: x.avail, reverse=True))


print( sum(
    0 if node.used == 0 else
    find_inc(0, n+1,  lambda i: False if i == 0 else True if i == n + 1 else by_avail[i-1].avail < node.used ) - 1 for node in nodes) )

def p2(nodes):
    maxx = max(n.x for n in nodes)
    maxy = max(n.y for n in nodes)
    shape = (maxx + 1, maxy + 1)
    z = np.zeros(shape, dtype=int)
    used = z.copy()
    size = z.copy()
    for n in nodes:
        used[n.x, n.y] = n.used
        size[n.x, n.y] = n.size

    def nb(n):
        goal, u = n
        u = np.frombuffer(u, dtype=int).reshape(shape)
        # += x+1,y
        bf = 0
        uu = u[:-1,:] + u[1:, :]
        for x, y in zip(*np.nonzero((uu <= size[:-1,:]) & (u[1:, :] > 0))):
            uc = u.copy()
            uc[x,y] += uc[x+1, y]
            uc[x+1, y] = 0
            bf += 1
            yield ((x, y) if (x+1, y) == goal else goal, uc.data.tobytes())
        # += x-1, y
        for x, y in zip(*np.nonzero((uu <= size[1:, :]) & (u[:-1,:] > 0))):
            x += 1
            uc = u.copy()
            uc[x,y] += uc[x-1, y]
            uc[x-1, y] = 0
            bf += 1
            yield ((x, y) if (x-1, y) == goal else goal, uc.data.tobytes())
        
        uu = u[:,:-1] + u[:,1:]
        # += x, y+1
        for x, y in zip(*np.nonzero((uu <= size[:,:-1]) & (u[:,1:] > 0))):
            uc = u.copy()
            uc[x,y] += uc[x, y+1]
            uc[x, y+1] = 0
            bf += 1
            yield ((x, y) if (x, y+1) == goal else goal, uc.data.tobytes())
        # += x, y-1
        for x, y in zip(*np.nonzero((uu <= size[:,1:]) & (u[:,:-1] > 0))):
            y += 1
            uc = u.copy()
            uc[x,y] += uc[x, y-1]
            uc[x, y-1] = 0
            bf += 1
            yield ((x, y) if (x, y-1) == goal else goal, uc.data.tobytes())
    
    def nb1(n):
        for x in nb(n):
            yield 1, x

    def h(n):
        (x, y), _ = n
        return x + y

    n0 = ((maxx, 0), used.data.tobytes())
    # state = (goalpos, usedsbuf)
    for i, (d, nn) in enumerate(astar([n0], nb1, h)):
        if i % 100 == 0:
            print(i, d, nn[0])
        if nn[0] == (0, 0):
            return d

print(p2(nodes))
