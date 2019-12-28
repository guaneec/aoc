from .util import getinput
from ..aoc import adj4, dij

fav = int(getinput(13))

cache = {}
def space(xy):
    if xy in cache:
        return cache[xy]
    x, y = xy
    o = sum(c == '1' for c in bin(x*x + 3*x + 2*x*y + y + y*y + fav)[2:]) % 2 == 0
    cache[xy] = o
    return o


def nb(xy):
    return [(1, (x, y)) for (x, y) in adj4(xy) if x >= 0 and y >= 0 and(space((x, y)))]

for d, xy in dij([(1,1)], nb):
    x, y = xy
    if (x, y) == (31,39):
        print(d)
        break

for i, (d, _) in enumerate(dij([(1,1)], nb)):
    if d > 50:
        print(i)
        break
