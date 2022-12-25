from .util import getinput
from math import prod
def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

def lcm(a, b):
    return (a * b) // gcd(a, b)

s = getinput(11)
for part in (1, 2):
    p = 1
    monks = []
    for m in s.strip().split('\n\n'):
        lines = m.splitlines()
        items = [int(x) for x in lines[1][len(' Starting items: '):].split(', ')]
        op = lines[2][len('  Operation: new = '):]
        op = eval(f'lambda old: {op}')
        d = int(lines[3].split()[-1])
        d1 = int(lines[4].split()[-1])
        d0 = int(lines[5].split()[-1])
        p = lcm(p, d)
        monks.append((items, op, d, (d0, d1)))
    c = [0] * len(monks)
    for t in range(20 if part == 1 else 10000):
        for i in range(len(monks)):
            items, op, d, dd = monks[i]
            c[i] += len(items)
            for x in items:
                x = op(x) % p
                if part == 1:
                    x = x // 3
                monks[dd[x % d == 0]][0].append(x)
            items.clear()
    print(prod(sorted(c)[-2:]))