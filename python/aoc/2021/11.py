from .util import getinput
import numpy as np
from scipy.signal import convolve2d
from itertools import count

s = getinput(11)
grid = np.array([[int(x) for x in line] for line in s.splitlines()])
kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

def step(grid):
    flashed = np.zeros_like(grid, dtype=bool)
    grid += 1
    while True:
        mask = (grid * (1 - flashed)) > 9
        if not np.any(mask):
            break
        flashed |= mask
        grid += convolve2d(mask, kernel, 'same')
    grid *= 1 - flashed
    return grid, flashed

g1 = np.copy(grid)
p1 = 0
for _ in range(100):
    g1, flashed = step(g1)
    p1 += np.sum(flashed)
print(p1)

g2 = np.copy(grid)
for i in count():
    g2, flashed = step(g2)
    if np.all(flashed):
        print(i + 1)
        break
