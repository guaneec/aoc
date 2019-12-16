from collections import defaultdict

from .util import getinput

s = '''     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ '''

s = getinput(19)
    
board = {  (x, y): c  for (y, l) in enumerate(s.splitlines()) for (x, c) in enumerate(l) }
board = defaultdict(lambda: ' ', board)

x, y = min( x for ((x, y), c) in board.items() if y == 0 and c == '|'), 0
dx, dy = 0, 1

steps = 0
while True:
    c = board[(x, y)]
    if c == ' ':
        break
    elif c.isalpha():
        print(c, end='')
        x, y = x+dx, y+dy
        steps += 1
    elif c in '|-':
        x, y = x+dx, y+dy
        steps += 1
    elif c == '+':
        for (dxx, dyy, cc) in [(1, 0, '-'), (-1, 0, '-'), (0, 1, '|'), (0, -1, '|')]:
            if (-dxx, -dyy) != (dx, dy) and (lambda z: z == cc or z.isalpha())(board[(x+dxx, y+dyy)]):
                dx, dy = dxx, dyy
                x, y = x+dx, y+dy
        steps += 1
    else:
        assert(False)
print()
print(steps)
