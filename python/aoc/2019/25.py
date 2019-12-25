from .util import getinput, Machine
from itertools import chain, combinations
import re

s = getinput(25)
c = [int(x) for x in s.strip().split(',')]
m = Machine(c)

inp = """east
east
south
take monolith
north
east
take shell
west
west
north
west
take bowl of rice
east
inv
north
take planetoid
west
take ornament
south
south
take fuel cell
north
north
east
east
take cake
south
west
north
take astrolabe
west
inv
"""

def ainp(m, s):
    m.iq.extend(ord(c) for c in s)
    m.iq.append(10)

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

ainp(m, inp)

items = ['monolith', 'bowl of rice', 'ornament', 'shell', 'astrolabe', 'planetoid', 'fuel cell', 'cake']

for p in powerset(items):
    for i in items:
        ainp(m, f'drop {i}')
    for i in p:
        ainp(m, f'take {i}')
    ainp(m, 'north')
    m.oq.clear()
    m.resume()
    out = ''.join(chr(c) for c in m.oq)
    if 'heavier' not in out and 'lighter' not in out:
        break

m.interact()
