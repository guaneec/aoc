from .util import getinput, Machine
import re

s = getinput(17)
c = [int(x) for x in s.strip().split(',')]
m = Machine(c)
m.run()
o = ""
for c in m.oq:
    o += chr(c)

a = []
d = set()
z0 = None
o0 = None

for (i, l) in enumerate(o.splitlines()):
    for (j, c) in enumerate(l):
        if c == '#':
             d.add((i,j))
        elif c in '^V<>':
            z0 = j + i*1j
            o0 = { '^': (-1j), 'v': (1j), '<': -1, '>': 1 }[c]

zz = set((x,y) for (x,y) in d if all( z in d for z in [(x+1,y), (x-1,y), (x,y+1), (x,y-1)] ))
print(sum(x*y for (x,y) in zz))

m = Machine([int(x) for x in s.strip().split(',')])
m.resume()
m.oq.clear()

print(len(d))

print(z0, o0)

def show(d, z, ori):
    out = []
    while True:
        steps = 0
        while (z + ori) in d:
            steps += 1
            z += ori
        if steps > 0:
            out.append(steps)
        
        if (z + ori * 1j) in d:
            out.append('R')
            ori = ori*1j
        elif (z + ori * -1j) in d:
            out.append('L')
            ori = ori*-1j
        else:
            break

# show( { x+y*1j for (y, x) in d },  z0, o0 )


m = Machine([int(x) for x in s.strip().split(',')])
m.code[0] = 2
m.resume()
print( ''.join([chr(c) for c in m.oq]) )
m.oq.clear()
for h in 'A,A,C,B,B,A,C,B,A,C\n':
    m.iq.append(ord(h))
m.resume()
print( ''.join([chr(c) for c in m.oq]) )
m.oq.clear()
for h in 'L,12,L,12,R,12\n':
    m.iq.append(ord(h))
m.resume()
print( ''.join([chr(c) for c in m.oq]) )
m.oq.clear()
for h in 'L,10,R,8,R,12\n':
    m.iq.append(ord(h))
m.resume()
print( ''.join([chr(c) for c in m.oq]) )
m.oq.clear()
for h in 'L,8,L,8,R,12,L,8,L,8\n':
    m.iq.append(ord(h))
m.resume()
print( ''.join([chr(c) for c in m.oq]) )
m.oq.clear()
for h in 'n\n':
    m.iq.append(ord(h))
print(len(m.oq))
m.resume()
print( ''.join([chr(c) for c in list(m.oq)[:-1]]) )
print(m.oq[-1])
