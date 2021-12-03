from .util import getinput

lines = getinput(3).splitlines()
xs = map(int, lines)

s = 0
n = len(lines)
m = len(lines[0])
cs = [0] * len(lines[0])
for l in lines:
    for i, x in enumerate(l):
        cs[i] += l[i] == '1'
    
gamma = int(''.join(str(+(x > n - x)) for x in cs), base=2)
eps = int(''.join(str(+(x < n - x)) for x in cs), base=2)



print(gamma * eps)



lo = [*lines]
for i in range(n):
    c = sum(l[i] == '1' for l in lo)
    b = '1' if c >= len(lo) - c else '0'
    lo = [l for l in lo if l[i] == b]
    if len(lo) == 1:
        break
ox = int(lo[0], base=2)
lo = [*lines]
for i in range(n):
    c = sum(l[i] == '0' for l in lo)
    b = '0' if c <= len(lo) - c else '1'
    lo = [l for l in lo if l[i] == b]
    if len(lo) == 1:
        break
co = int(lo[0], base=2)
print(ox * co)