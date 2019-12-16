import re
from itertools import combinations
from collections import defaultdict
from .util import getinput


s = '''p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>'''
s = getinput(20)

ps = [[int(x) for x in  re.findall('-?\d+', l)] for l in s.splitlines()]

a2 = lambda p: p[6] ** 2 + p[7] ** 2 + p[8] ** 2

print(min(enumerate(ps), key=lambda p: a2(p[1])))

def solq(a, b, c):
    if a == 0:
        if b == 0:
            return None if c == 0 else []
        x = -c / b
        return [int(x)] if x % 1 == 0 and x >= 0 else []
    
    if b ** 2 < 4 * a * c:
        return []
    d = (b ** 2 - 4 * a * c) ** 0.5
    x1 = (-b + d) / 2 / a
    x2 = (-b - d) / 2 / a
    return [int(x) for x in (x1, x2) if x % 1 == 0 and x >= 0]
    
def coll(p1, p2):
    px1, py1, pz1, vx1, vy1, vz1, ax1, ay1, az1 = p1
    px2, py2, pz2, vx2, vy2, vz2, ax2, ay2, az2 = p2
    solx = solq( (ax1-ax2) / 2, vx1-vx2 + (ax1-ax2) / 2, px1-px2 )
    soly = solq( (ay1-ay2) / 2, vy1-vy2 + (ay1-ay2) / 2, py1-py2 )
    solz = solq( (az1-az2) / 2, vz1-vz2 + (az1-az2) / 2, pz1-pz2 )
    ss = solx if solx is not None else soly if soly is not None else solz
    g = lambda s, x : s is None or x in s
    return [(s, (
        px1 + s * vx1 + s * (s+1) // 2 * ax1,
        py1 + s * vy1 + s * (s+1) // 2 * ay1,
        pz1 + s * vz1 + s * (s+1) // 2 * az1,
    ) ) for s in ss if g(solx, s) and g(soly, s) and g(solz, s) ]

# v(n) = n*a + v0
# p(n) = p(0) + sum(v(k), k==1..n) = p(0) + n*v0 + a * n * (n+1) / 2

# collision p1, p2 = n | x1-x2 + n * (v1-v2) + n * (n+1) / 2 * (a1-a2) == 0



cs = defaultdict(lambda: defaultdict(set))
n = len(ps)
for i in range(n):
    for j in range(i+1, n):
        for (t, p) in coll(ps[i], ps[j]):
            cs[t][p].add(i)
            cs[t][p].add(j)

safe = set(range(n))

for (t, cc) in sorted(cs.items(), key=lambda x:x[0]):
    if t < 0: 
        continue
    for where, who in cc.items():
        if len(who & safe) > 1:
            for i in who:
                safe.discard(i)

print(len(safe))
