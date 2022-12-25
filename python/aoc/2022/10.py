from .util import getinput

s = getinput(10)

cycle = 1
x = 1
trace = {}
for l in s.splitlines():
    if l == 'noop':
        trace[cycle] = x
        cycle += 1
    else:
        v = l.split()[-1]
        trace[cycle] = x
        trace[cycle + 1] = x
        x += int(v)
        cycle += 2
print(sum(trace[i] * i for i in range(20, 221, 40)))
for i in range(1, 241):
    x = trace[i]
    print('.#'[(i - 1) % 40 in (x-1, x, x+1)], end='')
    if i % 40 == 0:
        print()