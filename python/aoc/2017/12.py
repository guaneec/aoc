from collections import defaultdict

from .util import getinput

s = getinput(12)

adjs = {}
for l in s.strip().splitlines():
    a, b = l.split('<->')
    adjs[int(a)] = [int(c) for c in b.split(',')]
    
visited = set()
unvisited = set(adjs)

def flood(vs, a, uv):
    if a in vs: return
    vs.add(a)
    uv.discard(a)
    for b in adjs[a]:
        flood(vs, b, uv)

flood(visited, 0, unvisited)
print(len(visited))


unvisited = set(adjs)
ng = 0

while unvisited:
    visited = set()
    e = unvisited.pop()
    flood(visited, e, unvisited)
    ng += 1

print(ng)
