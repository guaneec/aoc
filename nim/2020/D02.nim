import strutils
import re

import ../aoc

var a1 = 0
var a2 = 0
for line in aocin(2020, 2).strip().splitLines():
    var matches: array[4, string]
    assert(match(line, re"(\d+)-(\d+) (\w): (\w+)", matches))
    let mn = parseInt(matches[0])
    let mx = parseInt(matches[1])
    let c =  matches[2][0]
    let s = matches[3]
    let cnt = count(s, c)
    if mn <= cnt and cnt <= mx:
        a1 += 1
    if (s[mn-1] == c) != (s[mx-1] == c):
        a2 += 1

echo a1
echo a2
