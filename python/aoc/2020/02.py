from .util import getinput

a1 = 0
a2 = 0
for line in getinput(2).splitlines():
    a, b, c = line.split()
    mn, mx = [int(x) for x in a.split('-')]
    if mn <= sum(x == b[0] for x in c) <= mx:
        a1 += 1
    if (c[mn-1] == b[0]) != (c[mx-1] == b[0]):
        a2 += 1
print(a1)
print(a2)
