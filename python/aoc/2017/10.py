from collections import defaultdict

from .util import getinput

s = getinput(10)
ls = [int(x) for x in s.split(',')]
l = list(range(256))
cur = 0
skip = 0

def rev(a, i, j):
    n = len(a)
    c = a.copy()
    it = list((x + n) % n for x in range(i, j))
    for x, y in zip(it, reversed(it)):
        a[x] = c[y]

for le in ls:
    rev(l, cur, cur + le)
    cur = (cur + le + skip) % len(l)
    skip += 1

print(l[0]*l[1])

l = list(range(256))
cur = 0
skip = 0
cs = [ord(c) for c in s.strip()]
cs.extend([17, 31, 73, 47, 23])
for _ in range(64):
    for le in cs:
        rev(l, cur, cur + le)
        cur = (cur + le + skip) % len(l)
        skip += 1

dh = 0
for i in range(16):
    x = 0
    for j in range(16):
        x ^= l[i*16+j]
    dh = dh * 256 + x

print(hex(dh)[2:])

