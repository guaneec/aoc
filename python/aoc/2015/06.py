from .util import getinput
import doctest
import numpy as np
import re

def p1(s):
    """
    >>> p1('turn on 0,0 through 999,999')
    1000000
    >>> p1('toggle 0,0 through 999,0')
    1000
    >>> p1('turn on 0,0 through 999,999\\nturn off 499,499 through 500,500')
    999996
    """
    a = np.zeros((1000, 1000), dtype=bool)
    for l in s.strip().splitlines():
        x1, y1, x2, y2 = map(int, re.findall(r'\d+', l))
        if "turn on" in l:
            a[x1:x2+1, y1:y2+1] = 1
        elif "toggle" in l:
            a[x1:x2+1, y1:y2+1] = np.logical_not(a[x1:x2+1, y1:y2+1])
        else:
            assert "turn off" in l
            a[x1:x2+1, y1:y2+1] = 0
    return np.sum(a)


def p2(s):
    """
    >>> p2('turn on 0,0 through 0,0')
    1
    >>> p2('toggle on 0,0 through 999,999')
    2000000
    """
    a = np.zeros((1000, 1000), dtype=int)
    for l in s.strip().splitlines():
        x1, y1, x2, y2 = map(int, re.findall(r'\d+', l))
        if "turn on" in l:
            a[x1:x2+1, y1:y2+1] += 1
        elif "toggle" in l:
            a[x1:x2+1, y1:y2+1] += 2
        else:
            assert "turn off" in l
            a[x1:x2+1, y1:y2+1] = np.maximum(0, a[x1:x2+1, y1:y2+1]-1)
    return np.sum(a)


doctest.testmod()
s = getinput(6)
print(p1(s))
print(p2(s))

