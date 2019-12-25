from .util import getinput
from copy import copy
from ..aoc import dij
import doctest
import re
from dataclasses import dataclass

"""
m
p m
s p m

"""

php, pmp = 50, 500
arm = 0
dmg = 9
bhp = 58


def spell(cost):
    def dec(f):
        def ff(game):
            if game.mp < cost: return None
            o = f(game)
            if o is not None:
                o.mp -= cost
                o.cost += cost
            return o
        return ff
    return dec

@dataclass(unsafe_hash=True)
class Game:
    php: int
    mp: int
    bhp: int
    dmg: int
    hard: bool = False
    shielded: int = 0
    poisoned: int = 0
    recharging: int = 0
    cost: int = 0
    log: str = ""

    def gameover(self):
        return self.bhp <= 0 or self.php <= 0

    def tick(self):
        if self.gameover():
            return self
        c = copy(self)
        if c.shielded:
            c.shielded -= 1
        if c.poisoned:
            c.poisoned -= 1
            c.bhp -= 3
        if c.recharging:
            c.recharging -= 1
            c.mp += 101
        return c

    def boss(self):
        if self.gameover():
            return self
        c = self.tick()
        if c.gameover():
            return c
        c.php -= max(1, (c.dmg - (c.shielded > 0) * 7))
        if c.gameover():
            return c
        return c.tick()

    @spell(53)
    def missile(self):
        c = copy(self)
        c.bhp -= 4
        c.log = c.log + "m"
        return c

    @spell(73)
    def drain(self):
        c = copy(self)
        c.bhp -= 2
        c.php += 2
        c.log = c.log + "d"
        return c

    @spell(113)
    def shield(self):
        if self.shielded:
            return
        c = copy(self)
        c.shielded = 6
        c.log = c.log + "s"
        return c
        
    @spell(173)
    def poison(self):
        if self.poisoned:
            return
        c = copy(self)
        c.poisoned = 6
        c.log = c.log + "p"
        return c
        
        
    @spell(229)
    def recharge(self):
        if self.recharging:
            return
        c = copy(self)
        c.recharging = 5
        c.log = c.log + "r"
        return c

    def choices(self):
        if self.hard:
            self = copy(self)
            self.php -= 1
        if self.gameover():
            return []
        return [x.boss() for x in [
            self.missile(), self.shield(), self.recharge(), self.drain(), self.poison()
            ] if x is not None]


def nb(game: Game):
    return ((c.cost - game.cost, c) for c in game.choices())


def p1(hp, mp, bhp, dmg, hard=False):
    g = Game(hp, mp, bhp, dmg, hard)
    for cost, g in dij([g], nb):
        if g.bhp <= 0:
            return g



doctest.testmod()
s = getinput(22)
bhp, dmg = [int(x) for x in re.findall(r'\d+', s)]
#print(p1(10, 250, 14, 8))
print(p1(50, 500, bhp, dmg).cost)
print(p1(50, 500, bhp, dmg, True).cost)
