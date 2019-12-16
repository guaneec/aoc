from .util import getinput, Machine
from collections import defaultdict
from itertools import cycle, accumulate, chain
import numpy as np

s = getinput(16).strip()
#s = '69317163492948606335995924319873'

def dsin(n):
    first = True
    for x in cycle([0,1,0,-1]):
        for _ in range(n):
            if not first:
                yield x
            first = False    

def fft1(a, n):
    g = dsin(n)
    d = np.array([x for (x,_) in zip(g,a)], dtype=int)
    abs(np.sum(a@d))

def fft(a):
    return [fft1(a, i) for i in range(1, len(a)+1)]

def p1():
    a = [int(x) for x in s]
    for _ in range(100):
        a = fft(a)
    print(''.join(str(x) for x in a[:8]))

def ffft(a):
    n = len(a)
    sums = list(reversed(list(accumulate(reversed(a)))))
    rets = sums.copy()
    for m, sign in zip(range(2, n+1), cycle([-1,-1,+1,+1])) :
        for i in range(1, n // m + 1):
            rets[i-1] += sign * sums[i*m-1]
    return [abs(x) % 10 for x in rets]


a = [int(x) for x in s] * 10000
off = int(s[:7])
print(''.join(str(x) for x in a[off:off+8]))
for x in range(100):
    print(x)
    a = ffft(a)
print(''.join(str(x) for x in a[off:off+8]))
