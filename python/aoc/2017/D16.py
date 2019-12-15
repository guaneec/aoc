from .util import getinput

def dancex(ps, i, j):
    i, j = min(i, j), max(i, j)
    return ps[:i]+ps[j]+ps[i+1:j]+ps[i]+ps[j+1:]

def domoves(moves, ps):
    n = len(ps)
    for d in moves:
        if d[0] == 's':
            x = int(d[1:])
            ps = ps[n-x:] + ps[:n-x]
        if d[0] == 'x':
            si, sj = d[1:].split('/')
            i, j = int(si), int(sj)
            ps = dancex(ps, i, j)
        if d[0] == 'p':
            a, b = d[1:].split('/')
            i, j = ps.find(a), ps.find(b)
            ps = dancex(ps, i, j)
    return ps

if __name__ == "__main__":
    s = getinput(16)
    ps = 'abcdefghijklmnop'
    moves = s.strip().split(',')


    print(domoves(moves, ps))
    # 30 by inpection
    for i in range(1000000000 % 30):
        ps = domoves(moves, ps)
    print(ps)
