from .util import getinput
from math import prod
from itertools import takewhile, dropwhile

s = getinput(8)
a = s.splitlines()

m, n = len(a), len(a[0])
dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def toedge(i, j, di, dj):
    while True:
        i, j = i + di, j + dj
        if not 0 <= i < m or not 0 <= j < n:
            return
        yield i, j

print(sum(
    any(all(a[ii][jj] < a[i][j] for ii, jj in toedge(i, j, di, dj)) for di, dj in dirs)
    for i in range(m) for j in range(n)
))

print(max(
    prod(
        sum(1 for _ in takewhile(lambda p: a[i][j] > a[p[0]][p[1]], toedge(i, j, di, dj)))
        + any(True for _ in dropwhile(lambda p: a[i][j] > a[p[0]][p[1]], toedge(i, j, di, dj)))
        for di, dj in dirs
    )
    for i in range(m) for j in range(n)
))