from .util import getinput
import doctest
from json import loads

def jsum(o, red=True):
    """
    >>> jsum([1,2,3])
    6
    >>> jsum({"a":2,"b":4})
    6
    >>> jsum([[[3]]])
    3
    >>> jsum({"a":{"b":4},"c":-1})
    3
    >>> jsum({"a":[-1,1]})
    0
    >>> jsum([-1,{"a":1}])
    0
    >>> jsum([])
    0
    >>> jsum({})
    0
    >>> jsum([1,{"c":"red","b":2},3], False)
    4
    >>> jsum({"d":"red","e":[1,2,3,4],"f":5}, False)
    0
    >>> jsum([1,"red",5], False)
    6
    """
    if type(o) == int:
        return o
    if type(o) == list:
        return sum(jsum(c, red) for c in o)
    if type(o) == dict:
        return sum(jsum(v, red) for v in o.values()) if "red" not in o.values() or red else 0
    else:
        return 0

doctest.testmod()
s = getinput(12).strip()
o = loads(s)
print(jsum(o))
print(jsum(o, False))
