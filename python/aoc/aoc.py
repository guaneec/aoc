from pathlib import Path
import sys
import subprocess
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any
from itertools import chain, combinations

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

rootdir = Path(__file__).parent / '../../'
def getinput(year, day):
    p = rootdir / f'data/{year}/{day:02d}.input.txt'
    if not p.is_file():
        cp = subprocess.run(f"python3 {rootdir / 'data.py'}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(cp.stdout.decode('utf-8'))
        cp.check_returncode()
    with open(p) as f:
        return f.read()

def bfs(seeds, neighbors):
    q = list(seeds)
    seen = set(seeds)
    d = 0
    while q:
        qq = []
        for n in q:
            yield d, n
            nb = list(neighbors(n))
            qq.extend(nn for nn in nb if nn not in seen)
            seen.update(nb)
            pass
        d += 1
        q = qq

def dij(seeds, neighbors):
    q = PriorityQueue()
    dists = {}
    for s in seeds:
        dists[s] = 0
        q.put_nowait(PrioritizedItem(0, s))
    
    while not q.empty():
        pi = q.get_nowait()
        d, n = pi.priority, pi.item
        yield d, n
        for nd, nn in neighbors(n):
            dNew = d + nd
            if nn in dists and dists[nn] <= dNew:
                continue
            dists[nn] = dNew
            q.put_nowait(PrioritizedItem(dNew, nn))

def ceildiv(a, b):
    return (a + b - 1) // b

def astar(seeds, neighbors, h):
    q = PriorityQueue()
    dists = {}
    for s in seeds:
        dists[s] = 0
        q.put_nowait(PrioritizedItem(h(s), s))
    
    while not q.empty():
        pi = q.get_nowait()
        n = pi.item
        g = dists[n]
        yield g, n
        for ng, nn in neighbors(n):
            gNew = g + ng
            if nn in dists and dists[nn] <= gNew:
                continue
            dists[nn] = gNew
            q.put_nowait(PrioritizedItem(gNew + h(nn), nn))
    

def rep(f, x, g=lambda x: x):
    s = set()
    while True:
        xx = g(x)
        if xx in s:
            return xx
        s.add(xx)
        x = f(x)


def combrange(p, rmin, rmax):
    return chain.from_iterable( combinations(p, r) for r in range(rmin, rmax) )


def adj4(xy):
    x, y = xy
    return [
        (x, y+1),
        (x, y-1),
        (x+1, y),
        (x-1, y),
    ]

def find_inc(l, h, pred):
    if l + 1 == h:
        return h
    m = (l + h) // 2
    return find_inc(l, m, pred) if pred(m) else find_inc(m, h, pred)
