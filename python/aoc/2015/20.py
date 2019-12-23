from .util import getinput
from sympy.ntheory import abundance, divisor_sigma, divisors, factorint
import doctest
from itertools import count

def p1(x):
    for i in count(x // 60):
        if 10 * divisor_sigma(i) >= x:
            return i

def p2(x):
    xx = (x + 10) // 11
    for i in count(xx // 6):
        if sum( a for a in divisors(i) if a >= i // 50 ) >= xx:
            return i

x = int(getinput(20))
print(p1(x))
print(p2(x))
