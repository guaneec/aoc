from collections import deque, defaultdict
from .util import getinput
from ..aoc import bfs, dij
from itertools import groupby
import numpy as np


join = ''.join

s = getinput(20)


class Maze:
    def __init__(self, s):
        ls = np.array([list(l) for l in s.splitlines()])
        y = 0
        chunks = lambda l: sum(1 for _ in groupby(l, lambda c: c in '.#'))
        while chunks(ls[y]) == 1:
            y += 1
        y1o = y
        while chunks(ls[y]) == 3:
            y += 1
        y1i = y
        while chunks(ls[y]) == 5:
            y += 1
        y2i = y
        while chunks(ls[y]) == 3:
            y += 1
        y2o = y
        x = 0
        while chunks(ls[:,x]) == 1:
            x += 1
        x1o = x
        while chunks(ls[:,x]) == 3:
            x += 1
        x1i = x
        while chunks(ls[:,x]) == 5:
            x += 1
        x2i = x
        while chunks(ls[:,x]) == 3:
            x += 1
        x2o = x

        portals = defaultdict(list)
        for y, dy, dd in ((y1o-2, 2, 1), (y1i, -1, -1), (y2i-2, 2, -1), (y2o, -1, 1)):
            for x, cs in enumerate(ls[y:y+2,:].T):
                ss = join(cs)
                if ss.isalpha():
                    yx = (y+dy, x)
                    if ss == 'AA':
                        self.aa = yx
                    elif ss == 'ZZ':
                        self.zz = yx
                    else:
                        portals[ss].append((yx, dd))
        
        for x, dx, dd in ((x1o-2, 2, 1), (x1i, -1, -1), (x2i-2, 2, -1), (x2o, -1, 1)):
            for y, cs in enumerate(ls[:,x:x+2]):
                ss = join(cs)
                if ss.isalpha():
                    yx = (y, x+dx)
                    if ss == 'AA':
                        self.aa = yx
                    elif ss == 'ZZ':
                        self.zz = yx
                    else:
                        portals[ss].append((yx, dd))
        pt = {}
        for a, b in portals.values():
            ac, ad = a
            bc, bd = b
            pt[ac] = b
            pt[bc] = a

        self.a = ls
        self.x1i = x1i
        self.x1o = x1o
        self.y1i = y1i
        self.y1o = y1o
        self.x2i = x2i
        self.x2o = x2o
        self.y2i = y2i
        self.y2o = y2o
        self.portals = pt
        self.cache = {}

    def neighbors(self, yx, port=True):
        y, x = yx
        l = [ (yy,xx) for (yy, xx) in [
            (y-1, x),
            (y+1, x),
            (y, x-1),
            (y, x+1),
        ] if self.a[yy, xx] == '.' ]
        if port and (y, x) in self.portals:
            l.append(self.portals[(y, x)][0])
        return l

    def neighborsR(self, yxd):
        yx, depth = yxd

        if yx not in self.cache:
            dists = {}
            for (d, yx_) in bfs([yx], lambda yx: self.neighbors(yx, False)):
                if yx_ != yx and yx_ in self.portals or yx_ == self.zz:
                    dists[yx_] = d
            self.cache[yx] = dists
        out = [(v, (k, depth)) for (k, v) in self.cache[yx].items()]
        if yx in self.portals:
            c, dd = self.portals[yx]
            if depth + dd >= 0:
                out.append((1, (c, depth + dd)))
        
        return out

    def solve(self):
        for (d, yx) in bfs([self.aa], self.neighbors):
            if yx == self.zz:
                return d
    
    def solveR(self):
        for (dist, yxd) in dij([(self.aa, 0)], self.neighborsR):
            if yxd == (self.zz, 0):
                return dist


m = Maze(s)
print(m.solve())
print(m.solveR())
