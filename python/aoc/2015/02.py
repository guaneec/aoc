from .util import getinput
import re


def wp(s):
    l, w, h = map(int, re.findall('\d+', s))
    return 2*l*w + 2*w*h + 2*h*l + min((l*w, w*h, h*l))

def rb(s):
    l, w, h = map(int, re.findall('\d+', s))
    return l*w*h + 2*(l+w+h) - 2 * max((l, w, h))


assert(wp('2x3x4') == 58)
assert(wp('1x1x10') == 43)

assert(rb('2x3x4') == 34)
assert(rb('1x1x10') == 14)

s = getinput(2)

print(sum(wp(l) for l in s.strip().splitlines()))
print(sum(rb(l) for l in s.strip().splitlines()))
