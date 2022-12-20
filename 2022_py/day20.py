from collections import deque
from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    val: int
    prev: Optional['Node']
    nxt: Optional['Node']
    mixed: bool = False


def read(filename, mult=1):
    root = None
    prev = None
    i = 0
    with open(filename) as f:
        for line in f:
            i += 1
            v = int(line.rstrip('\n')) * mult
            curr = Node(v, prev, None)
            if prev:
                prev.nxt = curr
            if not root:
                root = curr
            prev = curr
    root.prev = prev
    prev.nxt = root
    return root, i


def get_n_from(node, k):
    res = node
    for i in range(k):
        res = res.nxt
    return res.val


def print_l(node, n):
    for i in range(n):
        print(node.val)
        node = node.nxt


def solve(filename: str, mult=1, times=1):
    root, n = read(filename, mult=mult)
    q = deque()
    add = root
    for i in range(n):
        q.append(add)
        add = add.nxt
    zero = None
    for k in range(n * times):
        curr = q.popleft()
        if curr.val > 0:
            curr.prev.nxt = curr.nxt
            curr.nxt.prev = curr.prev
            tmp = curr
            for j in range(curr.val % (n - 1)):
                tmp = tmp.nxt
            tmp2 = tmp.nxt
            tmp.nxt = curr
            curr.prev = tmp
            tmp2.prev = curr
            curr.nxt = tmp2
        elif curr.val < 0:
            curr.nxt.prev = curr.prev
            curr.prev.nxt = curr.nxt
            tmp = curr
            for j in range(abs(curr.val) % (n - 1)):
                tmp = tmp.prev
            tmp2 = tmp.prev
            tmp2.nxt = curr
            curr.prev = tmp2
            tmp.prev = curr
            curr.nxt = tmp
        else:
            zero = curr
        q.append(curr)
    return get_n_from(zero, 1000 % n) + get_n_from(zero, 2000 % n) + get_n_from(zero, 3000 % n)


if __name__ == '__main__':
    print(solve("example20.txt"))
    print(solve("input20.txt"))
    print(solve("example20.txt", mult=811589153, times=10))
    print(solve("input20.txt", mult=811589153, times=10))
