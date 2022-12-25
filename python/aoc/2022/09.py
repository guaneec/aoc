from .util import getinput

s = getinput(9)

for n in (2, 10):
    knots = [(0, 0)] * n
    tt = {(0, 0)}
    for l in s.splitlines():
        a, b = l.split()
        dy = (a == 'U') - (a == 'D')
        dx = (a == 'L') - (a == 'R')
        for _ in range(int(b)):
            knots[0] = (knots[0][0] + dx, knots[0][1] + dy)
            for i in range(len(knots) - 1):
                hx, hy = knots[i]
                tx, ty = knots[i+1]
                while max(abs(hx-tx), abs(hy-ty)) > 1:
                    ty += (hy > ty) - (hy < ty)
                    tx += (hx > tx) - (hx < tx)
                knots[i+1] = (tx, ty)
            tt.add(knots[-1])
    print(len(tt))