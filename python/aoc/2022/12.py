from .util import getinput
from ..aoc import bfs

s = getinput(12)
s = s.strip().splitlines()
m = len(s)
n = len(s[0])
for i in range(m):
    for j in range(n):
        if s[i][j] == 'S':
            ps = (i, j)
        if s[i][j] =='E':
            pe = (i, j)

def h(p):
    x, y = p
    return ord(s[x][y] if s[x][y].islower() else 'a' if s[x][y] == 'S' else 'z')

def nb(p):
    x, y = p
    for xx, yy in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
        if 0 <= xx < m and 0 <= yy < n and h((xx, yy)) <= h(p) + 1:
            yield xx, yy

print(next(d for d, p in bfs([ps], nb) if p == pe))

def nb2(p):
    x, y = p
    for xx, yy in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
        if 0 <= xx < m and 0 <= yy < n and h(p) <= h((xx, yy)) + 1:
            yield xx, yy

print(next(d for d, p in bfs([pe], nb2) if h(p) == ord('a')))