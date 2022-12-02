from .util import getinput

o = 0
p = 0
s = getinput(2).strip()
for l in s.splitlines():
    a, b = l.split()
    t = ord(a) - ord('A')
    u = ord(b) - ord('X')
    o += [1, 2, 3][u]
    o += [3, 6, 0][(u - t + 3) % 3]
    p += [0, 3, 6][u]
    p += [1, 2, 3][(t + 3 + u - 1) % 3]
print(o)
print(p)