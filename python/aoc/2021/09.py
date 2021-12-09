from .util import getinput
from collections import Counter

s = getinput(9)
ls = [[int(x) for x in l] for l in s.splitlines()]

m, n = len(ls), len(ls[0])

def nb(i, j):
    for ii, jj in [(i+1, j), (i, j+1), (i-1, j), (i, j-1)]:
        if 0 <= ii < m and 0 <= jj < n:
            yield ii, jj

p1 = sum(
    ls[i][j] + 1
    for i in range(m)
    for j in range(n)
    if all(ls[i][j] < ls[ii][jj] for ii, jj in nb(i, j))
)

print(p1)

def f(i, j):
    while not all(ls[i][j] < ls[ii][jj] for ii, jj in nb(i, j)):
        i, j = next(iter((ii, jj) for ii, jj in nb(i, j) if ls[ii][jj] < ls[i][j]))
    return i, j

c = Counter(f(i, j) for i in range(m) for j in range(n) if ls[i][j] != 9)
(_, x), (_, y), (_, z) = c.most_common()[:3]
print(x * y * z)