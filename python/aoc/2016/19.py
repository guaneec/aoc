from .util import getinput
from numpy import base_repr

n = int(getinput(19))
print(int(bin(n)[3:]+"1", 2))


def p2(n):
    n3 = base_repr(n, 3)
    x = 3 ** (len(n3)-1)
    if n3[0] == '1':
        return x if x == n else n - x
    if n3[0] == '2':
        x = 3 ** (len(n3)-1)
        return 2 * n - 3 * x

print(p2(n))
