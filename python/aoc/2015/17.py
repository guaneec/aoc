from .util import getinput
import doctest
from collections import Counter

def p1(sizes, vol):
    """
    >>> p1([20, 15, 10, 5, 5], 25)
    4
    """
    if vol < 0:
        return 0
    if len(sizes) == 1:
        return vol == sizes[0] or not vol
    return p1(sizes[1:], vol-sizes[0]) + p1(sizes[1:], vol)


def p2(sizes, vol):
    """
    >>> p2([20, 15, 10, 5, 5], 25)
    3
    """
    def p2a(sizes, vol):
        if vol < 0:
            return Counter()
        if len(sizes) == 1:
            if vol == sizes[0]:
                return Counter({1: 1})
            if not vol:
                return Counter({0: 1})
            return Counter()
        return Counter({
            k+1: v for k, v in p2a(sizes[1:], vol-sizes[0]).items()
        }) + p2a(sizes[1:], vol)
    c = p2a(sizes, vol)
    return c[min(c)]

doctest.testmod()
s = getinput(17)
sizes = [int(x) for x in s.strip().splitlines()]
print( p1(sizes, 150) )
print( p2(sizes, 150) )
