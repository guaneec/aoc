from .util import getinput

lines = getinput(1)
a = [[int(l) for l in g.split('\n')] for g in getinput(1).strip().split('\n\n')]
print(max(map(sum, a)))
print(sum(sorted(map(sum, a))[-3:]))