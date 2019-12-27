package aoc.Y2016
import kotlin.math.abs
import aoc.aocin

data class XY(val x: Int, val y: Int)

fun main(args: Array<String>) {
    val s = aocin(2016, 1)
    var repFound = false
    var repX = 0
    var repY = 0
    var x = 0
    var y = 0
    var dx = 0
    var dy = 1
    var positions = setOf(XY(x, y))
    for (item in s.trim().split(", ")) {
        if (item[0] == 'L') {
            val t = dx
            dx = -dy
            dy = t
        } else {
            val t = dx
            dx = dy
            dy = -t
        }
        for (i in 1..item.drop(1).toInt()) {
            x += dx
            y += dy
            if (!repFound && XY(x, y) in positions) {
                repFound = true
                repX = x
                repY = y
            } else {
                positions += XY(x, y)
            }
        }
    }
    println(abs(x) + abs(y))
    println(abs(repX) + abs(repY))
}
