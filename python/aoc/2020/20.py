from .util import getinput
import numpy as np
from scipy import signal
from functools import lru_cache

s = getinput(20)
def getblock(s):
    a, _, b = s.partition('\n')
    return int(a[5:-1]), np.array( [ [c == '#' for c in l] for l in b.splitlines() ] )
tiles = {}
for sb in s.split('\n\n'):
    if not sb:
        continue
    k, v = getblock(sb)
    tiles[k] = v


def nxt(i, j):
    if i == j:
        return 0, j + 1
    if i + 1  == j:
        return i + 1, 0
    if i < j:
        return i + 1, j
    return i, j + 1


ks = list(tiles.keys())
m = len(ks)
n = int(m ** .5)

def tf(t, r, f):
    return np.rot90(t if not f else np.flipud(t), r)

@lru_cache(None)
def adj_(i, r, f):
    o = []
    edge = tf(tiles[i], r, f)[:,-1]
    for j in ks:
        if i == j:
            continue
        for ff in range(2):
            for rr in range(4):
                if np.all(edge == tf(tiles[j], rr, ff)[:,0]):
                    o.append((j, rr, ff))
    return o

def adj(i, r, f, hori):
    return adj_(i, r, f) if hori else [(j, (rr+3)%4, ff) for j, rr, ff in adj_(i, (r+1)%4, f) ]

def match(ids, rots, flips, rems, i1, i2):
    if not rems:
        return ids, rots, flips
    s = set((i, r, f) for i in rems for r in range(4) for f in range(2))
    if i1 > 0:
        s = s & set(adj(ids[i1-1,i2], rots[i1-1,i2], flips[i1-1,i2], False))
    if i2 > 0:
        s = s & set(adj(ids[i1,i2-1], rots[i1,i2-1], flips[i1,i2-1], True))
    
    for i, r, f in s:
        ids[i1,i2] = i
        rots[i1,i2] = r
        flips[i1,i2] = f
        rems.remove(i)
        m = match(ids, rots, flips, rems, *nxt(i1, i2))
        rems.add(i)
        if m is not None:
            return m
    return None

            
ids = np.zeros((n, n), dtype=int)
rots = np.zeros((n, n), dtype=int)
flips = np.zeros((n, n), dtype=int)
ids, rots, flips = match(ids, rots, flips, set(ks), 0, 0)
print(ids[0,0]*ids[0,-1]*ids[-1,0]*ids[-1,-1])

def stitch(ids, rots):
    o = np.zeros((n*8, n*8), dtype=int)
    for i in range(n):
        for j in range(n):
            o[i*8:i*8+8, j*8:j*8+8] = tf(tiles[ids[i, j]][1:-1,1:-1], rots[i, j], flips[i,j]) 
    return o

im = stitch(ids, rots)
sk = '''\
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
'''
k = np.array([[int(c == '#') for c in l] for l in sk.splitlines()])
a = np.sum(k)
p2m = sum(np.sum(signal.convolve2d(k, tf(im, r, f), 'valid') == a) for r in range(4) for f in range(2))
print(im.sum() - p2m * k.sum())
# print(adj_.cache_info())
