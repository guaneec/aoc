from .util import getinput
from queue import PriorityQueue, Queue

s = '''
#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######'''

s = '''
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############
'''

s = getinput(18)

vault = s.strip().splitlines()

states = 0

entrance = [(y, x) for (y, l) in enumerate(vault) for (x, c) in enumerate(l) if c == '@'][0]
allKeys = { c for c in s if c.islower() }

def adjs(vault, pos):
    y, x = pos
    return set( (y, x) for y, x in [
        (y + 1, x),
        (y - 1, x),
        (y, x + 1),
        (y, x - 1),
    ] if 0 <= x <= len(vault[0]) and 0 <= y <= len(vault) )

def keyDists(vault, pos, keys):
    toSee = [pos]
    seen = set()
    doors = set()
    keys = keys.copy()
    dist = 0
    while toSee:
        toSeeNew = []
        for y, x in toSee:
            seen.add((y, x))
            c = vault[y][x]
            if c in seen or c == '#':
                continue
            if c.isupper() and c.lower() not in keys:
                doors.add(c.lower())
                continue
            elif c.islower() and c not in keys:
                keys.add(c)
                yield (dist, c, (y, x))
                continue
            for yx in adjs(vault, (y,x)) - seen:
                toSeeNew.append(yx)
        toSee = toSeeNew
        dist += 1
            



def find(vault, pos):
    pq = PriorityQueue()
    pq.put_nowait((0, (pos, set())))
    visited = set()
    while pq:
        d, (pos, keys) = pq.get_nowait()
        x = (pos, frozenset(keys))
        if x in visited:
            continue
        visited.add(x)
        if keys == allKeys:
            return (d, (pos, keys))
        #print((d, (pos, keys)), list(keyDists(pos, keys)))
        for dd, k, p in keyDists(vault, pos, keys):
            kk = keys | {k}
            dd = d + dd
            pq.put_nowait((dd, (p, kk)))
    raise Exception('Not found')
    
def find2(vault, pos):
    ppy, ppx = pos
    vault = vault.copy()
    vault[ppy-1] = vault[ppy-1][:ppx-1] + '.#.' + vault[ppy-1][ppx+2:]
    vault[ppy] = vault[ppy][:ppx-1] + '###' + vault[ppy][ppx+2:]
    vault[ppy+1] = vault[ppy+1][:ppx-1] + '.#.' + vault[ppy+1][ppx+2:]
    poss = (
        (ppy-1, ppx-1),
        (ppy+1, ppx-1),
        (ppy-1, ppx+1),
        (ppy+1, ppx+1),
    )

    pq = PriorityQueue()
    pq.put_nowait((0, (poss, set())))
    visited = set()
    while not pq.empty():
        d, (poss, keys) = pq.get_nowait()
        x = (poss, frozenset(keys))
        if x in visited:
            continue
        visited.add(x)
        if keys == allKeys:
            return (d, (poss, keys))
        for pi, px in enumerate(poss):
            for dd, k, p in keyDists(vault, px, keys):
                kk = keys | {k}
                dd = d + dd
                pposs = tuple(z if j != pi else p for j, z in enumerate(poss))
                pq.put_nowait((dd, (pposs, kk)))
        # a bot either go through a door just unlocked or pick up a key

    raise Exception('Not found')


print(find(vault, entrance))
print(find2(vault, entrance))
