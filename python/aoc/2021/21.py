from functools import reduce
import functools
from .util import getinput
from dataclasses import dataclass
from typing import *
from math import *
from collections import *
from itertools import permutations, product
import numpy as np
from functools import cache

s = """Player 1 starting position: 4
Player 2 starting position: 8"""

s = [0, 0]
x0 = [1, 5]
x = [*x0]
turn = 0
rolled = 0


def die():
    global rolled
    while True:
        for i in range(1, 101):
            rolled += 1
            yield i


it = iter(die())
while True:
    x[turn] += sum(next(it) for _ in range(3))
    x[turn] -= 1
    x[turn] %= 10
    x[turn] += 1
    s[turn] += x[turn]
    if s[turn] >= 1000:
        break
    turn = 1 - turn
print(s[1 - turn] * rolled)

c = Counter(1 + a + 1 + b + 1 + c for a in range(3) for b in range(3) for c in range(3))


@functools.cache
def f(x1, x2, s1, s2):
    if s2 >= 21:
        return 0, 1
    if s1 >= 21:
        return 1, 0
    w1, w2 = 0, 0
    for k, v in c.items():
        y1 = ((x1 + k) - 1) % 10 + 1
        q2, q1 = f(x2, y1, s2, s1 + y1)
        w1 += v * q1
        w2 += v * q2
    return w1, w2


print(max(f(*x0, 0, 0)))
