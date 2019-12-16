from collections import Counter

from .util import getinput

s = '''0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10'''

s = getinput(24)

cs = [tuple(sorted(int(x) for x in l.split('/'))) for l in s.strip().splitlines()]

print(cs)

def f(current, pieces: Counter):
    maxscore = 0
    for p in pieces:
        if current in p:
            a, b = p
            other = a if a != current else b
            c = pieces.copy()
            c[p] -= 1
            if (c[p] == 0):
                del c[p]
            maxscore = max( maxscore, a + b + f( other, c ) )
    return maxscore

def g(current, pieces: Counter):
    maxscore = (0, 0)
    for p in pieces:
        if current in p:
            a, b = p
            other = a if a != current else b
            c = pieces.copy()
            c[p] -= 1
            if (c[p] == 0):
                del c[p]
            ll, ss = g( other, c )
            maxscore = max(maxscore,  (ll+1, ss + a + b) )
    return maxscore

print(f( 0, Counter(cs) ))
print(g( 0, Counter(cs) ))
