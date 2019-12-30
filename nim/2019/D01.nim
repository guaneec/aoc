import strutils
import ../aoc

proc fuel(mass: int): int =
    return mass div 3 - 2

proc fuel2(mass: int): int =
    let f = fuel(mass)
    if f <= 0:
        return f
    return f + fuel2(f)

let f = aocin(2019, 1)

var s1, s2 = 0
for line in splitLines(f.strip()):
    let i = line.parseInt()
    s1 += fuel(i)
    s2 += fuel2(i)

echo s1
echo s2
