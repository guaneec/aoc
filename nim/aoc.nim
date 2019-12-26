import strformat

proc aocin*(year: int, day: int): string =
    return readFile(fmt"../data/{year}/{day:02d}.input.txt")
