from .util import getinput
from collections import Counter, defaultdict
s = getinput(6)

xs = [int(x) for x in  s.split(',')]

def solve(xs, n):
    d = Counter(xs)
    for _ in range(n):
        d = defaultdict(int, {k - 1: v for k, v in d.items()})
        d[8] = d[-1]
        d[6] += d[-1]
        del(d[-1])
    return sum(d.values())

print(solve(xs, 80))
print(solve(xs, 256))