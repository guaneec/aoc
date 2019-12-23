from .util import getinput
from hashlib import md5
from itertools import count
import doctest

def nice(s):
    """
    >>> nice('ugknbfddgicrmopn')
    True
    >>> nice('aaa')
    True
    >>> nice('jchzalrnumimnmhp')
    False
    >>> nice('haegwjzuvuyypxyu')
    False
    >>> nice('dvszwmarrgswjxmb')
    False
    """

    threeV = lambda s: sum(c in 'aeiou' for c in s) >= 3
    twoRow = lambda s: any( a == b for (a, b) in zip(s, s[1:]) )
    noCon = lambda s: all(x not in s for x in ['ab', 'cd', 'pq', 'xy'])
    return threeV(s) and twoRow(s) and noCon(s)

def nice2(s):
    """
    >>> nice2('qjhvhtzxzqqjkmpb')
    True
    >>> nice2('xxyxx')
    True
    >>> nice2('uurcxstgmygtbstg')
    False
    >>> nice2('ieodomkazucvgmuy')
    False
    """

    conPair = lambda s: any( s[i:i+2] in s[i+2:] for i in range(0, len(s) - 3) )
    rep = lambda s: any(s[i] == s[i+2] for i in range(0, len(s) - 2))
    return conPair(s) and rep(s)

doctest.testmod()

ss = getinput(5).strip().splitlines()
print(sum(nice(s) for s in ss))
print(sum(nice2(s) for s in ss))

