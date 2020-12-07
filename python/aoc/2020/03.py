from .util import getinput
from functools import reduce
from operator import mul

s = getinput(3).splitlines()

m = len(s)
n = len(s[0])

trees = lambda dx, dy: sum(s[i * dy][i * dx % n] == "#" for i in range(m // dy))

ds = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

print(trees(3, 1))
print(reduce(mul, (trees(dx, dy) for dx, dy in ds), 1))