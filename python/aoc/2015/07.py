from .util import getinput
import doctest
import re

def p1(s, b=None):
    conns = {}
    for l in s.strip().splitlines():
        sl, sr = map(lambda s: s.strip(), l.split('->'))
        if sl.isdigit():
            sl = int(sl)
        if b is not None and sr == 'b':
            sl = b
        conns[sr] = sl
    
    def resolve(conns, x):
        if x.isdigit():
            return int(x)
        r = conns[x]
        if type(r) == int:
            return r
        if 'AND' in r:
            sl, sr = map(lambda s: s.strip(), r.split('AND'))
            res = resolve(conns, sl) & resolve(conns, sr)
        elif 'OR' in r:
            sl, sr = map(lambda s: s.strip(), r.split('OR'))
            res = resolve(conns, sl) | resolve(conns, sr)
            conns[x] = res
            return res
        elif 'NOT' in r:
            y = r[4:].strip()
            res = 65535 - resolve(conns, y)
        elif 'LSHIFT' in r:
            sl, sr = map(lambda s: s.strip(), r.split('LSHIFT'))
            res = resolve(conns, sl) << int(sr)
        elif 'RSHIFT' in r:
            sl, sr = map(lambda s: s.strip(), r.split('RSHIFT'))
            res = resolve(conns, sl) >> int(sr)
        else:
            res = resolve(conns, r)

        conns[x] = res
        return res
    
    for w in conns:
        resolve(conns, w)
    
    return conns

doctest.testmod()
s = getinput(7)
p1a = p1(s)['a']
print(p1a)
print(p1(s, b=p1a)['a'])
