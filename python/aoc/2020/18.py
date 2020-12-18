from .util import getinput
import re

s = getinput(18)


class N:
    def __init__(self, v):
        self.v = v

    def __truediv__(self, other):
        return N(self.v + other.v)

    def __add__(self, other):
        return N(self.v + other.v)

    def __sub__(self, other):
        return N(self.v * other.v)


def calc(s, part):
    s = re.sub(r"\*", "-", s)
    if part == 2:
        s = re.sub(r"\+", "/", s)
    s = re.sub(r"(\d+)", r"N(\1)", s)
    return eval(s).v


print(sum(calc(l, 1) for l in s.splitlines()))
print(sum(calc(l, 2) for l in s.splitlines()))
