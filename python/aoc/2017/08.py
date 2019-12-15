from collections import defaultdict

from .util import getinput

s = getinput(8)

vars = defaultdict(int)

ls = s.splitlines()
mm = 0

for l in ls:
    x, op, d, _, y, cmp, i = l.split(' ')
    if  (cmp == '>' and vars[y] > int(i)
    or cmp == '<' and vars[y] < int(i)
    or cmp == '==' and vars[y] == int(i)
    or cmp == '>=' and vars[y] >= int(i)
    or cmp == '<=' and vars[y] <= int(i)
    or cmp == '!=' and vars[y] != int(i)):
        if op == 'inc': vars[x] += int(d)
        if op == 'dec': vars[x] -= int(d)
        mm = max(vars[x], mm)

print(max(v for v in vars.values()))
print(mm)
