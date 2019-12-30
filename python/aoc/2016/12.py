from .util import getinput
import doctest
from collections import defaultdict
import re

'''
a,b,d = 1,1,26

if c:
    d+=7

repeat d:
    a, b = a+b, a 

a += 16 * 12

'''

def run(code, init=None):
    i = 0
    regs = defaultdict(int, [] if init is None else init)
    val = lambda x: int(x) if x.isdigit() else regs[x]
    while i < len(code):
        ins, args = code[i]
        if ins == 'cpy':
            x, y = args
            regs[y] = val(x)
        elif ins == 'inc':
            regs[args[0]] += 1
        elif ins == 'dec':
            regs[args[0]] -= 1
        elif ins == 'jnz':
            x, y = args
            if val(x):
                i += int(y) - 1
        else:
            assert(False)
        i += 1
    return dict(regs)
            

s = getinput(12)

a, b = 1, 1
for i in range(26+7):
    a, b = a+b, a
    if i == 26 - 1:
        print(a+ 16 * 12)
    if i == 26 + 7 - 1:
        print(a + 16 * 12)

"""
code = [(l[:3], l[4:].split()) for l in s.strip().splitlines() ]
print(run(code)['a'])
print(run(code, {'c': 1})['a'])
"""
