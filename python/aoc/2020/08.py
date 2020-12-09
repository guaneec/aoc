from .util import getinput
s = getinput(8)
prog = s.splitlines()

def runline(line, pc, acc):
    a, b = line[:3], int(line[4:])
    if a == 'jmp':
        return pc + b, acc
    return pc + 1, acc + b if a == 'acc' else acc

def ex(prog):
    run = set()
    i = 0
    acc = 0
    while True:
        if i == len(prog):
            return True, acc
        if i in run:
            break
        run.add(i)
        i, acc = runline(prog[i], i, acc)
    return False, acc

print(ex(prog)[1])

def p2(prog):
    i = 0
    acc = 0
    seen = set()
    while True:
        if prog[i][0] != 'a':
            bak = i, acc, prog[i]
            prog[i] = prog[i].replace('jmp', 'tmp').replace('nop', 'jmp').replace('tmp', 'nop')
            i, acc = runline(prog[i], i, acc)
            while i not in seen:
                seen.add(i)
                i, acc = runline(prog[i], i, acc)
                if i == len(prog):
                    return acc
            i, acc, prog[i] = bak
        i, acc = runline(prog[i], i, acc)

print(p2(prog))
