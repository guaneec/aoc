import re
from dataclasses import dataclass
from .util import getinput


@dataclass
class Cuboid:
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int

    def volume(self):
        return (
            (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1) * (self.z2 - self.z1 + 1)
        )

    def volume50(self):
        assert self.x2 >= self.x1 and self.y2 >= self.y1 and self.z2 >= self.z1
        return (
            max(0, min(self.x2, 50) - max(self.x1, -50) + 1)
            * max(0, min(self.y2, 50) - max(self.y1, -50) + 1)
            * max(0, min(self.z2, 50) - max(self.z1, -50) + 1)
        )


def intersects(a: Cuboid, b: Cuboid):
    f = lambda a1, a2, b1, b2: b2 < a1 or a2 < b1
    return not (
        f(a.x1, a.x2, b.x1, b.x2)
        or f(a.y1, a.y2, b.y1, b.y2)
        or f(a.z1, a.z2, b.z1, b.z2)
    )


def split(a: Cuboid, b: Cuboid):
    if not intersects(a, b):
        return [a]

    x1 = a.x1
    x2 = max(x1, b.x1)
    x4 = a.x2
    x3 = min(x4, b.x2)
    y1 = a.y1
    y2 = max(y1, b.y1)
    y4 = a.y2
    y3 = min(y4, b.y2)
    z1 = a.z1
    z2 = max(z1, b.z1)
    z4 = a.z2
    z3 = min(z4, b.z2)

    return [
        Cuboid(u1, u2, v1, v2, w1, w2)
        for u1, u2, v1, v2, w1, w2 in [
            (x1, x2 - 1, y1, y4, z1, z4),
            (x3 + 1, x4, y1, y4, z1, z4),
            (x2, x3, y1, y2 - 1, z1, z4),
            (x2, x3, y3 + 1, y4, z1, z4),
            (x2, x3, y2, y3, z1, z2 - 1),
            (x2, x3, y2, y3, z3 + 1, z4),
        ]
        if u1 <= u2 and v1 <= v2 and w1 <= w2
    ]


s = getinput(22).strip()
g = []
for l in s.splitlines():
    x1, x2, y1, y2, z1, z2 = map(int, re.findall(r"-?\d+", l))
    p = Cuboid(x1, x2, y1, y2, z1, z2)
    on = l[:2] == "on"
    gg = []
    for c in g:
        gg += split(c, p)
    if on:
        gg.append(p)
    g = gg
print(sum(p.volume50() for p in g))
print(sum(p.volume() for p in g))
