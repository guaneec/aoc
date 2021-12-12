from .util import getinput
from collections import defaultdict, Counter

s = getinput(12)

g = defaultdict(list)

for l in s.splitlines():
    a, b = l.split('-')
    g[a].append(b)
    g[b].append(a)

def good(c, s, two, is2):
    return s.isupper() or c[s] < 1 or is2 and c[s] < 2 and not two and s != 'start'

def f(cur, seen, two, is2):
    if cur == 'end':
        return 1
    s = 0
    for b in g[cur]:
        if good(seen, b, two, is2):
            seen[b] += 1
            s += f(b, seen, two or b.islower() and seen[b] >= 2, is2)
            seen[b] -= 1
    return s

for is2 in (0, 1):
    print(f('start', Counter(['start']), False, is2))
