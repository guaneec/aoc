from .util import getinput
import doctest
from collections import defaultdict
import re


def parse(s):
    return [ (l[:3], [ int(x) if re.match('[+-]\d+', x) else x.strip() for x in l[4:].split(', ') ]) for l in s.strip().splitlines() ]

def run(code, init=None):
    i = 0
    regs = defaultdict(int, [] if init is None else init)
    while i < len(code):
        ins, args = code[i]
        if ins == 'hlf':
            regs[args[0]] //= 2
        elif ins == 'tpl':
            regs[args[0]] *= 3
        elif ins == 'inc':
            regs[args[0]] += 1
        elif ins == 'jmp':
            i += args[0] - 1
        elif ins == 'jie' and regs[args[0]] % 2 == 0 or ins == 'jio' and regs[args[0]] == 1:
            i += args[1] - 1
        i += 1
    return dict(regs)
            

doctest.testmod()
s = getinput(23)

code = parse(s)
print(run(code)['b'])
print(run(code, {'a': 1})['b'])
