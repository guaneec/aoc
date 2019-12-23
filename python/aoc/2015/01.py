from .util import getinput


def p1(s):
    return sum((c == '(') * 2 - 1 for c in s)

p1t = [
    ('(())', 0),
    ('()()', 0),
    ('(((', 3),
    ('(()(()(', 3),
    ('))(((((', 3),
    ('())', -1),
    ('))(', -1),
    (')))', -3),
    (')())())', -3),
]

for tc, tr in p1t:
    assert(p1(tc) == tr)

def p2(s):
    floor = 0
    for i, c in enumerate(s):
        floor += (c == '(') * 2 - 1 
        if floor == -1:
            return i + 1

p2t = [
    (')', 1),
    ('()())', 5),
]

for tc, tr in p2t:
    assert(p2(tc) == tr)

s = getinput(1)

print(p1(s))
print(p2(s))
