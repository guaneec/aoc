from .util import getinput
from math import ceil
from functools import reduce

s = """\
939
7,13,x,x,59,x,31,19
"""
s = getinput(13)

a, b = s.splitlines()
a = int(a)
p = [(int(x), i) for i, x in enumerate(b.split(",")) if x != "x"]
b = [int(x) for x in b.split(",") if x != "x"]

t, i = min(((ceil(a / x) * x, x) for x in b), key=lambda a: a[0])
print((t - a) * i)

prod = lambda a: reduce(lambda p, q: p * q, a, 1)

P = prod(x[0] for x in p)
q2 = sum(P // q * pow(P // q, -1, q) * ((q - c) % q) for q, c in p) % P
print(q2)
