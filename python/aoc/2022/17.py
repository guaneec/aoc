from .util import getinput
from itertools import cycle

s = getinput(17).strip()

rocks = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""

rocks = [
    [
        (i, j)
        for j, l in enumerate(reversed(g.splitlines()))
        for i, c in enumerate(l)
        if c == "#"
    ]
    for g in rocks.split("\n\n")
]

RIGHT = 5
LEFT = -3
FLOOR = 0
tip = 0
placed = set()


class Recorder:
    def __init__(self) -> None:
        self.enabled = False
        self.logs = []

    def start(self, tip, placed, ir, ig):
        self.enabled = True
        self.tip = tip
        self.placed = {*placed}
        self.ir = ir
        self.ig = ig

    def add_record(self, bumped, rock):
        if self.enabled and (not bumped or will_bump(rock, self.placed)):
            self.logs.append((bumped, rock))

    def can_replay(self, tip, placed, ir, ig):
        return (
            self.logs
            and (self.ir - ir) % len(rocks) == 0
            and (self.ig - ig) % len(s) == 0
            and all(
                bumped
                == will_bump(((x, y + tip - self.tip) for x, y in blocks), placed)
                for bumped, blocks in self.logs
            )
        )


def will_bump(rock, placed):
    return any(
        x == RIGHT or x == LEFT or y == FLOOR or (x, y) in placed for x, y in rock
    )


offset = 0
target = 1000000000000
GUESS = 3000  # must be in a cycle after this many rocks
recorder = Recorder()
ig = 0
for ir, rock in enumerate(cycle(rocks)):
    if recorder.can_replay(tip, placed, ir, ig):
        P = ir - recorder.ir
        skipped = (target - ir) // P
        target -= skipped * P
        offset += skipped * (tip - recorder.tip)
    if ir >= GUESS and ir % len(rr) == target % len(rr):
        if not recorder.enabled:
            recorder.start(tip, placed, ir, ig)
    if ir == 2022:
        print(tip)
    if ir == target:
        print(tip + offset)
        break
    r = [(x, y + tip + 4) for x, y in rock]
    while True:
        dx = -1 if s[ig % len(s)] == "<" else 1
        ig += 1
        rr = [(x + dx, y) for x, y in r]
        if not (bumped := will_bump(rr, placed)):
            r = rr
        recorder.add_record(bumped, rr)
        rr = [(x, y - 1) for x, y in r]
        bumped = will_bump(rr, placed)
        recorder.add_record(bumped, rr)
        if not bumped:
            r = rr
        else:
            break
    tip = max(tip, max(y for x, y in r))
    placed.update(r)
