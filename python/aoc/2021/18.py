from functools import reduce
from .util import getinput
from dataclasses import dataclass
from typing import Tuple
from itertools import permutations
from math import prod


@dataclass
class Leaf:
    path: Tuple[bool]
    val: int

    def __repr__(self) -> str:
        return f'{self.val}@{len(self.path)}'

def flatten(t, path=tuple()):
    a, b = t
    match a:
        case _, _:
            yield from flatten(a, path + (True,))
        case _:
            yield Leaf(path + (True,), a)
    match b:
        case _, _:
            yield from flatten(b, path + (False,))
        case _:
            yield Leaf(path + (False,), b)

def explode(f):
    for i in range(len(f) - 1):
        l, r = f[i], f[i+1]
        if l.path[-1] and not r.path[-1] and len(r.path) > 4:
            if i > 0:
                f[i-1].val += l.val
            if i+2 < len(f):
                f[i+2].val += r.val
            return f[:i] + [Leaf(l.path[:-1], 0)] + f[i+2:], True
    return f, False

def split(f):
    for i in range(len(f)):
        x = f[i]
        if x.val >= 10:
            ll = Leaf(x.path + (True,), x.val // 2)
            lr = Leaf(x.path + (False,), (x.val + 1) // 2)
            return f[:i] + [ll, lr] + f[i+1:], True
    return f, False

def add(fa, fb):
    for x in fa:
        x.path = (True,) + x.path
    for x in fb:
        x.path = (False,) + x.path
    return fa + fb

def red(f):
    while True:
        f, done = explode(f)
        if done:
            continue
        f, done = split(f)
        if not done:
            return f

def mag(f):
    return sum(x.val * prod([2, 3][lr] for lr in x.path) for x in f)

s = getinput(18)
fs = map(lambda l: list(flatten(eval(l))), s.splitlines())
print(mag(reduce(lambda a, b: red(add(a, b)), fs)))

print(max(
    mag(red(add(list(flatten(ta)), list(flatten(tb)))))
    for ta, tb in permutations(map(eval, s.splitlines()), 2)
))