from collections import defaultdict

from .util import getinput

ne = 0
nw = 0

s = getinput(11)

def dist(ne, nw):
    return min((abs(ne) + abs(nw), abs(ne) + abs(ne-nw), abs(nw) + abs(ne-nw) ))

m = 0

for d in s.strip().split(','):
    if d == 'ne':
        ne += 1
    if d == 'nw':
        nw += 1
    if d == 'n':
        ne += 1
        nw += 1
    if d == 'se':
        nw -= 1
    if d == 'sw':
        ne -= 1
    if d == 's':
        ne -= 1
        nw -= 1
    m = max(m, dist(ne, nw))
    
print(dist(ne, nw))
print(m)
