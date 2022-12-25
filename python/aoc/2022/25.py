from .util import getinput

s = getinput(25)

def f(w):
    b = 1
    o = 0
    for c in w[::-1]:
        o += ('=-012'.find(c)-2) * b
        b *= 5
    return o

p1 = sum(map(f, s.strip().splitlines()))
print(p1)

def g(w):
    while True:
        if -2 <= w <= 2:
            return '=-012'[w+2]
        else:
            r = w % 5
            if r > 2:
                r -= 5
            return g((w-r)//5) + g(r)

print(g(p1))
            