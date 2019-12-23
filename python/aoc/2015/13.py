from .util import getinput
import doctest
import re
from collections import defaultdict

test = """
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
"""

def p1(s, me=False):
    """
    >>> p1(test)
    330
    """
    edges = defaultdict(dict)
    for l in s.strip().splitlines():
        a, pm, d, b = re.match(r'^(\w+).+(gain|lose) (\d+).+ (\w+)\.$', l).group(1, 2, 3, 4)
        edges[a][b] = int(d) * (1 if pm == 'gain' else -1)
    if me:
        for v in list(edges.keys()):
            edges[v]['me'] = 0
            edges['me'][v] = 0
    edges = dict(edges)
    def findmax(edges, v0, v, vs):
        if not vs:
            return edges[v][v0] + edges[v0][v]
        return max( edges[vv][v] + edges[v][vv] + findmax(edges, v0, vv, vs - {vv}) for vv in vs )
    vs = list(edges.keys())
    return findmax(edges, vs[0], vs[0], set(vs[1:]))

doctest.testmod()
s = getinput(13)
print(p1(s))
print(p1(s, True))
