from .util import getinput
import doctest
from collections import defaultdict

def parse(s):
    o = defaultdict(list)
    for l in s.strip().splitlines():
        a, b = l.split(' => ')
        o[a].append(b)
    return o

def pp(s):
    a, b = s.split('\n\n')
    return parse(a), b.strip()
    
tr = parse('''H => HO
H => OH
O => HH''')

tr2 = parse('''
e => H
e => O
H => HO
H => OH
O => HH''')

def p1(reps, seed):
    """
    >>> p1(tr, 'HOH')
    4
    >>> p1(tr, 'HOHOHO')
    7
    """
    o = set()
    for i in range(len(seed)):
        for k, v in reps.items():
            if seed[i:].startswith(k):
                for vv in v:
                    o.add(seed[:i] + seed[i:].replace(k, vv, 1))
    return len(o)

def rev(reps):
    o = defaultdict(list)
    for k, v in reps.items():
        for vv in v:
            o[vv].append(k)
    return o

def p2(reps, seed):
    """
    >>> p2(tr2, "HOH")
    3
    >>> p2(tr2, "HOHOHO")
    6
    """
    visited = {seed}
    stack = [(seed, 0)]
    reps = rev(reps)
    while stack:
        s, step = stack.pop()
        if s == 'e':
            return step
        for i in range(len(s)):
            for k, v in reps.items():
                if s[i:].startswith(k):
                    for vv in v:
                        ss = s[:i] + s[i:].replace(k, vv, 1)
                        if (vv == 'e' and ss != 'e') or ss in visited:
                            continue
                        stack.append( (ss, step+1) )


# reaches max recursion 
def p2r(reps, seed):
    """
    >>> p2r(tr2, "HOH")
    3
    >>> p2r(tr2, "HOHOHO")
    6
    """
    def f(reps, seed):
        if seed == 'e':
            return 0
        def g(reps, seed):
            for i in range(len(seed)):
                for k, v in reps.items():
                    if seed[i:].startswith(k):
                        for vv in v:
                            ss = seed[:i] + seed[i:].replace(k, vv, 1)
                            if not (vv == 'e' and ss != 'e'):
                                yield ss
        return min( (1 + x for x in (f(reps, ss) for ss in g(reps, seed)) if x is not None), default=None )
    return f(rev(reps), seed)

                    

doctest.testmod()
s = getinput(19)
r, seed = pp(s)
print(p1(r, seed))
print(p2(r, seed))

