from .util import getinput
from functools import reduce

s = getinput(6)

a1 = sum(len(set(''.join(group.splitlines()))) for group in s.split('\n\n'))
a2 = sum(len(reduce(lambda a, b: a & set(b), group.splitlines()[1:], set(group.splitlines()[0]))) for group in s.split('\n\n'))
print(a1)
print(a2)