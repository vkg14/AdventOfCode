from dataclasses import dataclass
from typing import List, Any
from operator import *


@dataclass
class Node:
    children: List[str]
    value: int = 0
    is_leaf: bool = False
    operation: Any = None


def sign_to_lambda(char):
    if char == '+':
        return add
    elif char == '-':
        return sub
    elif char == '/':
        return truediv
    elif char == '*':
        return mul
    else:
        return None


def read_input(filename):
    monkeys = dict()
    with open(filename) as f:
        for line in f:
            sp = line.rstrip('\n').split(': ')
            monkey = sp[0]
            sp2 = sp[1].split()
            if len(sp2) == 1:
                monkeys[monkey] = Node([], int(sp2[0]), True, None)
            else:
                monkeys[monkey] = Node([sp2[0], sp2[2]], 0, False, sign_to_lambda(sp2[1]))
    return monkeys


def dfs(monkey, cache, m):
    if m[monkey].is_leaf:
        return m[monkey].value
    elif monkey in cache:
        return cache[monkey]
    children = m[monkey].children
    vals = []
    for c in children:
        vals.append(dfs(c, cache, m))
    cache[monkey] = m[monkey].operation(*vals)
    return cache[monkey]


def solve(filename):
    monkeys = read_input(filename)
    return int(dfs('root', dict(), monkeys))


def try_humn_value(start, monkeys, val):
    monkeys['humn'].value = val
    return dfs(start, dict(), monkeys)


def solve_part_two(filename):
    monkeys = read_input(filename)

    root_children = monkeys['root'].children
    c0 = try_humn_value(root_children[0], monkeys, 0)
    c1 = try_humn_value(root_children[0], monkeys, 1)
    if c0 == c1:
        t = c0
        dependent = root_children[1]
    else:
        t = dfs(root_children[1], dict(), monkeys)
        dependent = root_children[0]
    d0 = try_humn_value(dependent, monkeys, 0)
    d1 = try_humn_value(dependent, monkeys, 1)
    same_direction = d1 > d0
    lower_bound = 0
    # Higher bound chosen through trial and error
    higher_bound = 10**15
    while lower_bound < higher_bound:
        midpoint = (lower_bound + higher_bound) // 2
        diff = t - try_humn_value(dependent, monkeys, midpoint)
        if diff > 0:
            if same_direction:
                # humn needs to be higher
                lower_bound = midpoint
            else:
                higher_bound = midpoint
        elif diff < 0:
            if same_direction:
                # humn needs to be lower
                higher_bound = midpoint
            else:
                lower_bound = midpoint
        else:
            return midpoint


if __name__ == '__main__':
    print(solve("example21.txt"))
    print(solve("input21.txt"))
    print(solve_part_two("example21.txt"))
    print(solve_part_two("input21.txt"))
