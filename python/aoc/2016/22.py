from .util import getinput
from collections import namedtuple
import re
import numpy as np
from ..aoc import find_inc, astar, adj4
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
    # two chunks of data never fit in a node
    assert(sum(list(sorted(n.used for n in nodes if n.used > 0 ))[:2]) > min(n.size for n in nodes) )
    # "small" data can go anywhere
    assert(max(n.used for n in nodes if n.used < 250) < min(n.size for n in nodes))
    # exactly one cavity
    assert(sum(n.used == 0 for n in nodes) == 1)

    normal = {(n.x, n.y) for n in nodes if n.used < 250}
    
    def nb(n):
        goal, empty = n
        for c in adj4(empty):
            if c in normal:
                yield (empty if c == goal else goal), c

    def nb1(n):
        for x in nb(n):
            yield 1, x

    def h(n):
        (gx, gy), (ex, ey) = n
        return gx + gy + abs(ex - gx) + abs(ey - gy)

    n0 = (max(n.x for n in nodes if n.y == 0), 0), list((n.x, n.y) for n in nodes if n.used == 0)[0]
    for d, nn in astar([n0], nb1, h):
        if nn[0] == (0, 0):
            return d

print(p2(nodes))
