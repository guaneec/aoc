from .util import getinput
from .D10 import knothash

bitsum = lambda x: sum(y == '1' for y in bin(x))

if __name__ == "__main__":    
    s = getinput(14).strip()
    seeds = (f'{s}-{i}' for i in range(128))
    grid = [f'{knothash(seed):0128b}' for seed in seeds]
    print(sum(sum(c == '1' for c in l) for l in grid))

    visited = set()
    def f(x, y):
        if not (0 <= x < 128) or not (0 <= y < 128):
            return
        if grid[x][y] == '0' or (x, y) in visited:
            return
        visited.add((x, y))
        for (xx, yy) in ((x+1, y), (x-1, y), (x, y+1), (x,y-1)):
            f(xx, yy)
    i = 0
    for x in range(128):
        for y in range(128):
            if grid[x][y] == '1' and (x, y) not in visited:
                f(x, y)
                i += 1
    print(i)
