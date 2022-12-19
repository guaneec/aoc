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

def f(T, b, state):
    t, ore, clay, obs, geo, dore, dclay, dobs, dgeo = state
    if t > T:
        assert t == T + 1
        yield geo
        return
    oo, co, obo, obc, go, gob = b
    tt = T + 1 - t
    if dore * tt + ore < max(oo, co, obo, go) * tt and (dt := cdiv(max(0, oo - ore), dore) + 1) + t <= T + 1:
        yield from f(T, b, (t+dt, ore+dt*dore-oo, clay+dt*dclay, obs+dt*dobs, geo+dt*dgeo, dore+1, dclay, dobs, dgeo))
    if dclay * tt + clay < obc * tt and (dt := cdiv(max(0, co - ore), dore) + 1) + t <= T + 1:
        yield from f(T, b, (t+dt, ore+dt*dore-co, clay+dt*dclay, obs+dt*dobs, geo+dt*dgeo, dore, dclay+1, dobs, dgeo))
    if dobs * tt + obs < gob * tt and (dt := max(cdiv(max(0, obo - ore), dore), cdiv(max(0, obc - clay), dclay)) + 1) + t <= T + 1:
        yield from f(T, b, (t+dt, ore+dt*dore-obo, clay+dt*dclay-obc, obs+dt*dobs, geo+dt*dgeo, dore, dclay, dobs+1, dgeo))
    if (dt := max(cdiv(max(0, go - ore), dore), cdiv(max(0, gob - obs), dobs)) + 1) + t <= T + 1:
        yield from f(T, b, (t+dt, ore+dt*dore-go, clay+dt*dclay, obs+dt*dobs-gob, geo+dt*dgeo, dore, dclay, dobs, dgeo+1))
    yield geo + (T + 1 - t) * dgeo
        
print(sum(k * max(f(24, v, (1, 0, 0, 0, 0, 1, 0, 0, 0))) for k, v in bps.items()))
print(prod(max(f(32, v, (1, 0, 0, 0, 0, 1, 0, 0, 0))) for k, v in bps.items() if k <= 3))
