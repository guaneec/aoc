from .util import getinput
import doctest
import re
from collections import defaultdict

test = '''
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
'''

def p1(s, minmax=min):
    """
    >>> p1(test)
    605
    >>> p1(test, max)
    982
    """
    edges = defaultdict(dict)
    for l in s.strip().splitlines():
        a, b, d = re.match(r'^(\w+) to (\w+) = (\d+)$', l).group(1, 2, 3)
        edges[a][b] = edges[b][a] = int(d)
    def minpath(es, v, vs):
        if not vs:
            return 0
        return minmax( minpath(es, vv, vs-{vv}) + es[v][vv] for vv in vs )

    vs = edges.keys()
    return minmax( minpath(edges, v, vs - {v}) for v in vs)
        

assert(doctest.testmod()[0] == 0)
s = getinput(9)
print(p1(s))
print(p1(s, max))
