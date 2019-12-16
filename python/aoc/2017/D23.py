from collections import defaultdict, deque
from .util import getinput

s = getinput(23)

regs = defaultdict(int)

def f(x):
    try:
        return int(x)
    except ValueError:
        return regs[x]



code = [l.split(' ') for l in  s.strip().splitlines()]

mul = 0

i = 0
while i < len(code):
    ws = code[i]
    if ws[0] == 'set':
        regs[ws[1]] = f(ws[2])
    elif ws[0] == 'sub':
        regs[ws[1]] -= f(ws[2])
    elif ws[0] == 'mul':
        regs[ws[1]] *= f(ws[2])
        mul += 1
    elif ws[0] == 'jnz':
        if f(ws[1]) != 0:
            i += f(ws[2]) - 1
    else:
        raise Exception('what??')
    i += 1

print(mul)

def isprime(n):
    return not n % 2 == 0 and not any( n % i == 0 for i in range(3, int(n**.5)) )
print(sum( not isprime(x) for x in range(106700, 106700+17001, 17)))
