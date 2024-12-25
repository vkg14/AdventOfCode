import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *


def _is_lock(sch):
    return all(char == '#' for char in sch.split('\n')[0].strip())


def get_heights(sch):
    is_lock = _is_lock(sch)
    grid = sch.split('\n')
    m = len(grid)
    n = len(grid[0])
    heights = []
    for c in range(0, n):
        cur = 0
        for _r in range(1, m):
            r = _r if is_lock else m-1-_r
            if grid[r][c] == '#':
                cur += 1
            else:
                break
        heights.append(cur)
    return is_lock, heights, m-2

def parse(fname):
    with open(fname) as f:
        content = f.read().split('\n\n')
    locks = []
    keys = []
    sz = 0
    for sch in content:
        is_lock, heights, sz = get_heights(sch)
        if is_lock:
            locks.append(heights)
        else:
            keys.append(heights)
    return locks, keys, sz


def solve_part_one(fname):
    locks, keys, sz = parse(fname)
    t = 0
    for l in locks:
        for k in keys:
            t += 1 if all(x+y <= sz for x, y in zip(k, l)) else 0
    return t


def solve_part_two(fname):
    return 0


def run_solution(day, ignore_example=False, ex_answer_1=3, ex_answer_2=0):
    example_file = f'examples/example{day}.txt'
    input_file = f'inputs/input{day}.txt'

    if not ignore_example:
        p1 = solve_part_one(example_file)
        print(p1)
        assert p1 == ex_answer_1, "Part 1 example case is incorrect."

    print("Solution to Part 1:", solve_part_one(input_file))
    print("\n**********************\n")

    if not ignore_example:
        p2 = solve_part_two(example_file)
        print(p2)
        assert p2 == ex_answer_2, "Part 2 example case is incorrect."

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
