from pathlib import Path
import sys
import subprocess
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

rootdir = Path(__file__) / '../../../'
def getinput(year, day):
    p = rootdir / f'data/{year}/{day:02d}.input.txt'
    if not p.is_file():
        cp = subprocess.run(f"python {rootdir / 'data.py'}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(cp.stdout.decode('utf-8'))
        cp.check_returncode()
    with open(p) as f:
        return f.read()

def bfs(seeds, neighbors):
    q = list(seeds)
    seen = set(seeds)
    d = 0
    while q:
        qq = []
        for n in q:
            yield d, n
            nb = list(neighbors(n))
            qq.extend(nn for nn in nb if nn not in seen)
            seen.update(nb)
            pass
        d += 1
        q = qq

def dij(seeds, neighbors):
    q = PriorityQueue()
    dists = {}
    for s in seeds:
        q.put_nowait(PrioritizedItem(0, s))
    
    while not q.empty():
        pi = q.get_nowait()
        d, n = pi.priority, pi.item
        yield d, n
        for nd, nn in neighbors(n):
            dNew = d + nd
            if nn in dists and dists[nn] <= dNew:
                continue
            dists[nn] = dNew
            q.put_nowait(PrioritizedItem(dNew, nn))
