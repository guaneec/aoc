from .util import getinput

s = getinput(5)

sid = lambda x: int(''.join('01'[c in 'BR'] for c in x), 2)
sids = sorted(sid(line) for line in s.splitlines())
print(sids[-1])
print(next((a, b) for a, b in zip(sids, sids[1:]) if a + 2 == b)[0] + 1)
