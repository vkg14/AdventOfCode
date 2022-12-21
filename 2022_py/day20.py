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
        if curr.val != 0:
            move = curr.val % (n-1)
            curr.prev.nxt = curr.nxt
            curr.nxt.prev = curr.prev
            tmp = curr
            for j in range(move):
                tmp = tmp.nxt
            tmp2 = tmp.nxt
            tmp.nxt = curr
            curr.prev = tmp
            tmp2.prev = curr
            curr.nxt = tmp2
        else:
            zero = curr
        q.append(curr)
    return get_n_from(zero, 1000 % n) + get_n_from(zero, 2000 % n) + get_n_from(zero, 3000 % n)


def jenn_solve(filename: str):
    nums = []
    num_dict = {}
    with open(filename) as file:
        i = 0
        for line in file.readlines():
            num = int(line.strip()) * 811589153
            nums.append((i, num))
            num_dict[i] = num
            i += 1

    copy = nums[::]
    for c in range(10):
        copy = copy[::]
        for i in range(len(nums)):
            num_to_move = num_dict[i]
            current_i = copy.index((i, num_to_move))
            new_i = (current_i + num_to_move) % (len(nums) - 1)

            if current_i < new_i:
                copy = copy[:current_i] + copy[current_i + 1:new_i + 1] + [(i, num_to_move)] + copy[new_i + 1:]

            elif current_i > new_i:
                copy = copy[:new_i] + [(i, num_to_move)] + copy[new_i:current_i] + copy[current_i + 1:]

    vals = [x[1] for x in copy]
    zero_index = vals.index(0)
    return sum([
        vals[(zero_index + i) % len(vals)] for i in [1000, 2000, 3000]
    ])


if __name__ == '__main__':
    # print(solve("example20.txt"))
    # print(solve("input20.txt"))
    # print(solve("example20.txt", mult=811589153, times=10))
    print(solve("input20.txt", mult=811589153, times=10))
    print(jenn_solve("input20.txt"))
