from .util import getinput
from itertools import accumulate
import doctest

d = {
    '^': 1j,
    'v': -1j,
    '<': -1,
    '>': 1,
}

def p1(s):
    """
    Unique locations

    >>> p1('>')
    2
    >>> p1('^>v<')
    4
    >>> p1('^v^v^v^v^v')
    2
    """
    return len(set(accumulate((d[c] for c in s), initial=0)))

def p2(s):
    """
    Unique locations, splitted
    >>> p2('^v')
    3
    >>> p2('^>v<')
    3
    >>> p2('^v^v^v^v^v')
    11
    """
    f = lambda s: set(accumulate((d[c] for c in s), initial=0)) 
    return len(f(s[::2]) | f(s[1::2]))

doctest.testmod()

s = getinput(3).strip()

print(p1(s))
print(p2(s))
