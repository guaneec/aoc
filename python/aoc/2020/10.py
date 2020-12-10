from .util import getinput
from collections import Counter

s = getinput(10)

a = [int(x) for x in s.splitlines()]
a.append(0)
a.append(max(a)+3)
a = sorted(a)

c = Counter([y-x for x, y in zip(a, a[1:])])
print(c[3] * c[1])

def g():
    p, q, r = 1, 0, 0
    for i in reversed(range(max(a)-3)):
        p, q, r = p + q + r if i in a else 0, p, q
    return p

print(g())