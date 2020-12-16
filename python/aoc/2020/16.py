from .util import getinput
import re
from functools import reduce, lru_cache

s = getinput(16)

s1, s2, s3 = s.split("\n\n")
ranges = [list(int(x.group()) for x in re.finditer(f"\d+", l)) for l in s1.splitlines()]
fields = [list(int(x) for x in l.split(",")) for l in s2.splitlines()[1:]] + [
    list(int(x) for x in l.split(",")) for l in s3.splitlines()[1:]
]
print(
    sum(
        sum(
            f for f in t if not any(a <= f <= b or c <= f <= d for a, b, c, d in ranges)
        )
        for t in fields
    )
)

fields = [
    t
    for t in fields
    if all(any(a <= f <= b or c <= f <= d for a, b, c, d in ranges) for f in t)
]


@lru_cache(None)
def val(x, y):
    a, b, c, d = ranges[x]
    valid = lambda t: a <= t[y] <= b or c <= t[y] <= d
    return all(valid(t) for t in fields)


def match(seq: list, remaining: set):
    for x in remaining:
        if val(x, len(seq)):
            seq.append(x)
            remaining.remove(x)
            if not remaining:
                yield tuple(seq)
            else:
                yield from match(seq, remaining)
            seq.pop()
            remaining.add(x)


seq = next(match([], set(range(len(fields[0])))))
print(reduce(lambda a, b: a * b, (fields[0][i] for i, x in enumerate(seq) if x < 6), 1))
