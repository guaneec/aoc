from .util import getinput

s = getinput(1)

def dist(z):
    return int(abs(z.real)+abs(z.imag))

turn = {'L': 1j, 'R': -1j}
direction = 1j
pos = 0
poss = {pos}
pos2 = None
for inst in s.strip().split(', '):
    direction *= turn[inst[0]]
    for _ in range(int(inst[1:])):
        pos += direction
        if pos2 is None and pos in poss:
            pos2 = pos
        else:
            poss.add(pos)

print(dist(pos))
print(dist(pos2))


