import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *


def solve_part_one(fname):
    with open(fname, "r") as f:
        lines = [[c for c in l.strip()] for l in f.readlines()]
    m = len(lines)
    n = len(lines[0])
    t = 0
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            if lines[r][c] != 'X':
                continue
            down = [(r+i, c) for i in range(4)]
            up = [(r-i, c) for i in range(4)]
            right = [(r, c+i) for i in range(4)]
            left = [(r, c-i) for i in range(4)]
            diag1 = [(r+i, c+i) for i in range(4)]
            diag2 = [(r-i, c-i) for i in range(4)]
            diag3 = [(r-i, c+i) for i in range(4)]
            diag4 = [(r+i, c-i) for i in range(4)]
            for attempt in [down, up, right, left, diag1, diag2, diag3, diag4]:
                success = True
                for coords, letter in zip(attempt, ['X', 'M', 'A', 'S']):
                    r1, c1 = coords
                    if not in_bounds(coords, m, n) or lines[r1][c1] != letter:
                        success = False
                        break
                if success:
                    t += 1
    return t


def solve_part_two(fname):
    with open(fname, "r") as f:
        lines = [[c for c in l.strip()] for l in f.readlines()]
    m = len(lines)
    n = len(lines[0])
    t = 0
    for r in range(m):
        for c in range(n):
            if lines[r][c] != 'A':
                continue
            diag1 = [(r-1, c-1), (r+1, c+1)]
            diag2 = [(r+1, c-1), (r-1, c+1)]
            success = True
            for attempt in [diag1, diag2]:
                total = set([lines[r1][c1] if in_bounds((r1,c1), m, n) else 'X' for r1, c1 in attempt])
                if total != {'M', 'S'}:
                    success = False
                    break
            if success:
                t += 1
    return t


def run_solution(day, ignore_example=False, ex_answer_1=18, ex_answer_2=9):
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
