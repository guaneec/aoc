from .util import getinput
from collections import defaultdict, Counter

s = getinput(13)

pa, pb = s.split('\n\n')

paper = set()
for l in pa.splitlines():
    x, y = l.split(',')
    paper.add((int(x), int(y)))

def fold(paper, fx, k):
    def g(x, y):
        if not fx:
            return (x, y if y < k else 2 * k - y)
        else:
            return (x if x < k else 2 * k - x, y)
    return {g(x, y) for x, y in paper}

p1 = False
for l in pb.splitlines():
    _, _, a = l.split()
    xy, k = a.split('=')
    paper = fold(paper, xy == 'x', int(k))
    if not p1:
        p1 = True
        print(len(paper))

mx = max(x for x, y in paper)
my = max(y for x, y in paper)

for i in range(my+1):
    for j in range(mx+1):
        print('#' if (j, i) in paper else ' ', end='')
    print()