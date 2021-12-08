from .util import getinput
from collections import Counter, defaultdict

s = getinput(8)

seven = [
    'abcefg',
    'cf',
    'acdeg',
    'acdfg',
    'bcdf',
    'abdfg',
    'abdefg',
    'acf',
    'abcdefg',
    'abcdfg',
]

print([(c, sum(c in w for w in seven)) for c in 'abcdefg'])

p1 = 0
p2 = 0
for l in s.replace('|\n', '| ').splitlines():
    w1, w2 = l.split(' | ')
    digs = [set(ds) for ds in  w1.split()]
    digo = [set(ds) for ds in  w2.split()]
    ds1 = [d for d in digs if len(d) == 2][0]
    ds7= [d for d in digs if len(d) == 3][0]
    ds4 = [d for d in digs if len(d) == 4][0]
    ds8 = [d for d in digs if len(d) == 7][0]
    c = Counter(w1.replace(' ', ''))
    sa = next(iter(ds7 - ds1))
    d = defaultdict(set)
    for k, v in c.items():
        d[v].add(k)
    se = next(iter(d[4]))
    sb = next(iter(d[6]))
    sf = next(iter(d[9]))
    sd = next(iter(ds4 - ds1 - {sb}))
    sg = next(iter(d[7] - {sd}))
    sc = next(iter(d[8] - {sa}))
    lookup = {
        sa: 'a',
        sb: 'b',
        sc: 'c',
        sd: 'd',
        se: 'e',
        sf: 'f',
        sg: 'g',
    }
    def dec(w):
        return seven.index(''.join(sorted(lookup[d] for d in w)))
    def dd(w):
        return int(''.join(str(dec(c)) for c in w))
    p1 += sum(any(do == x for x in (ds1, ds7, ds4, ds8)) for do in digo)
    p2 += dd(digo)

print(p1)
print(p2)