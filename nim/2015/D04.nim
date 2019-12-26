import strutils
import  md5

let s = readFile("../../data/2015/04.input.txt").strip()

var o5 = 0
for i in 1..high(int):
    let h = (s & intToStr(i)).getMD5()
    if h[..4] == "00000" and o5 == 0:
        o5 = i
    if h[..5] == "000000":
        echo o5
        echo i
        break
