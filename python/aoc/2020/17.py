from .util import getinput
from itertools import product, islice, starmap

s = getinput(17)

xys = {
    (x, y)
    for (y, l) in enumerate(s.splitlines())
    for (x, c) in enumerate(l)
    if c == "#"
}
n = len(s.splitlines())


def adj(p):
    return islice(product(*((x, x - 1, x + 1) for x in p)), 1, None)


def step(state, height, dim):
    def lives(p):
        s = sum(pp in state for pp in adj(p))
        has = p in state
        return 2 <= s <= 3 and has or 3 == s and not has

    return {
        p
        for p in product(
            *starmap(
                range, [(-height, n + height)] * 2 + [(-height, height + 1)] * (dim - 2)
            )
        )
        if lives(p)
    }


for d in (3, 4):
    state = {(*p, *([0] * (d - 2))) for p in xys}
    for i in range(6):
        state = step(state, i + 1, d)
    print(len(state))