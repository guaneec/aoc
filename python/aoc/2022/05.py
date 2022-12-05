from .util import getinput
from string import ascii_uppercase

s = getinput(5)
for step in (-1, 1):
    d, z = s.split('\n\n')
    d = list(map(list, zip(*d.splitlines())))
    d = [[c for c in l[-1::-1] if c in ascii_uppercase] for l in d[1::4]]
    for l in z.splitlines():
        _, q, _, w, _, e = l.split()
        q, w, e = map(int, (q, w, e))
        d[e-1].extend(d[w-1][-q:][::step])
        d[w-1][-q:] = []
    print(''.join(t[-1] for t in d))