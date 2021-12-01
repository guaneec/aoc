from .util import getinput

lines = getinput(1).splitlines()
x = [int(line) for line in lines]
s = [a + b + c for a, b, c in zip(x, x[1:], x[2:])]
print(sum(a < b for a, b in zip(x, x[1:])))
print(sum(a < b for a, b in zip(s, s[1:])))
