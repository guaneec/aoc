from aoc2018 import getinput, Machine

s = getinput(15)
c = [int(x) for x in s.strip().split(',')]

m = Machine(c)

visited = {(0, 0): 1}
back = {
    1: 2,
    2: 1,
    3: 4,
    4: 3,
}

def search(xy0):
    x, y = xy0
    for d, xy in zip([1,2,3,4], [(x,y+1), (x,y-1), (x-1,y), (x+1,y)]):
        if xy in visited:
            continue
        m.iq.append(d)
        m.resume()
        o = m.oq.popleft()
        visited[xy] = o
        if o == 0:
            continue
            
        search(xy)
        m.iq.append(back[d])
        m.resume()
        assert(0 != m.oq.popleft())
        
search((0, 0))


def getdd(xy0):    
    x, y = xy0
    for xy in  [(x,y+1), (x,y-1), (x-1,y), (x+1,y)]:
        if not (xy in visited and visited[xy]):
            continue
        if xy not in dd or dd[xy] > dd[xy0]+1:
            dd[xy] = dd[xy0]+1
            getdd(xy)

target = [k for k in visited if visited[k] == 2][0]

dd = {(0, 0): 0}
getdd((0, 0))
print(dd[target])

dd = {target: 0}
getdd(target)
print(max(v for v in dd.values()))
