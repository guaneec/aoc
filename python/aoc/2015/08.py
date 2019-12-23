from .util import getinput
import doctest

p1t = '''
""
"abc"
"aaa\\"aaa"
"\\x27"
'''

def p1(s):
    '''
    >>> p1(p1t)
    12
    '''
    f = lambda s: len(s) - len(eval(s))
    return sum(f(l.strip()) for l in s.strip().splitlines())

def p2(s):
    '''
    >>> p2(p1t)
    19
    '''
    f = lambda s: len(repr(s)) + sum(c == '"' for c in s) - len(s)
    return sum(f(l.strip()) for l in s.strip().splitlines())


doctest.testmod()
s = getinput(8)
print(p1(s))
print(p2(s))
