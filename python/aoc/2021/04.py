from .util import getinput

s = getinput(4)
parts = s.split('\n\n')

seq = list(map(int, parts[0].split(',')))

def parse(b):
    return [[int(x) for x in l.split()] for l in b.splitlines()]

boards = [parse(b) for b in parts[1:]]


print(seq)
print(boards[0])

marks = [[[0] * 5 for _ in range(5)] for _ in boards]
print(marks[0])

def find(board, x):
    for i in range(5):
        for j in range(5):
            if board[i][j] == x:
                return i, j
    return -1, -1

def winning():
    won = [0] * len(boards)
    rem = len(boards)
    for x in seq:
        for k, (m, b) in enumerate(zip(marks, boards)):
            i, j = find(b, x)
            if i < 0:
                continue
            m[i][j] = 1
            if (any(sum(m[i][j] for i in range(5)) == 5 for j in range(5)) or
                any(sum(m[i][j] for j in range(5)) == 5 for i in range(5))):
                if won[k]:
                    continue
                if rem == 1:
                    return m, b, x
                won[k] = 1
                rem -= 1

m, b, x = winning()
score = sum(sum((1 - mm)*bb for mm, bb in zip(rm, rb)) for rm, rb in zip(m, b))
print(score * x)


