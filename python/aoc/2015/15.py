from .util import getinput
import doctest
import re
import numpy as np
from functools import reduce


def foo(ings, n):
    if not ings:
        yield 0
    else:
        for i in range(n+1):
            for res in foo(ings[1:], i):
                yield (n-i) * ings[0] + res

def score(arr):
    return 0 if any(arr[:-1] <= 0) else np.product(arr[:-1])




def parseIngs(s):
    return [
        np.array([int(x) for x in re.findall(r'-?\d+', l)])
        for l in s.strip().splitlines()
    ]


test = parseIngs('''
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
''')

def maxscore(ings, cal=None):
    """
    >>> maxscore(test)
    62842880
    >>> maxscore(test, 500)
    57600000
    """
    return max(score(res) for res in foo(ings, 100) if cal is None or res[-1] == 500)


doctest.testmod()
s = getinput(15)
print(maxscore(parseIngs(s)))
print(maxscore(parseIngs(s), 500))
