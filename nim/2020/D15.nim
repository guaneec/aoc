import strutils
import fusion/btreetables

import ../aoc

for n in [2020, 30000000]:
    let d = newTable[int, int]()
    var i: int = 0
    var x: int
    for istr in aocin(2020, 15).strip().split(","):
        x = istr.parseInt()
        d[x] = i
        i += 1

    d.del(x)

    for j in i-1 .. n-2:
        let y = j - d.getOrDefault(x, j)
        d[x] = j
        x = y
    echo x
