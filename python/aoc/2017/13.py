from .util import getinput

s = getinput(13)
d = {}
sev = 0

nums = []
for l in s.strip().splitlines():
    sa, sb = l.split(':')
    a, b = int(sa), int (sb)
    nums.append((a,b))
    if a % (2*b-2) == 0:
        sev += a*b

def good(l, delay):
    return all((a+delay) % (2*b-2) != 0 for (a,b) in l)

print(sev)
for i in range(10000000):
    if good(nums, i):
        print(i)
        break
