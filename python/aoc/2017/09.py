from collections import defaultdict

from .util import getinput

s = getinput(9)

garb = False
cancel = False
group = 0
total = 0
ngarb = 0

for c in s:
    if cancel:
        cancel = False
        continue
    if garb:
        if c == '!':
            cancel = True
            continue
        if c == '>':
            garb = False
            continue
        ngarb += 1
        continue
    if c == '<':
        garb = True
        continue
    if c == '{':
        group += 1
        total += group
    if c == '}':
        group -= 1

print(total)
print(ngarb)
