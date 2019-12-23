from .util import getinput
import doctest
from itertools import groupby

def say(s):
    """
    >>> say('1')
    '11'
    >>> say('11')
    '21'
    >>> say('21')
    '1211'
    >>> say('1211')
    '111221'
    >>> say('111221')
    '312211'
    """
    o = ''
    for k, g in groupby(s):
        o += f'{len(list(g))}{k}'
    return o

doctest.testmod()

s = getinput(10).strip()
for _ in range(40):
    s = say(s)

print(len(s))

for _ in range(10):
    s = say(s)
    
print(len(s))
