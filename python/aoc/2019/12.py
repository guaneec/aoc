import re
from itertools import permutations
import numpy as np
from numpy import array
from functools import reduce
from math import gcd

def nextxv(xv):
    xs, vs = np.array([xv[0]]), np.array(xv[1])
    vs += np.sum(np.sign(xs-xs.T), axis=1)
    xs[0] += vs
    return tuple(xs[0]), tuple(vs)

def findcycle(f, x0):
    xs = {x0: 0}
    x = x0
    i = 0
    while True:
        i += 1
        x = f(x)
        if x in xs:
            return xs[x], i - xs[x]
        xs[x] = i
        
def lcm(a, b):
    return a * b // gcd(a, b)

def sumcycles(mcs):
    ms, cs = zip(*mcs)
    return max(ms), reduce(lcm, cs)

s = '''<<x=7, y=10, z=17>
<x=-2, y=7, z=0>
<x=12, y=5, z=12>
<x=5, y=-8, z=6>'''

moons = array([[array(list(int(i) for i in re.findall(r'-?\d+', l))), array([0,0,0])] for l in s.split('\n')])
n = len(moons)
for _ in range(1000):
    for d in range(3):
        xs, vs = tuple(moons[:,0,d]), tuple(moons[:,1,d])
        xxs, vvs = nextxv((xs, vs))
        moons[:,0,d], moons[:,1,d] = np.array(xxs), np.array(vvs)
        
print(abs(moons[:,0,:]).sum(axis=1) @ abs(moons[:,1,:]).sum(axis=1))

moons = array([[array(list(int(i) for i in re.findall(r'-?\d+', l))), array([0,0,0])] for l in s.split('\n')])
mcs = [findcycle( nextxv, (tuple(moons[:,0,d]), tuple(moons[:,1,d])) ) for d in range(3)]
m,c = sumcycles(mcs)
print( m, c, m+c)
