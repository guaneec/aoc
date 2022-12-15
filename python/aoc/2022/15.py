from .util import getinput
from collections import *
from itertools import combinations
import re

s = getinput(15)
yy = 2000000
Y = 4000000

r = re.compile(r'Sensor at x=(.+), y=(.+): closest beacon is at x=(.+), y=(.+)')

def intersect(x, y1, y2, y, x1, x2):
    if x1 <= x <= x2 and y1 <= y <= y2:
        yield x, y

def corners(u11, v11, u21, v21, u12, v12, u22, v22):
    for u in (u11, u21):
        for v in (v12, v22):
            yield from intersect(u, v11+1, v21-1, v, u12+1, u22-1)
    for v in (v11, v21):
        for u in (u12, v22):
            yield from intersect(u, v12+1, v22-1, v, u11+1, u21-1)

suvs = [] # (u1, v1, u2, v2)
z = set()

for l in s.splitlines():
    m = re.match(r, l)
    sx, sy, bx, by = map(int, m.groups())
    su, sv = sx + sy, sx - sy
    bu, bv = bx + by, bx - by
    d = abs(sx-bx) + abs(sy-by)
    dx = d - abs(sy - yy)
    for x in range(sx-dx, sx+dx+1):
        if (x, yy) != (bx, by):
            z.add(x)
    suvs.append((su-d-1, sv-d-1, su+d+1, sv+d+1))

print(len(z))

def f():
    for uv1, uv2 in combinations(suvs, 2):
        for u, v in corners(*uv1, *uv2):
            if not any(u1 < u < u2 and v1 < v < v2 for u1, v1, u2, v2 in suvs):
                x, y = (u+v) // 2, (u-v) // 2
                if (u+v) % 2 == 0 and  0 <= x <= Y and 0 <= y <= Y:
                    return x * 4000000 + y
print(f())