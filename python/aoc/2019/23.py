from .util import getinput, Machine
from itertools import count
import re

s = getinput(23)
c = [int(x) for x in s.strip().split(',')]

def p1(c):
    ms = []
    for i in range(50):
        m = Machine(c)
        m.iq.append(i)
        m.resume()
        ms.append(m)

    while not all(m.halted for m in ms):
        # send
        while any(m.oq for m in ms):
            for i, m in enumerate(ms):
                while m.oq:
                    addr, x, y = m.oq.popleft(), m.oq.popleft(), m.oq.popleft()
                    if addr == 255:
                        return y
                    ms[addr].iq.extend([x, y])
                    ms[addr].resume()
        # receive 
        for i, m in enumerate(ms):
            if not m.halted:
                m.iq.append(-1)
                m.resume()
                if m.oq:
                    break

def p2(c):
    ms = []
    for i in range(50):
        m = Machine(c)
        m.iq.append(i)
        m.resume()
        ms.append(m)

    nat = None
    natys = set()
    while not all(m.halted for m in ms):
        # send
        while any(m.oq for m in ms):
            for i, m in enumerate(ms):
                while m.oq:
                    addr, x, y = m.oq.popleft(), m.oq.popleft(), m.oq.popleft()
                    if addr == 255:
                        nat = (x, y)
                        continue
                    ms[addr].iq.extend([x, y])
                    ms[addr].resume()
        # receive 
        for i, m in enumerate(ms):
            if not m.halted:
                m.iq.append(-1)
                m.resume()
                if m.oq:
                    break
        else:
            if nat[1] in natys:
                return nat[1]
            ms[0].iq.extend(nat)
            natys.add(nat[1])


print(p1(c))
print(p2(c))
