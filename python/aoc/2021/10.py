from .util import getinput
from collections import *

s = getinput(10)

left = '(<[{'
right = ')>]}'

lookup = {
    ')': 3,
    ']' : 57,
    '}': 1197,
    '>': 25137,
}

lookup2 = {
    ')': 1,
    ']' : 2,
    '}': 3,
    '>': 4,
}

def bad(l):
    s = []
    for c in l:
        if c in left:
            i = left.index(c)
            s.append(right[i])
        else:
            if not s or s[-1] != c:
                return lookup[c]
            s.pop()
    return 0

def score(l):
    s = []
    for c in l:
        if c in left:
            i = left.index(c)
            s.append(right[i])
        else:
            if not s or s[-1] != c:
                return 0
            s.pop()
    ans = 0
    for c in s[::-1]:
        ans = 5 * ans + lookup2[c]
    return ans

p1 = sum(bad(l) for l in s.splitlines())
print(p1)
scores = sorted(filter(lambda x: x > 0,  (score(l) for l in s.splitlines())))
p2 = scores[len(scores) // 2]
print(p2)