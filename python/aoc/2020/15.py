from .util import getinput

s = '''\
0,3,6
'''
s = getinput(15)
a = [int(x) for x in s.split(',')]

for n in (2020, 30000000):
    d = {}
    for i, x in enumerate(a[:-1]):
        d[x] = i

    x = a[-1]
    for i in range(len(a) - 1, n - 1):
        try:
            y = i - d[x]
        except KeyError:
            y = 0
        d[x] = i
        x = y
    print(x)