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
    return ''.join(str(z) for z in sayi(int(x) for x in s))

def sayi(nums):
    o = []
    for k, g in groupby(nums):
        o.append(len(list(g)))
        o.append(k)
    return o
    

doctest.testmod()

s = getinput(10).strip()
nums = [int(x) for x in s]
for _ in range(40):
    nums = sayi(nums)

print(len(nums))

for _ in range(10):
    nums = sayi(nums)
    
print(len(nums))
