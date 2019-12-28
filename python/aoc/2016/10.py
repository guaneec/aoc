from .util import getinput
from collections import defaultdict
from functools import reduce
import re


s = getinput(10)

bots = defaultdict(lambda: {
    'high': None,
    'low': None,
    'chips': [],
})

def trygive(bots, b):
    bb = bots[b]
    if len(bb['chips']) == 2 and bb['high'] is not None and bb['low'] is not None:
        while bb['chips']:
            l, h = min(bb['chips']), max(bb['chips'])
            bb['chips'] = []
            bots[bb['low']]['chips'].append(l)
            bots[bb['high']]['chips'].append(h)
            if (l, h) == (17, 61):
                print(b[4:])
            while trygive(bots, bb['low']) or trygive(bots, bb['high']):
                pass
        return True
    else:
        return False
        

for l in s.strip().splitlines():
    if "goes to" in l:
        v, b = re.match(r'value (\d+) goes to (bot \d+)', l).group(1, 2)
        bots[b]['chips'].append(int(v))
        trygive(bots, b)
    elif 'gives low to' in l:
        b, bol, boh = re.match(r'^(bot \d+) gives low to (.+) and high to (.+)$', l).group(1, 2, 3)
        bots[b]['low'] = bol
        bots[b]['high'] = boh
        trygive(bots, b)
    else:
        assert(False)

prod = lambda l: reduce(lambda a, b: a*b, l)
print(prod(prod(bots[f'output {i}']['chips']) for i in range(3)))
