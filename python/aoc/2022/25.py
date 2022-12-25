from .util import getinput

s = getinput(25)

def f(w):
    b = 1
    o = 0
    for c in w[::-1]:
        o += ('=-012'.find(c)-2) * b
        b *= 5
    return o

x = sum(map(f, s.splitlines()))

def g(w):
    o = []
    while w:
        r = w % 5
        o.append('012=-'[r])
        w = w // 5 + (r > 2)
    return ''.join(reversed(o)) if o else '0'

print(g(x))
            