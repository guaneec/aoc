from .util import getinput, Machine
from itertools import count
import re

s = getinput(19)
c = [int(x) for x in s.strip().split(',')]


cache = {}
def isBeam(x, y):
    if (x, y) in cache:
        return cache[(x, y)]
    m = Machine(c)
    m.iq.extend((x, y))
    m.resume()
    cache[(x, y)] = m.oq[0]
    return m.oq[0]

s = 0
for y in range(50):
    for x in range(50):
        v = isBeam(x, y)
        print(".#"[v], end='')
        s += v
    print()

print(s)


def findSquare(d):
    x0, y0 = 3,4
    while True:
        for y in count(y0):
            x1 = None
            for x in count(x0):
                v = isBeam(x, y)
                if x1 is None and v:
                    x1 = x
                if x1 is not None and not v: break
            x0 = x1
            x = x - 1
            if isBeam(x, y) and isBeam(x - (d - 1), y) and isBeam(x - (d - 1), y + (d - 1)):
                while isBeam(x - (d - 1) - 1, y) and isBeam(x - (d - 1) - 1, y + (d - 1)):
                    x -= 1
                return (x - (d - 1), y)
            


print(findSquare(100))
