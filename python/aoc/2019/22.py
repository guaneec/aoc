from .util import getinput
import re

# gives the new position
def dNew(k, p):
    return p - 1 - k 

def dCut(k, p, i):
    return (k - i) % p

def dInc(k, p, i):
    return (k * i) % p


s = getinput(22)


P = 10007 
pos = 2019

for l in s.strip().splitlines():
    if "new" in l:
        f = lambda k: dNew(k, P)
    else:
        i = int(re.findall(r'-?\d+', l)[0])
        if "cut" in l:
            f = lambda k: dCut(k, P, i)
        else:
            assert("inc" in l)
            f = lambda k: dInc(k, P, i)
    pos = f(pos)

print(pos)

# modular inverse
def inv(a, n):
    t, newt = 0, 1
    r, newr = n, a
    while newr:
        q = r // newr
        t, newt = newt, t - q * newt
        r, newr = newr, r - q * newr
    assert(r <= 1)
    if t < 0:
        t = t + n
    return t

# gives the previous position
def cNew(x, p):
    return p - 1 - x

def cCut(x, p, i):
    return (x + i) % p

def cInc(x, p, i):
    return (x * inv(i, p)) % p

# find the linear polynomial ax + b
def pNew(ab, p):
    a, b = ab
    return (-a) % p, (-b - 1) % p

def pCut(ab, p, i):
    a, b = ab
    return a % p, (b + i) % p

def pInc(ab, p, i):
    a, b = ab
    ii = inv(i, p)
    return (a * ii) % p, (b * ii) % p



P = 119315717514047

pol = (1, 0)


for l in reversed(s.strip().splitlines()):
    if "new" in l:
        f = lambda k: pNew(k, P)
    else:
        i = int(re.findall(r'-?\d+', l)[0])
        if "cut" in l:
            f = lambda k: pCut(k, P, i)
        else:
            assert("inc" in l)
            f = lambda k: pInc(k, P, i)
    pol = f(pol)


def modPow(k, n, p):
    if n == 0:
        return 1
    if n == 1:
        return k
    m, r = divmod(n, 2)
    x = modPow(k, m, p)
    return (x * x * modPow(k, r, p)) % p


# x
# ax + b
# a(ax + b) + b = a^2 x + ab + b  = a^2 x + b * (a^2 - 1) / (a - 1)
# a(a(ax + b) + b) + b = a^3 x + a^2 b + ab + b = a^3 x + b * (a^3 - 1) / (a - 1)

def polyIter(ab, n, p):
    a, b = ab
    an = modPow(a, n, p)
    return an, (b * inv(a - 1, p) * (an - 1)) % p

pol = polyIter(pol, 101741582076661, P)
a, b = pol
print((a * 2020 + b) % P)
