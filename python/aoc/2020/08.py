from .util import getinput
s = getinput(8)
prog = s.splitlines()
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
        l = prog[i]
        a, b = l[:3], int(l[4:])
        if a == 'jmp':
            i += b
        else:
            i += 1
            if a == 'acc':
                acc += b
    return False, acc

print(ex(prog)[1])
for i, l in enumerate(prog):
    prog[i] = l.replace('jmp', 'tmp').replace('nop', 'jmp').replace('tmp', 'nop')
    a, b = ex(prog)
    if a:
        print(b)
    prog[i] = l