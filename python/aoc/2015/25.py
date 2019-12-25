from .util import getinput
import doctest
import re


def a(n):
    return 20151125*pow(252533, n-1, 33554393) % 33554393

def xy2n(x, y):
    z = x + y - 2
    return z * (z + 1) // 2 + x

doctest.testmod()
s = getinput(25)
y, x = map(int, re.findall(r'\d+', s))
print(a(xy2n(x, y)))
