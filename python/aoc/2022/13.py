from .util import getinput
import functools

s = getinput(13)

# correct: -1
def cmp(a, b):
    if type(a) == int and type(b) == int:
        return (a > b) - (a < b)
    elif type(a) == int:
        return cmp([a], b)
    elif type(b) == int:
        return cmp(a, [b])
    else:
        for x, y in zip(a, b):
            c = cmp(x, y)
            if c != 0:
                return c
        return (len(a) > len(b)) - (len(a) < len(b))
a = [[[2]], [[6]]]
o = 0
for i, g in enumerate(s.split('\n\n'), 1):
    l, r = map(eval, g.splitlines())
    o += i * (cmp(l, r) == -1)
    a.extend([l, r])
print(o)
a.sort(key=functools.cmp_to_key(cmp))
i = a.index([[2]])
j = a.index([[6]])
print((i+1)*(j+1))