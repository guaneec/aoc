from .util import getinput
from collections import defaultdict

s = getinput(7).strip()
files = {}
p = []
for l in s.splitlines():
    a = l.split()
    if a[:2] == ['$', 'cd']:
        if a[-1] == '/':
            p = []
        elif a[-1] == '..':
            p.pop()
        else:
            p.append(a[-1])
    elif a[:2] == ['$', 'ls'] or a[0] == 'dir':
        pass
    else:
        files[tuple(p + [a[1]])] = int(a[0])
dirs = defaultdict(int)
for k, v in files.items():
    for i in range(len(k)):
        dirs[k[:i]] += v
print(sum(v for v in dirs.values() if v <= 1e5))
print(min(v for v in dirs.values() if 70000000 - dirs[tuple()] + v >= 30000000))