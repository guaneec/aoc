import re
from .util import getinput

s = getinput(25)


pre, body = s.split('steps.')

state = pre[15]
n = int(re.findall('\d+', pre)[0])


def parse(p):
    a =  [int(x) for x in re.findall('[01]', p)]
    ss = [x[-1] for x in re.findall('state \w', p)]
    lr = [x[0] == 'r' for x in re.findall('left|right', p)]
    return (ss[0],  (
        (a[1], lr[0]*2-1, ss[1]),
        (a[3], lr[1]*2-1, ss[2]),
    ))
rules =  { k: v for (k, v) in  map(parse, filter(lambda x: x, body.strip().split('In'))) }


x = 0
tape = set()

for i in range(n):
    b = x in tape
    v, lr, s = rules[state][b]
    if v:
        tape.add(x)
    else:
        tape.discard(x)
    
    x += lr
    state = s
print(len(tape))
