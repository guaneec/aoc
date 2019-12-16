from .util import getinput

import numpy as np

s = '''../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#'''

s = getinput(21)

def rot(a):
    n = len(a)
    return a.T[:,n-1::-1]

rules = {}

for l in s.strip().splitlines():
    ll, lr = l.split('=>')
    pat =  np.array([[c == '#' for c in l] for l in ll.strip().split('/') ])
    res = np.array([[c == '#' for c in l] for l in lr.strip().split('/') ])

    for _ in range(4):
        pat = rot(pat)
        rules[tuple(pat.ravel())] = res
        rules[tuple(pat.T.ravel())] = res


a = np.array([[0,1,0,0,0,1,1,1,1]]).reshape((3,3))

def step(rules, a):
    n = len(a)
    d = 2 if len(a) % 2 == 0 else 3
    return np.block([[ rules[tuple(a[i:i+d, j:j+d].ravel())] for j in range(0, n, d) ] for i in range(0, n ,d) ])


for _ in range(5):
    a = step(rules, a)
print(np.sum(a))

for _ in range(18-5):
    a = step(rules, a)
print(np.sum(a))
