from .util import getinput
import numpy as np
import doctest
from itertools import count

def p1(x):
    x = (x + 9) // 10
    a = np.zeros((x,))
    for i in range(1, x):
        a[i-1::i] += i
    return np.nonzero(a >= x)[0][0]+1
    

def p2(x):
    x = (x + 10) // 11
    a = np.zeros((x,))
    for i in range(1, x):
        a[i-1:i*50:i] += i
    return np.nonzero(a >= x)[0][0]+1

x = int(getinput(20))
print(p1(x))
print(p2(x))
