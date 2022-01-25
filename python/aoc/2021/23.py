from .util import getinput
from ..aoc import astar
from itertools import permutations, chain


s = getinput(23)

doors = [(1, j) for j in (3, 5, 7, 9)]
slots = [(1, j) for j in range(1, 12) if j not in [3, 5, 7, 9]]

# State: [(a0, a1), (b0, b1), ...]


def dist(a, b):
    i1, j1 = a
    i2, j2 = b
    return abs(j1 - j2) + (abs(i1 - i2) if j1 == j2 else abs(1 - i1) + abs(1 - i2))


costs = [1, 10, 100, 1000]


def assign(state, t, u, q):
    return tuple(
        tuple(sorted(q if (t, u) == (tt, uu) else c for uu, c in enumerate(r)))
        for tt, r in enumerate(state)
    )


def solve(d):
    def h(state):
        return sum(
            costs[t]
            * min(
                sum(dist(a, (b, 3 + 2 * t)) for a, b in zip(p, range(2, 2 + d)))
                for p in permutations(qs)
            )
            for t, qs in enumerate(state)
        )

    def nb(state):
        s = set(chain(*state))
        for t, ps in enumerate(state):
            for u, (i, j) in enumerate(ps):
                if i != 1:  # in room, move into hallway
                    if not any((ii, j) in s for ii in range(2, i)):
                        for rr in (range(j, 0, -1), range(j, 12)):
                            for jj in rr:
                                if (1, jj) in s:
                                    break
                                if jj not in (3, 5, 7, 9):
                                    yield costs[t] * dist((i, j), (1, jj)), assign(
                                        state, t, u, (1, jj)
                                    )
                # move into room
                ri, rj = 1 + d - sum(jj == 3 + 2 * t for _, jj in ps), 3 + 2 * t
                if not (
                    (i, j) == (ri + 1, rj)
                    or any((ii, j) in s for ii in range(2, i))
                    or any((1, jj) in s for jj in range(min(j, rj) + 1, max(j, rj)))
                    or any((ii, rj) in s for ii in range(2, ri + 1))
                ):
                    yield costs[t] * dist((i, j), (ri, rj)), assign(
                        state, t, u, (ri, rj)
                    )

    init = [[] for _ in range(4)]
    if d == 4:
        ss = ("  #D#C#B#A#", "  #D#B#A#C#")
        ll = s.splitlines()
        ss = "\n".join([*ll[:3], *ss, *ll[3:]])
    else:
        ss = s
    for i, r in enumerate(ss.splitlines()):
        for j, c in enumerate(r):
            if c in "ABCD":
                init["ABCD".index(c)].append((i, j))
    init = tuple(map(tuple, init))
    goal = tuple(tuple((i, j) for i in range(2, 2 + d)) for j in [3, 5, 7, 9])

    for g, n in astar([init], nb, h):
        if n == goal:
            return g
    assert False


print(solve(2))
print(solve(4))
