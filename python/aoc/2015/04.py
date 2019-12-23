from .util import getinput
from hashlib import md5
from itertools import count
import doctest

def mymd5(s):
    return md5(bytes(s, 'utf-8')).hexdigest()

def p1(s):
    """
    First digits suffix to generate md5 hash with 5 leading zeros 
    >>> p1('abcdef')
    609043
    >>> p1('pqrstuv')
    1048970
    """
    for i in count(1):
        if mymd5(s + str(i))[:5] == '00000':
            return i

def p2(s):
    for i in count(1):
        if mymd5(s + str(i))[:6] == '000000':
            return i


doctest.testmod()

s = getinput(4).strip()
print(p1(s))
print(p2(s))

