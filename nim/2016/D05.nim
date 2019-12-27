import strutils
import  md5
import ../aoc

let s = aocin(2016, 5).strip()
var c = 0
var d = 0
var p2 = "________"
for i in 1..high(int):
    let h = (s & intToStr(i)).getMD5()
    if h[..4] == "00000":
        if c < 8:
            stdout.write(h[5])
        c += 1
        if c == 8:
            stdout.write('\n')
        let x = ord(h[5]) - ord('0')
        if 0 <= x and x <= 7:
            if p2[x] == '_':
                d += 1
                p2[x] = h[6]
                if d == 8:
                    break
echo p2
