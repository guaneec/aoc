from .util import getinput
import doctest
from collections import Counter
from itertools import combinations, product, chain
from ..aoc import combrange
import numpy as np
import re


def ceildiv(a, b):
    return (a + b - 1) // b

# hp atk def
def wins(player, boss):
    """
    >>> wins( (8, 5 ,5), (12, 7, 2) )
    True
    """
    ph, pa, pd = player
    bh, ba, bd = boss
    pt = ceildiv(bh, max(1, pa - bd))
    bt = ceildiv(ph, max(1, ba - pd))
    return pt <= bt

store = np.array([ np.array([z[-3:] for z in (np.array([int(i) for i in re.findall(r'\d+', l)]) for l in  x.strip().splitlines()) if len(z)]) for x in '''
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
'''.strip().split('\n\n')])

def storeiter(store, ns):
    return (np.array(sum(sum(x) for x in z)) for z in product(*(combrange(cat, nmin, nmax) for (nmin, nmax), cat in zip(ns, store))))

doctest.testmod()
s = getinput(21)

boss = [int(x) for x in re.findall(r'\d+', s)]

def p1():
    for cost, dmg, arm in sorted(storeiter(store, [(1,2), (0,2), (0,3)]), key=lambda x: x[0]):
        if wins((100, dmg, arm), boss):
            return cost
        
def p2():
    for cost, dmg, arm in sorted(storeiter(store, [(1,2), (0,2), (0,3)]), key=lambda x: x[0], reverse=True):
        if not wins((100, dmg, arm), boss):
            return cost

print(p1())
print(p2())
