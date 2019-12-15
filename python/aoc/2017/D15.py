def eq(a, b):
    mask = 0b1111_1111_1111_1111
    return (a & mask) == (b & mask)

def gen(seed, m):
    while True:
        seed = seed * m % 2147483647
        yield seed

ga = gen(277, 16807)
gb = gen(349, 48271)

print(sum(eq(next(ga), next(gb)) for i in range(40_000_000)))


def fa():
    g = gen(277, 16807)
    for x in g:
        if x % 4 == 0:
            yield x
def fb():
    g = gen(349, 48271)
    for x in g:
        if x % 8 == 0:
            yield x

ga2 = fa()
gb2 = fb()

print(sum(eq(next(ga2), next(gb2)) for i in range(5_000_000)))
