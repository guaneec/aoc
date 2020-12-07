import re

from .util import getinput

s = getinput(7)

graph = {}

for line in s.splitlines():
    this = {}
    f, b = line.split(' contain ')
    label = f.rpartition(' ')[0]
    for match in re.finditer(r'(\d+) (.+?) bag', line):
        this[match.group(2)] = int(match.group(1))
    graph[label] = this

def has_color(parent, child):
    return any(k == child or has_color(k, child) for k in graph[parent])

def n_bags(color):
    return sum((1 + n_bags(k)) * v for k, v in graph[color].items())

print(sum(has_color(k, 'shiny gold') for k in graph))
print(n_bags('shiny gold'))