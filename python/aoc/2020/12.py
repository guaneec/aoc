from .util import getinput

s = getinput(12)


def move(command, x, y, p):
    d, i = command[0], int(command[1:])

    if d == "N" or d == "F" and p == 0:
        return x, y + i, p
    if d == "S" or d == "F" and p == 180:
        return x, y - i, p
    if d == "E" or d == "F" and p == 90:
        return x + i, y, p
    if d == "W" or d == "F" and p == 270:
        return x - i, y, p
    if d == "L":
        return x, y, (p - i + 360) % 360
    if d == "R":
        return x, y, (p + i + 360) % 360
    assert False


x, y, p = 0, 0, 90

for l in s.splitlines():
    x, y, p = move(l, x, y, p)

print(abs(x) + abs(y))


def move2(command, x, y, dx, dy):
    d, i = command[0], int(command[1:])

    if d == "N":
        return x, y, dx, dy + i
    if d == "S":
        return x, y, dx, dy - i
    if d == "E":
        return x, y, dx + i, dy
    if d == "W":
        return x, y, dx - i, dy
    if d in "LR":
        p = (i * [-1, 1][d == "R"] + 360) % 360
        if p == 0:
            return x, y, dx, dy
        if p == 90:
            return x, y, dy, -dx
        if p == 180:
            return x, y, -dx, -dy
        if p == 270:
            return x, y, -dy, dx
        assert False
    if d == "F":
        return x + i * dx, y + i * dy, dx, dy
    assert False


x, y, dx, dy = 0, 0, 10, 1

for l in s.splitlines():
    x, y, dx, dy = move2(l, x, y, dx, dy)

print(abs(x) + abs(y))
