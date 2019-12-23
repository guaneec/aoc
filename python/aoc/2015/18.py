from .util import getinput
import doctest
from itertools import product

def adj8(xy):
    x, y = xy
    return [
        (x+1, y+1),
        (x-1, y-1),
        (x-1, y+1),
        (x+1, y-1),
        (x, y+1),
        (x, y-1),
        (x+1, y),
        (x-1, y),
    ]

def coords(board):
    s = set()
    for y, l in enumerate(board.strip().splitlines()):
        for x, c in enumerate(l):
            if c == '#':
                s.add((x, y))
    return s

test = coords("""
.#.#.#
...##.
#....#
..#...
#.#..#
####..
""")
test1 = coords("""
..##..
..##.#
...##.
......
#.....
#.##..
""")
test2 = coords("""
..###.
......
..###.
......
.#....
.#....
""")
test3 = coords("""
...#..
......
...#..
..##..
......
......
""")
test4 = coords("""
......
......
..##..
..##..
......
......
""")

ttest = coords("""
##.#.#
...##.
#....#
..#...
#.#..#
####.#
""")
ttest1 = coords("""
#.##.#
####.#
...##.
......
#...#.
#.####
""")
ttest2 = coords("""
#..#.#
#....#
.#.##.
...##.
.#..##
##.###
""")
ttest3 = coords("""
#...##
####.#
..##.#
......
##....
####.#
""")
ttest4 = coords("""
#.####
#....#
...#..
.##...
#.....
#.#..#
""")
ttest5 = coords("""
##.###
.##..#
.##...
.##...
#.#...
##...#
""")

def step(lights, n, stuck=False):
    """
    >>> step(test, 6) == test1
    True
    >>> step(test1, 6) == test2
    True
    >>> step(test2, 6) == test3
    True
    >>> step(test3, 6) == test4
    True
    >>> step(ttest, 6, True) == ttest1
    True
    >>> step(ttest1, 6, True) == ttest2
    True
    >>> step(ttest2, 6, True) == ttest3
    True
    >>> step(ttest3, 6, True) == ttest4
    True
    >>> step(ttest4, 6, True) == ttest5
    True
    """
    lnew = set()
    for xy in product(range(n), range(n)):
        if (xy in lights and sum(z in lights for z in adj8(xy)) in (2, 3)
            or xy not in lights and sum(z in lights for z in adj8(xy)) == 3
            or stuck and xy[0] in (0, n-1) and  xy[1] in (0, n-1)
            ):
            lnew.add(xy)
    return lnew

doctest.testmod()
s = getinput(18)
l = coords(s)
for _ in range(100):
    l = step(l, 100)
print(len(l))
l = coords(s) | { (0,0), (99, 0), (0, 99), (99, 99) }
for _ in range(100):
    l = step(l, 100, True)
print(len(l))
