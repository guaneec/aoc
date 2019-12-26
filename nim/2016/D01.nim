import strutils
import sets
import ../aoc

let s = aocin(2016, 1)

type XY = tuple[x: int, y: int]

var direction: XY = (0, 1)
var position: XY
var positions: HashSet[XY]
var reppos: XY
var repgood: bool

proc rot(xy: XY, ccw: bool): XY =
    let (x, y) = xy
    return if ccw: (-y, x) else: (y, -x)

proc `+` (xy1: XY, xy2: XY): XY =
    return (xy1.x + xy2.x, xy1.y + xy2.y)

proc dist(xy: XY): int =
    abs(xy.x) + abs(xy.y)

for inst in s.strip().split(", "):
    direction = rot(direction, inst[0] == 'L')
    for _ in 1..parseInt(inst.substr(1)):
        position = position + direction
        if not repgood and position in positions:
            reppos = position
            repgood = true
        else:
            positions.incl(position)


echo position.dist()
echo reppos.dist()
