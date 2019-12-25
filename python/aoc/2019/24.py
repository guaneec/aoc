from .util import getinput
from ..aoc import rep
import doctest
from itertools import product

def adj4(xy):
    x, y = xy
    return [
        (x, y+1),
        (x, y-1),
        (x+1, y),
        (x-1, y),
    ]

def adj4r(xyd):
    x, y, d = xyd
    o = [(x,y,d) for (x,y) in adj4((x,y)) if 0 <= x < 5 and 0 <= y < 5 and (x,y) != (2, 2)]
    if abs(x-2) == 1 and y == 2:
        o.extend((2*x-2,yy,d+1) for yy in range(5))
    elif x in (0, 4):
        o.append((1+x//2, 2, d-1))
    if abs(y-2) == 1 and x == 2:
        o.extend((xx,2*y-2,d+1) for xx in range(5))
    elif y in (0, 4):
        o.append((2, 1+y//2, d-1))
    return o


def coords(board):
    s = set()
    for y, l in enumerate(board.strip().splitlines()):
        for x, c in enumerate(l):
            if c == '#':
                s.add((x, y))
    return s

test = coords("""
....#
#..#.
#..##
..#..
#....
""")
test1 = coords("""
#..#.
####.
###.#
##.##
.##..
""")
test2 = coords("""
#####
....#
....#
...#.
#.###
""")
test3 = coords("""
#....
####.
...##
#.##.
.##.#

""")
test4 = coords("""
####.
....#
##..#
.....
##...
""")


def step(lights, n):
    """
    >>> step(test, 5) == test1
    True
    >>> step(test1, 5) == test2
    True
    >>> step(test2, 5) == test3
    True
    >>> step(test3, 5) == test4
    True
    """
    lnew = set()
    for xy in product(range(n), range(n)):
        if (xy in lights and sum(z in lights for z in adj4(xy)) == 1
            or xy not in lights and sum(z in lights for z in adj4(xy)) in (1, 2)
            ):
            lnew.add(xy)
    return lnew

def stepr(bugs):
    dmin = min(b[2] for b in bugs)
    dmax = max(b[2] for b in bugs)
    o = set()
    for xyd in product(range(n), range(n),range(dmin-1, dmax+2)):
        if xyd[:2] != (2,2) and (xyd in bugs and sum(z in bugs for z in adj4r(xyd)) == 1
            or xyd not in bugs and sum(z in bugs for z in adj4r(xyd)) in (1, 2)
            ):
            o.add(xyd)

    return o

def p1(bugs, n):
    """
    >>> p1(test, 5)
    2129920
    """
    s = rep( lambda x: step(x, 5), bugs, frozenset )
    return sum( 2**(y*n+x) for (x, y) in s )

s = getinput(24)

bugs = coords(s)
n = len(s.splitlines()[0])
print(p1(bugs, n))

bugs = {(*xy, 0) for xy in bugs}
for _ in range(200):
    bugs = stepr(bugs)
print(len(bugs))

