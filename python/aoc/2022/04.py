from .util import getinput

s = getinput(4).strip()

p1, p2 = 0, 0
for l in s.splitlines():
    x, y = l.split(',')
    a, b = map(int, x.split('-'))
    c, d = map(int, y.split('-'))
    t, u = set(range(a, b+1)), set(range(c, d+1))
    p1 += t & u == u or t & u == t
    p2 += not not t & u
print(p1)
print(p2)