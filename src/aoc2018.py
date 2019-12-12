from collections import deque


class Machine:
    @staticmethod
    def parse_op(op):
        return (op % 100, (op // 100 % 10, op // 1000 % 10, op // 10000 % 10))

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
            op, modes = self.parse_op(self.code[self.ptr])
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
