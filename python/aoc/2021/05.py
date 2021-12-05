from .util import getinput

s = getinput(5)

def parse(l):
    a, b = l.split(' -> ')
    q, w = map(int, a.split(','))
    e, r= map(int, b.split(','))
    return q, w, e, r

lines = [parse(l) for l in s.splitlines()]

m = max(max(a, b) for (a, _, b, _) in lines)
n = max(max(a, b) for (_, a, _, b) in lines)


for diag in (0, 1):
    grid = [[0] * (n + 1) for _ in range(m + 1)]    
    for a, b, c, d in lines:
        if a == c:
            b, d = sorted([b, d])
            for i in range(b, d+1):
                grid[a][i] += 1
        elif b == d:
            a, c = sorted([a, c])
            for i in range(a, c+1):
                grid[i][b] += 1
        elif diag and a - c == b - d:
            a, c = sorted([a, c])
            b, d = sorted([b, d])
            for i in range(c - a + 1):
                grid[a + i][b + i] += 1
        elif diag and a - c == d - b:
            a, c = sorted([a, c])
            b, d = sorted([b, d])
            for i in range(c - a + 1):
                grid[a + i][d - i] += 1
    print(sum(sum(x > 1 for x in l) for l in grid))
