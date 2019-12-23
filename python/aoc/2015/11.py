from .util import getinput
import doctest
from itertools import groupby

def r1(s):
    """
    >>> r1('hijklmmn')
    True
    >>> r1('abbceffg')
    False
    """
    o = [ord(c) for c in s]
    return any( o[i] + 1 == o[i+1] and o[i+1] + 1 == o[i+2] for i in range(0, len(s) - 2))

def r2(s):
    """
    >>> r2('hijklmmn')
    False
    >>> r2('ghjaabaa')
    True
    """
    return all(c not in s for c in 'iol')

def r3(s):
    """
    >>> r3('abbceffg')
    True
    >>> r3('abbcegjk')
    False
    >>> r3('ghjaabcc')
    True
    >>> r3('ghjaabaa')
    False
    """
    return len(set( k for k, g in groupby(s) if len(list(g)) >= 2)) >= 2

def nxt(s):
    """
    >>> nxt('xy')
    'xz'
    >>> nxt('xz')
    'ya'
    >>> nxt('zz')
    'aaa'
    """
    if s == '':
        return 'a'
    if s[-1] != 'z':
        return s[:-1] + chr(ord(s[-1])+1+(s[-1] in 'hnk'))
    return nxt(s[:-1]) + 'a'

def nxtpwd(s):
    """
    >>> nxtpwd('abcdefgh')
    'abcdffaa'
    >>> nxtpwd('ghijklmn')
    'ghjaabcc'
    """
    while not r2(s) or not r1(s) or not r3(s):
        s = nxt(s)
    return s

doctest.testmod()
s = getinput(11).strip()
s = nxtpwd(s)
print(s)
print(nxtpwd(nxt(s)))
