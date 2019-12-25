from .util import getinput
from collections import Counter
import doctest
from functools import reduce

def foo(ws, w1, n, m=None):
    if m is None:
        m = max(ws.keys()) + 1
    if n == 0:
        return
    if w1 in ws and m > w1:
        yield (w1,)
    else:
        for w, v in sorted(ws.items(), key=lambda x: x[0], reverse=True):
            if v > 0 and w1 >= w and w < m:
                for x in foo(ws - Counter({w:1}), w1 - w, n-1, w):
                    sol = (w, *x)
                    if len(sol) < n:
                        n = len(sol)
                    if n == len(sol):
                        yield sol

# not always correct for nn > 2
def splittable(ws, nn):
    w, r = divmod(sum(ws), nn)
    if r:
        return False
    n = sum(ws.keys()) // nn
    for _ in foo(ws, w, n):
        return True
    return False

def p1(ws, nn):
    """
    >>> p1(Counter([1,2,3,4,5,7,8,9,10,11]), 3)
    99
    """
    w, r = divmod(sum(ws), nn)
    n = sum(ws.keys()) // nn
    if r:
        return None
    g1s = list(foo(ws, w, n))
    n = min(len(x) for x in g1s)
    prod = lambda x: reduce(lambda a, b: a*b, x)
    return min(prod(x) for x in g1s if len(x) == n and splittable(ws - Counter(x), nn-1))

doctest.testmod()
s = getinput(24)
ws = Counter(int(x) for x in s.strip().splitlines())
print(p1(ws, 3))
print(p1(ws, 4))
