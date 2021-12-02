from .util import getinput

lines = getinput(2).splitlines()

h1, d1, h2, d2, a = 0, 0, 0, 0, 0

for l in lines:
    c, x = l.split()
    x = int(x)
    match c[0]:
        case 'f':
            h1 += x
            h2 += x
            d2 += a * x
        case 'd':
            d1 += x
            a += x
        case 'u':
            d1 -= x
            a -= x
print(h1 * d1)
print(h2 * d2)
