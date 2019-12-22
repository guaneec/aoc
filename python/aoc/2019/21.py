from .util import getinput, Machine
from itertools import count
import re

s = getinput(21)
c = [int(x) for x in s.strip().split(',')]

m = Machine(c)

'''
Jump if you can land safely and there's hole in ABC
D AND NOT (A AND B AND C)
'''

program = '''
NOT J T
AND T J
AND J T
OR D J
OR A T
AND B T
AND C T
NOT T T
AND T J
WALK
'''

m.readLines(program)
m.interact()

m = Machine(c)

'''
Jump if you can land safely and there's hole in ABC and can jump again
'''

program = '''
NOT J T
AND T J
AND J T
OR D J
OR A T
AND B T
AND C T
NOT T T
AND T J
NOT E T
NOT T T
OR H T
AND T J
RUN
'''

m.readLines(program)
m.interact()
