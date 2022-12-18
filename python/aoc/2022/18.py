from .util import getinput
from ..aoc import bfs

s = getinput(18).strip()
x1, x2, y1, y2, z1, z2 = 100, -1, 100, -1, 100, -1
ds = set()
for l in s.splitlines():
    x, y, z = map(int, l.split(','))
    ds.add((x, y, z))
    x1, x2 = min(x1, x-1), max(x2, x+1)
    y1, y2 = min(z1, y-1), max(y2, y+1)
    z1, z2 = min(y1, z-1), max(z2, z+1)

def adj6(p):
    x, y, z = p
    yield from [(x, y, z+1), (x, y, z-1), (x, y+1, z), (x, y-1, z), (x+1, y, z), (x-1, y, z)]
print(sum(p not in ds for x, y, z in ds for p in adj6((x, y, z))))

def nb(p):
    x, y, z = p
    for xx, yy, zz in [(x, y, z+1), (x, y, z-1), (x, y+1, z), (x, y-1, z), (x+1, y, z), (x-1, y, z)]:
        if x1 <= xx <= x2 and y1 <= yy <= y2 and z1 <= zz <= z2 and (xx, yy, zz) not in ds:
            yield xx, yy, zz

nb = lambda p: ((x, y, z) for x, y, z in adj6(p) if (x, y, z) not in ds and x1<=x<=x2 and y1<=y<=y2 and z1<=z<=z2)
print(sum(pp in ds for _, p in bfs([(x1, y1, z1)], nb) for pp in adj6(p)))