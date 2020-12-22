from .util import getinput
from itertools import permutations
import re

s = getinput(21)

ingredents = set()
allergens = set()
foods = []

for l in s.splitlines():
    m = re.match(r"^(.+) \(contains (.+)\)$", l)
    ings = m.group(1).split()
    llers = m.group(2).split(", ")
    foods.append((ings, llers))
    ingredents.update(ings)
    allergens.update(llers)

safe = set() | ingredents
for a in allergens:
    this = set() | safe
    for ins, ls in foods:
        if not a in ls:
            continue
        this = this & set(ins)
    safe = safe - set(this)

dangers = set(ingredents) - safe
assert len(dangers) == len(allergens)
print(sum(sum(i in safe for i in ii) for ii, _ in foods))
allergens = sorted(allergens)
for p in permutations(dangers):
    trans = {k: v for k, v in zip(allergens, p)}
    if all(all(trans[l] in ii for l in ll) for ii, ll in foods):
        print(",".join(p))
        break
