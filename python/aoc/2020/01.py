from .util import getinput



a = [int(line) for line in getinput(1).splitlines()]
l = sorted(set(a))

def findsum(l, target):
    i, j = 0, len(l) - 1
    while i < j:
        ss = l[i] + l[j]
        if ss == target:
            return l[i], l[j]
        if ss < target:
            i += 1
        else:
            j -= 1

x1, x2 = findsum(l, 2020)
print(x1 * x2)

for i, x1 in enumerate(l):
    try:
        x2, x3 = findsum(l[i+1:], 2020 - x1)
        print(x1 * x2 * x3)
        break
    except:
        pass