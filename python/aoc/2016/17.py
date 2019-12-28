from .util import getinput
from hashlib import md5
from ..aoc import astar, adj4

def mymd5(s):
    return md5(bytes(s, 'utf-8')).hexdigest()

def go(d, xy):
    x, y = xy
    dx, dy = {
        'U': (0, -1),
        'D': (0, 1),
        'L': (-1, 0),
        'R': (1, 0),
    }[d]
    return x + dx, y + dy

def nb(n):
    code, xy = n
    if xy == (3, 3):
        return []
    h = mymd5(code)
    return filter(lambda z:  0 <= z[1][0] <= 3 and 0 <= z[1][1] <= 3, 
        ((code+d, go(d, xy)) for c, d in zip(h, 'UDLR') if c in 'bcdef'))

def nb1(n):
    return ((1, x) for x in nb(n))

def h(n):
    _, (x, y) = n
    return 6 - x - y

l = None
s = getinput(17).strip()
for d, n in astar( [(s, (0, 0))], nb1, h ):
    if n[1] == (3, 3):
        o = n[0][len(s):]
        if l is None:
            print(o)
        l = len(o) 
print(l)
