from .util import getinput
from typing import *
from math import *
from collections import *
from itertools import permutations, product, combinations
import numpy as np

s = getinput(19)

ss = [np.array([list(map(int, l.split(','))) for l in g.splitlines()[1:]]) for g in s.strip().split('\n\n')]

ux = np.array([1, 0, 0])
uy = np.array([0, 1, 0])
uz = np.array([0, 0, 1])
rots = [np.array([ex, ey, ez]).T for ex, ey, ez in permutations([ux, uy, uz, -ux, -uy, -uz], 3) if np.all(np.cross(ex, ey) == ez)]
thres = 12

dists = [Counter(sum(np.abs(p - q)) for p, q in combinations(ps ,2)) for ps in ss]
def common(c1, c2):
    return sum(min(c1[k], c2[k]) for k in c1)

d = {0: (np.eye(3, dtype=int), np.array([0, 0, 0]), ss[0])}
unused = [0]
n = len(ss)
beacons = {tuple(p) for p in ss[0]}
while len(d) != n:
    i = unused.pop()
    _, _, a = d[i]
    for j in range(n):
        if j in d:
            continue
        if common(dists[i], dists[j]) < thres * (thres - 1) // 2:
            continue        
        b = ss[j]
        for (a0, b0, r) in product(a, b, rots):
            # u = [r @ (p - b0) + a0 for p in b]
            u = ((r @ (b - b0).T).T + a0)
            if len(set(map(tuple, a)) & set(map(tuple, u))) >= thres:
                d[j] = (r, r @ -b0 + a0, u)
                for p in u:
                    beacons.add(tuple(p))
                unused.append(j)
                break
print(len(beacons))
l = [v[1] for v in d.values()]
print(max(sum(np.abs(a-b)) for a in l for b in l))