from .util import getinput

s = getinput(7)
xs = [int(x) for x in  s.split(',')]
f = lambda x: x * (x + 1) // 2
print(min(sum(abs(m-x) for x in xs) for m in range(min(xs), max(xs))))
print(min(sum(f(abs(m-x)) for x in xs) for m in range(min(xs), max(xs))))