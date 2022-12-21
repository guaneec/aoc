from fractions import Fraction
from .util import getinput

s = getinput(21)

mnks = {}
for l in s.splitlines():
    who, what = l.split(': ')
    mnks[who] = what

def f(who):
    if str.isdigit(mnks[who]):
        return int(mnks[who])
    a, op, b = mnks[who].split()
    if op == '+':
        return f(a) + f(b)
    if op == '-':
        return f(a) - f(b)
    if op == '*':
        return f(a) * f(b)
    if op == '/':
        return f(a) // f(b)

print(f('root'))

def f(who):
    if who == 'humn':
        return (0, 1)
    if str.isdigit(mnks[who]):
        return (int(mnks[who]), 0)
    a, op, b = mnks[who].split()
    a0, a1 = f(a)
    b0, b1 = f(b)
    if op == '+':
        return (a0+b0, a1+b1)
    if op == '-':
        return (a0-b0, a1-b1)
    if op == '*':
        assert a1 * b1 == 0
        return (a0*b0, a1*b0+a0*b1)
    if op == '/':
        assert b1 == 0
        return (Fraction(a0)/b0, Fraction(a1)/b0)
    
a, _, b =  mnks['root'].split()
mnks['root'] = f'{a} - {b}'
e = f('root')
print(-e[0]/e[1])