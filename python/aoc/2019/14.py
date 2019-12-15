from .util import getinput

from collections import defaultdict
import networkx as nx


def rp(s):
    a, b = s.strip().split(' ')
    return (int(a), b)

def builddb(a):
    G = nx.DiGraph()
    ret = {}
    for (l, o) in a:
        oi, ot = o
        ret[ot] = (oi, {v: k for (k, v) in l})
        G.add_edges_from((ot, v) for (_, v) in l)
    return ret, G

def getcost(d, g, t, amount=1):
    o = defaultdict(int, {t:amount})
    for t in nx.topological_sort(g):
        if t not in o or t not in d:
            continue
        i, l = d[t]
        oi = o[t]
        n = (oi + i - 1) // i
        for k, v in l.items():
            o[k] += n * v
        o.pop(t)
    return dict(o)

def search(pred, l, h):
    if h <= l + 1:
        return h
    m = (l + h) // 2
    return search(pred, l, m) if pred(m) else search(pred, m, h)


s = getinput(14)
a1 = [l.split('=>') for l in s.strip().split('\n')]
a = [(tuple(rp(x) for x in a.split(',')), rp(b)) for [a,b] in a1]
d,  g = builddb(a)

print(getcost(d, g, 'FUEL')['ORE'])
print(search(lambda x: getcost(d,g, 'FUEL', x)['ORE'] > 1000000000000, 1, 1000000000000) - 1)
