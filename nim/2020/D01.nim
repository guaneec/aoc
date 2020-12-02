from sugar import collect
import strutils
import algorithm
import ../aoc

var nums = collect(newSeq):
    for line in splitLines(aocin(2020, 1).strip()): line.parseInt()

nums.sort()

proc findsum(l: seq[int], target: int): (int, int) =
    var (i, j) = (0, l.len - 1)
    result = (-1, -1)
    while i < j:
        let ss = l[i] + l[j]
        if ss == target:
            return (l[i], l[j])
        if ss < target:
            i += 1
        else:
            j -= 1
    
let (x1, x2) = findsum(nums, 2020)
echo x1 * x2

for i in 0 .. nums.len-1:
    let (y1, y2) = findsum(nums[i .. ^1], 2020 - nums[i])
    if y1 >= 0:
        echo nums[i] * y1 * y2
        break