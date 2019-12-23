from .util import getinput
import doctest
import re
from collections import namedtuple

def pos(v, tFly, tRest, t):
    """
    >>> pos(14, 10, 127, 1000)
    1120
    >>> pos(16, 11, 162, 1000)
    1056
    """
    n, rem = divmod(t, tFly + tRest)
    return (tFly * n + min(rem, tFly)) * v

def p1(s):
    def parse(l):
        return pos(*map(int, re.findall('\d+', l)), 2503)
    return max(parse(l) for l in s.strip().splitlines())


class Deer():
    def __init__(self, v, tf, tr):
        self.v = v
        self.tf = tf
        self.tr = tr
        self.point = 0
        self.pos = 0
        self.flying = True
        self.cd = tf

    def advance(self):
        if self.flying:
            self.pos += self.v
        
        self.cd -= 1
        if self.cd == 0:
            self.flying ^= 1
            self.cd = self.tf if self.flying else self.tr
        
test = """
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
"""

def p2(s, t):
    """
    >>> p2(test, 1000)
    689
    """

    deers = []
    for l in s.strip().splitlines():
        v, tf, tr = map(int, re.findall('\d+', l))
        deers.append(Deer(v, tf, tr))
    
    for _ in range(t):
        for deer in deers:
            deer.advance()
        maxpos = max(deer.pos for deer in deers)
        for deer in deers:
            if deer.pos == maxpos:
                deer.point += 1
    return max(deer.point for deer in deers)



doctest.testmod()
s = getinput(14)
print(p1(s))
print(p2(s, 2503))
