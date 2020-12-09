from .util import getinput

s = getinput(9)

m = 25

a = [int (x) for x in s.splitlines()]

def issum(a, target):
    n = len(a)
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] + a[j] == target:
                return True
    return False

for i, x in enumerate(a[m:]):
    if not issum(a[i:i+m], x):
        a1 = x
        print(x)

cumsum = []
s = 0
for x in a:
    s += x
    cumsum.append(s)

for i in range(len(a)):
    for j in range(i+2, len(a)):
        if cumsum[j] - cumsum[i] == a1:
            print(min(a[i+1:j])+max(a[i+1:j]))

