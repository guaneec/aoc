from os import getcwd
from aoc2018 import getinput

nums = [int(i) for i in getinput(1).splitlines()]
fuel = lambda i: (i // 3) - 2
def realfuel(i):
    f = fuel(i)
    return 0 if f <= 0 else f + realfuel(f)

print(sum(fuel(i) for i in nums))
print(sum(realfuel(i) for i in nums))
