from .util import getinput

s = getinput(6).strip()

for l in (4, 14):
    for i in range(len(s)):
        if len(set(s[i:i+l])) == l:
            print(i+l)
            break
