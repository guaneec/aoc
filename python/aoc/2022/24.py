from .util import getinput
from itertools import count
s = getinput(24)
m = len(s.splitlines())
n = len(s.splitlines()[0])
i0, i1 = 0, m-1
blizzards = []
for i, l in enumerate(s.splitlines()):
    for j, c in enumerate(l):
        if c == '.':
            if i == i0:
                j0 = j
            if i == i1:
                j1 = j
        elif c in '^v<>':
            blizzards.append((i, j, (c == 'v') - (c == '^'), (c == '>') - (c == '<')))
z0 = (i0, j0)
z1 = (i1, j1)

def f(t0, start, end):
    q = {start}
    for t in count(t0):
        assert q
        blocked = {
            (1+(i-1+(t+1)*di)%(m-2), 1+(j-1+(t+1)*dj)%(n-2))
            for i, j, di, dj in blizzards
        }
        qq = []
        for i, j in q:
            if (i, j) == end:
                return t
            for ii, jj in ((i, j), (i+1,j), (i-1, j), (i, j+1), (i, j-1)):
                if (ii, jj) in (start, end) or (0 < ii < m-1 and 0 < jj < n-1 and (ii, jj) not in blocked):
                    qq.append((ii, jj))
        q = set(qq)
t1 = f(0, z0, z1)
print(t1)
t2 = f(t1, z1, z0)
t3 = f(t2, z0, z1)
print(t3)