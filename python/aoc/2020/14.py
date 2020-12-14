from .util import getinput
import re
from collections import defaultdict

s = getinput(14)


def masked(orig, target, mask):
    return "".join(c if m == "X" else m for c, m in zip(target, mask))

def mask2(orig, mask):
    return "".join(c if m == '0' else m for c, m in zip(f'{orig:036b}', mask))

def all_addr(mask):
    if not mask:
        yield ''
        return
    c = mask[-1]
    for head in all_addr(mask[:-1]):
        if c != '0':
            yield head + '1'
        if c != '1':
            yield head + '0'


mem = defaultdict(lambda: "0" * 36)
for l in s.splitlines():
    s1, _, s2 = l.partition(" = ")
    if s1 == "mask":
        mask = s2
    else:
        addr, val = re.match(r"^mem\[(\d+)\] = (\d+)$", l).groups()
        val = f"{int(val):0>36b}"
        mem[addr] = masked(mem[addr], val, mask)

print(sum(int(x, base=2) for x in mem.values()))


mem = defaultdict(int)
for l in s.splitlines():
    s1, _, s2 = l.partition(" = ")
    if s1 == "mask":
        mask = s2
    else:
        addr, val = re.match(r"^mem\[(\d+)\] = (\d+)$", l).groups()
        addr, val = int(addr), int(val)
        for a in all_addr(mask2(addr, mask)):
            mem[a] = val
print(sum(mem.values()))
