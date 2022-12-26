from .util import getinput
from math import prod
import re

s = getinput(19)

bps = {}
for g in s.split('obsidian.'):
    if not g.strip():
        continue
    q = [int(x) for x in re.findall('[0-9]+', g)]
    bps[q[0]] = q[1:]

cdiv = lambda a, b: 1e8 if b == 0 else (a+b-1) // b

def g(T, b, state):
    t, ore, clay, obs, dore, dclay, dobs = state
    oo, co, obo, obc, go, gob = bps[b]
    m = 0
    if (tt := T-2-t) > 0 and dore * (tt-1) + ore < max(oo, co, obo, go) * tt and (dt := cdiv(max(0, oo - ore), dore) + 1) + t <= T:
        m = max(m, g(T, b, (t+dt, ore+dt*dore-oo, clay+dt*dclay, obs+dt*dobs, dore+1, dclay, dobs)))
    if (tt := T-4-t) > 0 and dclay * (tt-1) + clay < obc * tt and (dt := cdiv(max(0, co - ore), dore) + 1) + t <= T:
        m = max(m, g(T, b, (t+dt, ore+dt*dore-co, clay+dt*dclay, obs+dt*dobs, dore, dclay+1, dobs)))
    if (tt := T-2-t) > 0 and dobs * (tt-1) + obs < gob * tt and (dt := max(cdiv(max(0, obo - ore), dore), cdiv(max(0, obc - clay), dclay)) + 1) + t <= T:
        m = max(m, g(T, b, (t+dt, ore+dt*dore-obo, clay+dt*dclay-obc, obs+dt*dobs, dore, dclay, dobs+1)))
    if (dt := max(cdiv(max(0, go - ore), dore), cdiv(max(0, gob - obs), dobs)) + 1) + t <= T:
        m = max(m, T+1-(t+dt) + g(T, b, (t+dt, ore+dt*dore-go, clay+dt*dclay, obs+dt*dobs-gob, dore, dclay, dobs)))
    return m
        
print(sum(k * (g(24, k, (1, 0, 0, 0, 1, 0, 0))) for k in bps))
print(prod((g(32, k, (1, 0, 0, 0, 1, 0, 0))) for k in bps if k <= 3))
