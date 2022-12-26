from .util import getinput
from math import prod
import re
from functools import lru_cache
from ..aoc import astar

s = getinput(19)

bps = {}
for g in s.split('obsidian.'):
    if not g.strip():
        continue
    q = [int(x) for x in re.findall('[0-9]+', g)]
    bps[q[0]] = q[1:]

cdiv = lambda a, b: 1e8 if b == 0 else (a+b-1) // b

# infinite ore and clay
@lru_cache(None)
def h(T, b, state):
    t, obs, dobs = state
    oo, co, obo, obc, go, gob = bps[b]
    m = 0
    if (dt := cdiv(max(0, gob - obs), dobs) + 1) + t <= T:
        m = max(m, T+1-(t+dt) + h(T, b, (t+dt, obs+dt*dobs-gob, dobs)))
    if (tt := T-2-t) > 0 and dobs * (tt-1) + obs < gob * tt and (dt := 1) + t <= T:
        m = max(m, h(T, b, (t+dt, obs+dt*dobs, dobs+1)))
    return m

def z(T, b, state):
    oo, co, obo, obc, go, gob = bps[b]
    def nb(state):
        t, ore, clay, obs, dore, dclay, dobs = state
        if (dt := max(cdiv(max(0, go - ore), dore), cdiv(max(0, gob - obs), dobs)) + 1) + t <= T:
            yield -(T+1-(t+dt)), (t+dt, ore+dt*dore-go, clay+dt*dclay, obs+dt*dobs-gob, dore, dclay, dobs)
        if (tt := T-2-t) > 0 and dobs * (tt-1) + obs < gob * tt and (dt := max(cdiv(max(0, obo - ore), dore), cdiv(max(0, obc - clay), dclay)) + 1) + t <= T:
            yield 0, (t+dt, ore+dt*dore-obo, clay+dt*dclay-obc, obs+dt*dobs, dore, dclay, dobs+1)
        if (tt := T-4-t) > 0 and dclay * (tt-1) + clay < obc * tt and (dt := cdiv(max(0, co - ore), dore) + 1) + t <= T:
            yield 0, (t+dt, ore+dt*dore-co, clay+dt*dclay, obs+dt*dobs, dore, dclay+1, dobs)
        if (tt := T-2-t) > 0 and dore * (tt-1) + ore < max(oo, co, obo, go) * tt and (dt := cdiv(max(0, oo - ore), dore) + 1) + t <= T:
            yield 0, (t+dt, ore+dt*dore-oo, clay+dt*dclay, obs+dt*dobs, dore+1, dclay, dobs)
        yield 0, (T+1, 0, 0, 0, 0, 0, 0)

    def hh(state):
        t, ore, clay, obs, dore, dclay, dobs = state
        return -h(T, b, (t, obs, dobs))

    for d, x in astar([state], nb, hh):
        if x[0] == T+1:
            return -d

print(sum(k * (z(24, k, (1, 0, 0, 0, 1, 0, 0))) for k in bps))
print(prod((z(32, k, (1, 0, 0, 0, 1, 0, 0))) for k in bps if k <= 3))
