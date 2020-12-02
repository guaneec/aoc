from sugar import collect
import strutils
import ../aoc

let nums = collect(newSeq):
    for line in splitLines(aocin(2020, 1).strip()): line.parseInt()
let n = nums.len

block b1:
    for i in countup(0, n - 1):
        for j in countup(i + 1, n - 1):
            if nums[i] + nums[j] == 2020:
                echo nums[i] * nums[j]
                break b1
block b2:
    for i in countup(0, n - 1):
        for j in countup(i + 1, n - 1):
            for k in countup(j + 1, n - 1):
                if nums[i] + nums[j] + nums[k] == 2020:
                    echo nums[i] * nums[j] * nums[k]
                    break b2
