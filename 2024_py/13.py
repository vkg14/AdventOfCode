import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *


def parse_button(line):
    equations = line.split(": ")[1]
    x, y = equations.split(", ")
    return int(x.split('+')[1]), int(y.split('+')[1])


def parse_prize(line):
    equations = line.split(": ")[1]
    x, y = equations.split(", ")
    return int(x.split('=')[1]), int(y.split('=')[1])


def parse(fname):
    content = get_readlines_stripped(fname)
    i = 0
    claw_machines = []
    while i < len(content):
        a = parse_button(content[i])
        b = parse_button(content[i+1])
        prize = parse_prize(content[i+2])
        claw_machines.append((a, b, prize))
        i += 4
    return claw_machines


def compute_tokens(a, b, prize):
    ax, ay = a
    bx, by = b
    px, py = prize
    for m in range(101):
        leftover_x = px - m * ax
        leftover_y = py - m * ay
        if leftover_x < 0 or leftover_y < 0:
            return 0
        if leftover_x % bx == 0 and leftover_y % by == 0 and leftover_x // bx * by == leftover_y:
            return m*3 + leftover_x // bx
    return 0


def solve_part_one(fname):
    claw_machines = parse(fname)
    tokens = 0
    for a, b, prize in claw_machines:
        tokens += compute_tokens(a, b, prize)
    return tokens


def parse_two(fname):
    claw_machines = parse(fname)
    adjusted = []
    to_add = (10000000000000, 10000000000000)
    for a, b, prize in claw_machines:
        adjusted.append((a, b, sum_tuples(prize, to_add)))
    return adjusted

"""
ax * A + bx * B = px
ay * A + by * B = py
---
ay * ax * A + ay * bx * B = ay * px
ax * ay + A + ax * by * B = ax * py
---
B * (ay * bx - ax * by) = ay * px - ax * py
B = (ay * px - ax * py) / (ay * bx - ax * by)
"""
def compute_tokens_opt(a, b, prize):
    ax, ay = a
    bx, by = b
    px, py = prize
    B = (ay * px - ax * py) // (ay * bx - ax * by)
    A = (px - B * bx) // ax
    if A * ax + B * bx == px and A * ay + B * by == py:
        return 3 * A + B
    else:
        return 0


def solve_part_two(fname):
    claw_machines = parse_two(fname)
    tokens = 0
    for a, b, prize in claw_machines:
        tokens += compute_tokens_opt(a, b, prize)
    return tokens


def run_solution(day, ignore_example=False, ex_answer_1=480, ex_answer_2=0):
    example_file = f'examples/example{day}.txt'
    input_file = f'inputs/input{day}.txt'

    if not ignore_example:
        p1 = solve_part_one(example_file)
        print(p1)
        assert p1 == ex_answer_1, "Part 1 example case is incorrect."

    print("Solution to Part 1:", solve_part_one(input_file))
    print("\n**********************\n")

    print("Solution to Part 2:", solve_part_two(input_file))


if __name__ == '__main__':
    # File stuff
    current_script = __file__
    num = os.path.basename(current_script).split('.')[0]
    try:
        num = int(num)
    except ValueError as e:
        print(f"Your file is not a number: {num}.")
        exit(1)
    if not os.path.exists(f'inputs/input{num}.txt'):
        get_input(day=num)
    print(f"Solving problem {num}\n*************\n")

    run_solution(num)
