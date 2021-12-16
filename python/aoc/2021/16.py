from .util import getinput
from math import prod
from heapq import *

s = getinput(16).strip()

def be(bits):
    o = 0
    for b in bits:
        o = o * 2 + b
    return o

def tobits(h):
    for c in h:
        for i in range(3, -1, -1):
            yield int(c, base=16) >> i & 1

def read_lit(it):
    o = 0
    l = 0
    while True:
        a = [next(it) for _ in range(5)]
        l += 5
        o = o * 16 + be(a[1:])
        if not a[0]:
            return l, o


def read_op(it):
    i = next(it)
    l = 1
    vds = []
    if i == 0:
        m = be(next(it) for _ in range(15))
        l += 15
        while m > 0:
            ll, vd = read_packet(it)
            vds.append(vd)
            l += ll
            m -= ll
        assert(m == 0)
    else:
        m = be(next(it) for _ in range(11))
        l += 11
        for _ in range(m):
            ll, vd = read_packet(it)
            vds.append(vd)
            l += ll
    return l, vds
    

def read_packet(it):
    v = be(next(it) for _ in range(3))
    t = be(next(it) for _ in range(3))
    if t == 4:
        l, d = read_lit(it)
    else:
        l, d = read_op(it)
    return l + 6, (v, t, d)

def packet_sum(vps):
    v, _, ps = vps
    match ps:
        case [*ps]:
            return v + sum(packet_sum(p) for p in ps)
        case _:
            return v

def packet_eval(vps):    
    match vps[1:]:
        case 0, ps:
            return sum(packet_eval(p) for p in ps)
        case 1, ps:
            return prod(packet_eval(p) for p in ps)
        case 2, ps:
            return min(packet_eval(p) for p in ps)
        case 3, ps:
            return max(packet_eval(p) for p in ps)
        case 4, p:
            return p
        case 5, (p1, p2):
            return packet_eval(p1) > packet_eval(p2)        
        case 6, (p1, p2):
            return packet_eval(p1) < packet_eval(p2)
        case 7, (p1, p2):
            return packet_eval(p1) == packet_eval(p2)
        

l, vps = read_packet(tobits(s))
print(packet_sum(vps))
print(packet_eval(vps))