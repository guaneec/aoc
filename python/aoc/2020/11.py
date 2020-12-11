from .util import getinput

s = '''\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
'''
s = getinput(11)

a = [list(x) for x in s.splitlines()]

def step(x, prob):
    n = len(x)
    m = len(x[0])
    def adj1(i, j):
        for p, q in [ (i+1, j), (i-1, j), (i, j-1), (i, j+1), (i+1,j+1), (i-1,j+1), (i-1, j-1), (i+1, j-1) ]:
            if 0 <= p < n and 0 <= q < m:
                yield p, q
    
    def adj2(i, j):
        for dx, dy in [ (1, 1), (1, 0), (1, -1), (-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1) ]:
            p, q = i + dx, j + dy
            while 0 <= p < n and 0 <= q < m:
                if x[p][q] != '.':
                    yield p, q
                    break
                p, q = p + dx, q + dy
    
    adj = adj1 if prob == 1 else adj2
    thres = 4 if prob == 1 else 5

    return [[('#' if x[i][j] == 'L' and not any( x[p][q] == '#' for p, q in adj(i, j) )
            else 'L' if x[i][j] == '#' and thres <= sum( x[p][q] == '#' for p, q in adj(i, j) )
            else x[i][j])
        for j in range(m)] for i in range(n)]

def show(x):
    print('\n'.join(  ''.join(l) for l in x ))
    print()

p, n = a, step(a, 1)
while p != n:
    p, n = n, step(n, 1)
    # show(p)

print(sum(l.count('#') for l in p))

p, n = a, step(a, 2)
while p != n:
    p, n = n, step(n, 2)
    # show(p)

print(sum(l.count('#') for l in p))