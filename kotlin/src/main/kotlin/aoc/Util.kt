package aoc

import java.io.File

fun aocin(year: Int, day: Int): String {
    return File("../data/${year}/${"%02d".format(day)}.input.txt").readText()
}
