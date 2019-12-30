from .util import getinput
import doctest
from collections import defaultdict
from math import factorial
import re
from itertools import islice, count


def run(code, init=None):
    i = 0
    regs = defaultdict(int, [] if init is None else init)
    val = lambda x: int(x) if x not in 'abcd' else regs[x]
    while i < len(code):
        if (i == 28):
            print(ins, args, tuple(regs[x] for x in 'abcd'))
        ins, args = code[i]
        if ins == 'cpy':
            x, y = args
            if y in 'abcd':
                regs[y] = val(x)
        elif ins == 'inc':
            if args[0] in 'abcd':
                regs[args[0]] += 1
        elif ins == 'dec':
            if args[0] in 'abcd':
                regs[args[0]] -= 1
        elif ins == 'jnz':
            x, y = args
            if val(x):
                i += val(y) - 1
        elif ins == 'tgl':
            d = val(args[0])
            if 0 <= i+d < len(code):
                ns = code[i+d][0]
                code[i+d][0] = 'dec' if ns == 'inc' else 'inc' if ns in ('dec', 'tgl') else 'cpy' if ns == 'jnz' else 'jnz' if ns == 'cpy' else None
        elif ins == 'out':
            yield val(args[0])
        else:
            assert(False)
        i += 1
            
s = getinput(25)

ans = int('10' * ((len(bin(2532)[2:]) + 1) // 2), 2) - 2532
print(ans)
