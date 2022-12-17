from .util import getinput
from itertools import cycle

s = getinput(17).strip()

rocks = '''####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
'''

rr = []
for g in rocks.split('\n\n'):
    r = []
    mini = 1000
    maxj = -1
    for j, l in enumerate(g.splitlines()):
        for i, c in enumerate(l):
            if c == '#':
                r.append((i, j))
                mini = min(mini, i)
                maxj = max(maxj, j)
    rr.append([(i-mini, maxj-j) for i, j in r])

tip = 0
placed = set()
it = cycle((j, 1 if c == '>' else -1) for j, c in enumerate(s))
for rock, _ in zip(cycle(rr), range(2022)):
    r = [(x, y + tip + 4) for x, y in rock]
    while True:
        j, dx = next(it)
        if not any(x + dx == 5 or x + dx == -3 or (x+dx, y) in placed  for x, y in r):
            r = [(x + dx, y) for x, y in r]
        if not any(y - 1 == 0 or (x, y-1) in placed for x, y in r):
            r = [(x, y-1) for x, y in r]
        else:
            break
    tip = max(tip, max(y for x, y in r))
    placed.update(r)
print(tip)