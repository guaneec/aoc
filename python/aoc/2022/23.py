from .util import getinput
from collections import Counter
from itertools import count

s = getinput(23)
s = s.splitlines()
e0 = { i+1j*j for i, row in enumerate(s) for j, c in enumerate(row) if c == '#'}
dirs = (-1,1,-1j,1j) * 2
def move(elves, elf, t):
    if sum(elf+i+j*1j in elves for i in (-1,0,1) for j in (-1,0,1)) == 1:
        return elf
    for d in dirs[t%4:][:4]:
        ee = elf + d
        if ee not in elves and (
            ((1+d+elf) not in elves and (-1+d+elf) not in elves) if d.real == 0 
            else ((1j+d+elf) not in elves and (-1j+d+elf) not in elves)):
            return ee
    return elf

def f(elves, t):
    a = [(e, move(elves, e, t)) for e in elves]
    c = Counter(ee for _, ee in a)
    return {ee if c[ee] == 1 else e for e, ee in a}

elves = e0
for i in range(10):
    elves = f(elves, i)
    
rmn = min(e.real for e in elves)
rmx = max(e.real for e in elves)
imn = min(e.imag for e in elves)
imx = max(e.imag for e in elves)
print(int((rmx-rmn+1)*(imx-imn+1)) - len(elves))

elves = e0
for i in count():
    pe = elves
    elves = f(elves, i)
    if pe == elves:
        print(i+1)
        break
