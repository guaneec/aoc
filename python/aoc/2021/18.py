from __future__ import annotations
from functools import reduce
from .util import getinput
from dataclasses import dataclass
from typing import Union, Optional, Tuple
from itertools import permutations


s = getinput(18)


@dataclass
class Leaf:
    left: Optional[Leaf]
    right: Optional[Leaf]
    val: int
    depth: int

    def __repr__(self) -> str:
        return repr(self.val)

@dataclass
class TreeNode:
    depth: int
    left: Union[TreeNode, Leaf]
    right: Union[TreeNode, Leaf]

    def __repr__(self) -> str:
        return repr((self.left, self.right))

def from_list(expr, depth=0) -> Tuple[Optional[Leaf], Union[TreeNode, Leaf], Optional[Leaf]]:
    match expr:
        case [xl, xr]:
            ll, ln, lr = from_list(xl, depth+1)
            rl, rn, rr = from_list(xr, depth+1)
            if lr:
                lr.right = rl
            if rl:
                rl.left = lr
            return ll, TreeNode(depth, ln, rn), rr
        case x:
            leaf = Leaf(None, None, x, depth)
            return leaf, leaf, leaf

def explode(n: TreeNode) -> Tuple[Union[TreeNode, Leaf], bool]:
    if type(n.left) == type(n.right) == Leaf and n.depth >= 4:
        leaf = Leaf(n.left.left, n.right.right, 0, n.depth)
        if n.left.left:
            n.left.left.val += n.left.val
            n.left.left.right = leaf
        if n.right.right:
            n.right.right.val += n.right.val
            n.right.right.left = leaf
        return leaf, True
    if type(n.left) == TreeNode:
        nl, done = explode(n.left)
        if done:
            n.left = nl
            return n, True
    if type(n.right) == TreeNode:
        nr, done = explode(n.right)
        if done:
            n.right = nr
            return n, True
    return n, False

def split(l: Union[TreeNode, Leaf]) -> Tuple[Union[TreeNode, Leaf], bool]:
    if type(l) == TreeNode:
        xl, done = split(l.left)
        if done:
            l.left = xl
            return l, True
        xr, done = split(l.right)
        if done:
            l.right = xr
            return l, True
        return l, False
    if l.val < 10:
        return l, False
    ll = Leaf(l.left, None, l.val // 2, l.depth + 1)
    lr = Leaf(None, l.right, (l.val + 1) // 2, l.depth + 1)
    ll.right = lr
    lr.left = ll
    if l.left:
        l.left.right = ll
    if l.right:
        l.right.left = lr
    return TreeNode(l.depth, ll, lr), True

def red(n: TreeNode) -> TreeNode:
    while True:
        # print(n)
        if type(n.left) == TreeNode:
            nl, done = explode(n.left)
            if done:
                n.left = nl
                continue
        if type(n.right) == TreeNode:
            nr, done = explode(n.right)
            if done:
                n.right = nr
                continue
        x, done = split(n.left)
        if done:
            n.left = x
            continue
        x, done = split(n.right)
        if done:
            n.right = x
            continue
        return n

def inc_depth(x: Optional[Union[TreeNode, Leaf]]):
    if not x:
        return
    x.depth += 1
    if type(x) == TreeNode:
        inc_depth(x.left)
        inc_depth(x.right)

def add(a: TreeNode, b: TreeNode) -> TreeNode:
    inc_depth(a)
    inc_depth(b)
    lr = a
    while type(lr) != Leaf:
        lr = lr.right
    rl = b
    while type(rl) != Leaf:
        rl = rl.left
    lr.right = rl
    rl.left = lr
    return TreeNode(0, a, b)

ls = [eval(l) for l in s.splitlines()]
print(ls)
def op(a, b):
    return red(add(a, b))
t = reduce(op, map(lambda l: from_list(l)[1], ls))
print(t)

def mag(t):
    if type(t) == Leaf:
        return t.val
    return 3 * mag(t.left) + 2 * mag(t.right)

print(mag(t))

f = lambda x: from_list(x)[1]
p2 = max(
    mag(red(add(f(a), f(b))))
    for a, b in permutations(ls, 2)
)
print(p2)