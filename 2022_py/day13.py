import json
from dataclasses import dataclass
from math import prod
from typing import List


@dataclass
class MyClass:
    lst: List

    def __lt__(self, other):
        return compare(self.lst, other.lst)


def read_input(fname):
    with open(fname) as f:
        lines = []
        for line in f:
            if not line.rstrip('\n'):
                yield lines
                lines = []
                continue
            lines.append(line.rstrip('\n'))
        if lines:
            yield lines


def compare(left, right):
    for l, r in zip(left, right):
        if l == r:
            continue
        if type(l) == type(r) and isinstance(l, list):
            return compare(l, r)
        if type(l) == type(r) and isinstance(l, int):
            return l < r
        elif isinstance(l, int):
            l2 = [l]
            if l2 == r:
                continue
            return compare(l2, r)
        else:
            r2 = [r]
            if l == r2:
                continue
            return compare(l, r2)
    return len(left) < len(right)


def solve_part2(fname):
    total = []
    for lines in read_input(fname):
        total.append(MyClass(json.loads(lines[0])))
        total.append(MyClass(json.loads(lines[1])))
    total.append(MyClass([[2]]))
    total.append(MyClass([[6]]))
    s = sorted(total)
    return prod([i+1 for i, x in enumerate(s) if x.lst == [[2]] or x.lst == [[6]]])


def solve_part1(fname):
    i = 1
    right_order = []
    for lines in read_input(fname):
        left = json.loads(lines[0])
        right = json.loads(lines[1])
        if compare(left, right):
            right_order.append(i)
        i += 1
    return sum(right_order)


if __name__ == '__main__':
    print(solve_part1("input13.txt"))
    print(solve_part2("example13.txt"))
    print(solve_part2("input13.txt"))
