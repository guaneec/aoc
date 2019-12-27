from .util import getinput
import numpy as np

s = getinput(8)

a = np.zeros((50, 6), dtype=bool)

for l in s.strip().splitlines():
    if l[:5] == 'rect ':
        x, y = map(int, l[5:].split('x'))
        a[:x, :y] = 1
    elif l[:16] == 'rotate column x=':
        r, d = map(int, l[16:].split(' by '))
        a[r] = np.roll(a[r], d)
    elif l[:13] == 'rotate row y=':
        r, d = map(int, l[13:].split(' by '))
        a[:,r] = np.roll(a[:,r], d)
    else:
        assert(False)

print(np.sum(a))
print('\n'.join(''.join(' #'[x] for x in l) for l in a.T))
