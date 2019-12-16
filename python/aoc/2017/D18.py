from collections import defaultdict, deque
from .util import getinput

s = getinput(18)

regs = defaultdict(int)

def f(x):
    try:
        return int(x)
    except ValueError:
        return regs[x]



freq = None
code = [l.split(' ') for l in  s.strip().splitlines()]
i = 0
while True:
    ws = code[i]
    if ws[0] == 'snd':
        freq = f(ws[1])
    elif ws[0] == 'set':
        regs[ws[1]] = f(ws[2])
    elif ws[0] == 'add':
        regs[ws[1]] += f(ws[2])
    elif ws[0] == 'mul':
        regs[ws[1]] *= f(ws[2])
    elif ws[0] == 'mod':
        regs[ws[1]] %= f(ws[2])
    elif ws[0] == 'rcv':
        if f(ws[1]):
            print(freq)
            break
    elif ws[0] == 'jgz':
        if f(ws[1]) > 0:
            i += f(ws[2]) - 1
    else:
        raise Exception('what??')
    i += 1


class Machine:
    def __init__(self, code, pid):
        self.code = code
        self.i = 0
        self.blocked = False
        self.regs = defaultdict(int)
        self.regs['p'] = pid

    def f(self, x):
        try:
            return int(x)
        except ValueError:
            return self.regs[x]


    
    def run(self, iq, oq):
        while True:
            ws = self.code[self.i]
            if ws[0] == 'snd':
                oq.append(self.f(ws[1]))
            elif ws[0] == 'set':
                self.regs[ws[1]] = self.f(ws[2])
            elif ws[0] == 'add':
                self.regs[ws[1]] += self.f(ws[2])
            elif ws[0] == 'mul':
                self.regs[ws[1]] *= self.f(ws[2])
            elif ws[0] == 'mod':
                self.regs[ws[1]] %= self.f(ws[2])
            elif ws[0] == 'rcv':
                if not iq:
                    self.blocked = True
                    return
                self.blocked = False
                self.regs[ws[1]] = iq.popleft()
            elif ws[0] == 'jgz':
                if self.f(ws[1]) > 0:
                    self.i += self.f(ws[2]) - 1
            else:
                raise Exception('what??')
            self.i += 1

class CQueue(deque):
    def __init__(self):
        deque.__init__(self)
        self.total = 0

    def append(self, x):
        deque.append(self, x)
        self.total += 1


ma = Machine(code, 0)
mb = Machine(code, 1)
qab = CQueue()
qba = deque()
while True:
    ma.run(qab, qba)
    mb.run(qba, qab)
    if ma.blocked and mb.blocked and not qab and not qba:
        print(qab.total)
        break
