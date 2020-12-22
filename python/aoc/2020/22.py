from .util import getinput
from collections import deque
from itertools import islice

s = getinput(22)

ps = []
for p in s.split("\n\n"):
    ps.append([int(l) for l in p.splitlines() if l[0] != "P"])

p1, p2 = deque(ps[0]), deque(ps[1])


def game(p1: deque, p2: deque, recurse: bool):
    """retuns p1 wins"""
    seen = set()
    while p1 and p2:
        k = (tuple(p1), tuple(p2))
        if k in seen:
            return True
        seen.add(k)
        a1 = p1.popleft()
        a2 = p2.popleft()
        if recurse and len(p1) >= a1 and len(p2) >= a2:
            g = game(deque(islice(p1, a1)), deque(islice(p2, a2)), True)
        else:
            g = a1 > a2
        if g:
            p1.append(a1)
            p1.append(a2)
        else:
            p2.append(a2)
            p2.append(a1)
    return not p2


for recurse in (False, True):
    p1c, p2c = deque(p1), deque(p2)
    game(p1c, p2c, recurse)
    p = p1c if p1c else p2c
    n = len(p)
    print(sum((n - i) * x for i, x in enumerate(p)))
