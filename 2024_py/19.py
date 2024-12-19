import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce, cache
from heapq import heappush, heappop

from helpers import *


def parse(fname):
    with open(fname) as f:
        patterns, lines = f.read().split('\n\n')
    patterns = set(patterns.split(', '))
    lines = lines.split('\n')
    return patterns, lines


def solve_part_one(fname):
    patterns, lines = parse(fname)

    @cache
    def backtrack(line, idx):
        if idx == len(line):
            return True

        for j in range(len(line), idx, -1):
            nxt = line[idx:j]
            if nxt in patterns and backtrack(line, j):
                return True
        return False

    t = 0
    for l in lines:
        if backtrack(l, 0):
            t += 1

    return t


def solve_part_two(fname):
    patterns, lines = parse(fname)

    @cache
    def backtrack(line, idx):
        if idx == len(line):
            return 1

        total = 0
        for j in range(len(line), idx, -1):
            nxt = line[idx:j]
            if nxt in patterns:
                total += backtrack(line, j)

        return total

    t = 0
    for l in lines:
        t += backtrack(l, 0)

    return t


def run_solution(day, ignore_example=False, ex_answer_1=6, ex_answer_2=16):
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
