from .util import getinput
import doctest
import re
import numpy as np
from functools import reduce

target = '''
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
'''.strip()

td = { k: int(v) for (k, v) in [ re.match('^(\w+): (\d+)$', l).group(1, 2) for l in target.splitlines() ]}

def p1(s):
    for l in s.strip().splitlines():
        i, a, b, c = re.match(r'Sue (\d+): (.+), (.+), (.+)', l).group(1,2,3,4)
        if all(x in target for x in (a, b, c)):
            return int(i)
def p2(s):
    for l in s.strip().splitlines():
        i, ta, ia, tb, ib, tc, ic = re.match(r'Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)', l).group(1,2,3,4,5,6,7)
        ia, ib, ic = map(int, (ia, ib, ic))
        if all(
            td[tt] < ii if tt in ('cats', 'trees') else
            td[tt] > ii if tt in ('pomeranians', 'goldfish') else
            td[tt] == ii for (tt, ii) in (
                (ta, ia), (tb, ib), (tc, ic)
            )
        ): return i

s = getinput(16)
print(p1(s))
print(p2(s))
