from .util import getinput
from collections import defaultdict, Counter

s = getinput(24)

def fromline(s):
    sn = ""
    for c in s:
        if c in "sn":
            sn = c
        else:
            yield sn + c
            sn = ""


def adj(p):
    x, y = p
    return [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y + 1),
    ]


a = defaultdict(int)
for l in s.splitlines():
    x, y = 0, 0
    for d in fromline(l):
        if d == "e":
            x += 1
        elif d == "w":
            x -= 1
        elif d == "ne":
            y += 1
        elif d == "sw":
            y -= 1
        elif d == "nw":
            x -= 1
            y += 1
        elif d == "se":
            x += 1
            y -= 1
    a[(x, y)] += 1

t = {k for k, v in a.items() if v % 2 == 1}
print(len(t))


def step(t):
    def cands(t):
        for tt in t:
            yield tt
            yield from adj(tt)

    q = set(cands(t))
    nt = set()
    for z in q:
        l = sum(x in t for x in adj(z))
        if z in t and not (l == 0 or l > 2) or z not in t and l == 2:
            nt.add(z)
    return nt


def viz(t):
    n = max(max(abs(x), abs(y), abs(abs(x)-abs(y))) for x, y in t) + 1
    m = 4 * n + 1
    for z in reversed(range(-n + 1, n)):
        s = " ".join(
            ".#"[(x, z) in t] for x in range(-n + max(0, -z), 1 + n - max(0, z))
        )
        print(" " * ((m - len(s)) // 2) + s)
    print()

# viz(t)
for _ in range(100):
    t = step(t)
    # viz(t)

print(len(t))