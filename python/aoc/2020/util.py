from pathlib import Path

from .. import aoc

rootdir = Path(__file__).parent / '../../'

def getinput(day):
    return aoc.getinput(2020, day)

