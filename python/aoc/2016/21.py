from .util import getinput
import re
from itertools import chain, groupby, permutations

s = getinput(21)
ops = s.strip().splitlines()

def swap(s, x, y):
    x, y = min(x, y), max(x, y)
    return s[:x] + s[y:y+1] + s[x+1:y] + s[x:x+1] + s[y+1:]

def rotate(s, i):
    i %= len(s)
    return s[-i:] + s[:-i]

def deperm(s, rf, rt):
    return ''.join(s[rt.index(c)] for c in rf)


def p1(ops, s):
    for op in ops:
        if g := re.match(r'swap position (\d+) with position (\d+)', op):
            x, y = map(int, g.group(1,2))
            s = swap(s, x, y)
        elif g := re.match(r'swap letter (\w) with letter (\w)', op):
            x, y = map(s.index, g.group(1, 2))
            s = swap(s, x, y)
        elif g := re.match(r'rotate (left|right) (\d+) steps?', op):
            s = rotate(s, int(g.group(2)) * ([-1,1][g.group(1) == 'right']) )
        elif g := re.match(r'rotate based on position of letter (\w)', op):
            i = s.index(g.group(1))
            s = rotate(s, i + 1 if i < 4 else i + 2)
        elif g := re.match(r'reverse positions (\d+) through (\d+)', op):
            x, y = map(int, g.group(1,2))
            s = s[:x] + ''.join(reversed(s[x:y+1])) + s[y+1:]
        elif g := re.match(r'move position (\d+) to position (\d+)', op):
            x, y = map(int, g.group(1,2))
            c = s[x]
            s = s[:x] + s[x+1:]
            s = s[:y] + c + s[y:]
        else:
            assert(False)
    return s
sf = 'abcdefgh'
st = p1(ops, sf)
print(st)
for sf in permutations('abcdefgh'):
    sf = ''.join(sf)
    if p1(ops, sf) == 'fbgdceah':
        print(sf)
        break
