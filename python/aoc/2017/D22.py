from .util import getinput
from collections import defaultdict

ds = ((1,0), (0, -1), (-1, 0), (0,1))
di = 1

x, y = 0, 0

s = '''..#
#..
...'''

s = getinput(22)

lines = s.strip().splitlines()
n = len(lines)
off = n // 2
infected =  set(((i-off, j-off) for (j,l) in enumerate(lines) for (i, c) in enumerate(l) if c == '#' ))


WEAKENED = 0
CLEAN = 1
FLAGGED = 2
INFECTED = 3


board = defaultdict(lambda: CLEAN, { xy: INFECTED for xy in infected })

bi = 0

for _ in range(10000):
    if (x, y) in infected:
        di = (di - 1) % 4
        infected.remove((x,y))
    else:
        di = (di + 1) % 4
        bi += 1
        infected.add((x, y))
    x, y = x + ds[di][0], y + ds[di][1]

print(bi)


di = 1
x, y = 0, 0

bi = 0

for _ in range(10000000):
    s = board[(x, y)]
    di = (di + s) % 4
    board[(x,y)] = [INFECTED, WEAKENED, CLEAN, FLAGGED][s]
    if board[(x,y)] == INFECTED: bi += 1
    x, y = x + ds[di][0], y + ds[di][1]

print(bi)
