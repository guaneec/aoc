from .util import getinput

s = getinput(3).strip()

p1 = 0
for l in s.splitlines():
    n = len(l) // 2
    a, b = l[:n], l[n:]
    x = next(iter(set(a) & set(b)))
    p1 += 1 + ord(x.lower()) - ord('a') + 26 * x.isupper()
print(p1)

ss = s.splitlines()
p2 = 0
for x, y, z in zip(ss[::3], ss[1::3], ss[2::3]):
    x = next(iter(set(x) & set(y) & set(z)))
    p2 += 1 + ord(x.lower()) - ord('a') + 26 * x.isupper()
print(p2)