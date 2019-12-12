from collections import deque
from itertools import permutations

def parse_op(op):
    return (op % 100, (op // 100 % 10, op // 1000 % 10, op // 10000 % 10))

class Machine:
    def __init__(self, code):
        self.code = code
        self.ptr = 0
        self.iq = deque()
        self.oq = deque()
        self.on_wait = lambda: None
    
    def t(self, mode, val):
        return val if mode else self.code[val]
    
    def run(self, n=None, v=None, inp=None):
        if n is not None:
            self.code[1] = n
        if v is not None:
            self.code[2] = v
        if inp is not None:
            for i in inp:
                self.iq.append(i)
        return self.resume()
    
    def resume(self):
        l = len(self.code)
        while self.ptr < l:
            op, modes = parse_op(self.code[self.ptr])
            c = self.code
            if op == 99:
                break
            elif op == 1:
                self.do_add(modes, c[self.ptr+1], c[self.ptr+2], c[self.ptr+3])
                self.ptr += 4
            elif op == 2:
                self.do_mult(modes, c[self.ptr+1], c[self.ptr+2], c[self.ptr+3])
                self.ptr += 4
            elif op == 3:
                if not self.iq:
                    return
                self.code[c[self.ptr+1]] = self.iq.popleft()
                self.ptr += 2
            elif op == 4:
                self.do_output(modes, c[self.ptr+1])
                self.ptr += 2
            elif op == 5:
                if self.t(modes[0], c[self.ptr+1]) != 0:
                    self.ptr = self.t(modes[1], c[self.ptr+2])
                else:
                    self.ptr += 3
            elif op == 6:
                if self.t(modes[0], c[self.ptr+1]) == 0:
                    self.ptr = self.t(modes[1], c[self.ptr+2])
                else:
                    self.ptr += 3
            elif op == 7:
                self.code[c[self.ptr+3]] = self.t(modes[0], c[self.ptr+1]) < self.t(modes[1], c[self.ptr+2])
                self.ptr += 4
            elif op == 8:
                self.code[c[self.ptr+3]] = self.t(modes[0], c[self.ptr+1]) == self.t(modes[1], c[self.ptr+2])
                self.ptr += 4
        return self.oq
    
    def do_add(self, modes, r1, r2, r3):
        self.code[r3] = self.t(modes[0], r1) + self.t(modes[1], r2)
        
    def do_mult(self, modes, r1, r2, r3):
        self.code[r3] = self.t(modes[0], r1) * self.t(modes[1], r2)
    
    def do_output(self, modes, r1):
        self.oq.append(self.t(modes[0], r1))
        
    def do1202(self):
        self.code[1] = 12
        self.code[2] = 2

def argmax(f, xs):
    x0 = next(xs)
    y0 = f(x0)
    for x in xs:
        y = f(x)
        if y > y0:
            x0 = x
            y0 = y
    return x0, y0

def throut(c, ps, i=0):
    o = i
    for p in ps:
        m = Machine(c.copy())
        m.run(inp=[p, o])
        o = m.oq.popleft()
    return o

def throutcl(c, ps, ii=0):
    o = ii
    ms = []
    for (i, p) in enumerate(ps):
        m = Machine(c.copy())
        ms.append(m)
        if i != 0:
            m.iq = ms[i-1].oq
        m.iq.append(p)
    m.oq = ms[0].iq
    ms[0].iq.append(o)
    while True:
        for m in ms:
            m.resume()
        o_new = ms[0].iq[0]
        if o_new == o:
            return o
        o = o_new

c = [3,8,1001,8,10,8,105,1,0,0,21,34,43,60,81,94,175,256,337,418,99999,3,9,101,2,9,9,102,4,9,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,102,4,9,9,1001,9,4,9,102,3,9,9,4,9,99,3,9,102,4,9,9,1001,9,2,9,1002,9,3,9,101,4,9,9,4,9,99,3,9,1001,9,4,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,99]

print(argmax(lambda x: throut(c, x), permutations([0,1,2,3,4])))
print(argmax(lambda x: throutcl(c, x), permutations([5,6,7,8,9])))
