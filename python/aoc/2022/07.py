from .util import getinput
from collections import defaultdict

s = getinput(7).strip()
files = {}
p = []
for l in s.splitlines():
    match l.split():
        case ['$', 'cd', d]:
            if d == '/':
                p = []
            elif d == '..':
                p.pop()
            else:
                p.append(d)
        case ['$', 'ls'] | ['dir', _]:
            pass
        case [a, b]:
            files[tuple(p + [b])] = int(a)
dirs = defaultdict(int)
for k, v in files.items():
    for i in range(len(k)):
        dirs[k[:i]] += v
print(sum(v for v in dirs.values() if v <= 1e5))
print(min(v for v in dirs.values() if 70000000 - dirs[tuple()] + v >= 30000000))