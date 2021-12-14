from typing import Counter
from .util import getinput


s = getinput(14)

t, b = s.split('\n\n')

rules = {}

for l in b.splitlines():
    x, y = l.split(' -> ')
    rules[x] = y

for n in (10, 40):
    cc = Counter(a + b for a, b in zip(t, t[1:]))
    for _ in range(n):
        ccc = Counter()
        for k, v in cc.items():
            x = rules[k]
            ccc[k[0] + x] += v
            ccc[x + k[1]] += v
        cc = ccc

    c = Counter()
    for k, v in cc.items():
        c[k[0]] += v
    c[t[-1]] += 1

    print(c.most_common()[0][1] - c.most_common()[-1][1])